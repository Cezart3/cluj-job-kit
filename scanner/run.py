#!/usr/bin/env python3
"""Read every board, keep the tech jobs open to someone in Romania, write site/data/jobs.json.

    python scanner/run.py                 all boards (boards-ro.txt + boards-global.txt)
    python scanner/run.py --ro-only       only boards-ro.txt, fast, for testing
    python scanner/run.py --workers 16

Standard library only. Works the same on Linux, macOS and Windows.
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify import classify  # noqa: E402
from sources import SOURCES  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "site" / "data" / "jobs.json"
LISTS = [HERE / "boards-ro.txt", HERE / "boards-global.txt"]


def read_boards(paths):
    """[(source, slug, display name)] from 'source:slug | Name' lines, deduplicated."""
    seen, out = set(), []
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            board, _, name = line.partition("|")
            src, slug = (x.strip() for x in board.split(":", 1))
            if src in SOURCES and (src, slug) not in seen:
                seen.add((src, slug))
                out.append((src, slug, name.strip() or pretty(slug)))
    return out


def pretty(slug):
    return slug.replace(".com", "").replace("-", " ").replace("_", " ").title()


def scan(board):
    src, slug, name = board
    raw = SOURCES[src](slug)
    if raw is None:
        return board, None
    rows = []
    for r in raw:
        row = classify(r)
        if row and row["url"]:
            row["company"] = name
            rows.append(row)
    return board, rows


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ro-only", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()

    boards = read_boards(LISTS[:1] if a.ro_only else LISTS)
    old = {}
    if OUT.exists():
        try:
            old = {j["url"]: j for j in json.loads(OUT.read_text(encoding="utf-8")).get("jobs", [])}
        except (json.JSONDecodeError, OSError):
            old = {}

    today = str(datetime.date.today())
    jobs, failed, answered = {}, [], 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, (board, rows) in enumerate(ex.map(scan, boards), 1):
            if rows is None:
                failed.append(f"{board[0]}:{board[1]}")
                continue
            answered += 1
            for r in rows:
                r["first_seen"] = old.get(r["url"], {}).get("first_seen", today)
                jobs[r["url"]] = r
            if i % 100 == 0:
                print(f"  {i}/{len(boards)} boards", file=sys.stderr)

    # A board that did not answer today keeps yesterday's rows, so a timeout does not hide jobs.
    failed_set = set(failed)
    by_board = {}
    for src, slug, name in boards:
        by_board[name] = f"{src}:{slug}"
    for url, j in old.items():
        if url not in jobs and by_board.get(j.get("company")) in failed_set:
            jobs[url] = j

    rows = sorted(jobs.values(), key=lambda j: (j["first_seen"], j.get("posted", "")), reverse=True)
    write_json(OUT, dict(updated=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"),
                         boards=len(boards), answered=answered, failed=sorted(failed), jobs=rows))
    new = sum(1 for j in rows if j["first_seen"] == today)
    print(f"{len(rows)} jobs ({new} new today) from {answered}/{len(boards)} boards -> {OUT}")


if __name__ == "__main__":
    main()
