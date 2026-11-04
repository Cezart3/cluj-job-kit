#!/usr/bin/env python3
"""Build and check the CVs. Replaces cv/build.sh and pdftotext, so it runs anywhere Python does.

    python build.py                   rebuild every CV in me/cv-data and check them all
    python build.py --one FILE        build one throwaway CV from a data file, no checks
    python build.py --letter FILE     build one cover letter
    python build.py --text PDF        print a PDF's pages, word count and text

It re-runs itself with me/.venv's Python (made by setup.py), so plain `python` is enough.
Done only when it prints ALL GOOD.
"""
import collections
import glob
import importlib.util
import os
import pathlib
import re
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent
ME = pathlib.Path(os.environ.get("JOBKIT_ME") or KIT / "me")
VENV = KIT / "me" / ".venv"
VPY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_venv():
    try:
        import reportlab, pypdf  # noqa: F401,E401
        return
    except ImportError:
        pass
    # Compare prefixes, not executables: on Linux the venv python is a symlink to the system one.
    if VPY.exists() and pathlib.Path(sys.prefix).resolve() != VENV.resolve():
        sys.exit(subprocess.run([str(VPY), __file__, *sys.argv[1:]]).returncode)
    sys.exit("reportlab or pypdf missing. Run: python setup.py")


ensure_venv()
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
os.environ["JOBKIT_ME"] = str(ME)
sys.path.insert(0, str(KIT / "cv"))
from pypdf import PdfReader  # noqa: E402

import cvlib as cv  # noqa: E402
import letter as letter_mod  # noqa: E402
import render as render_mod  # noqa: E402


def pdf_text(path):
    r = PdfReader(path)
    return [p.extract_text() or "" for p in r.pages]


def page_fill(path):
    """Share of page 1 height that has text on it, top to the lowest line."""
    page = PdfReader(path).pages[0]
    height = float(page.mediabox.height)
    ys = []
    page.extract_text(visitor_text=lambda t, cm, tm, *_: ys.append(tm[5] * cm[3] + cm[5]) if t.strip() else None)
    return (height - min(ys)) / height * 100 if ys else 0


def load(path):
    spec = importlib.util.spec_from_file_location("d", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(data):
    problems = []
    # A missing space at a Python string join silently glues two words together.
    for f in data + [str(ME / "profile.py")]:
        lines = pathlib.Path(f).read_text(encoding="utf-8").split("\n")
        for i in range(len(lines) - 1):
            a, b = lines[i].rstrip(), lines[i + 1].strip()
            ma, mb = re.search(r'"([^"]*)"$', a), re.match(r'"([^"]*)"', b)
            if ma and mb and not a.endswith(('",', '"),', '")', '"]')):
                left, right = ma.group(1), mb.group(1)
                if left and right and not left.endswith(" ") and not right.startswith(" "):
                    problems.append(f"glued string {os.path.basename(f)}:{i + 1} ...{left[-25:]!r} + {right[:25]!r}")

    # An override that equals the default is a copy waiting to go stale.
    flat = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())  # noqa: E731
    defaults = {j["key"]: flat("".join(j["bullets"])) for j in cv.JOBS[1:]}
    for f in data:
        for k, v in (getattr(load(f), "OVERRIDES", None) or {}).items():
            if flat("".join(v)) == defaults.get(k):
                problems.append(f"pointless override {os.path.basename(f)}: {k} equals the default")

    pdfs = sorted({load(f).OUT for f in data})
    print("  CV                                          pages  fill   p2   dupes")
    for name in pdfs:
        path = os.path.join(cv.OUT_DIR, name)
        pages = pdf_text(path)
        text = "\n".join(pages)
        n = len(pages)
        fill = page_fill(path)
        words = re.findall(r"[a-z0-9%+/&-]+", re.sub(r"\s+", " ", text.lower()))
        grams = collections.Counter(" ".join(words[i:i + 6]) for i in range(len(words) - 5))
        dupes = [g for g, c in grams.items() if c > 1]
        p2 = len([l for l in pages[1].split("\n") if l.strip()]) if n == 2 else 0
        flag = ""
        if n > 2:
            flag += " <- TOO LONG"
            problems.append(f"{name}: {n} pages")
        elif n == 2 and p2 < 6:
            flag += " <- page 2 is a stub"
        if n == 1 and fill < 88:
            flag += " <- looks thin"
        if dupes:
            problems.append(f"{name}: {len(dupes)} repeated 6-word phrases")
        print(f"  {name[:-4]:<42} {n:>3}   {fill:>4.0f}%  {p2:>3}   {len(dupes):>4}{flag}")
        for g in dupes[:3]:
            print(f"        repeated: {g}")
        if re.search("[–—]", text):
            problems.append(f"{name}: has an en or em dash")
        for tool in cv.BANNED:
            if re.search(r"\b" + re.escape(tool.lower()) + r"\b", text.lower()):
                problems.append(f"{name}: banned tool {tool!r} is on the page")
    return problems


def main():
    args = sys.argv[1:]
    if args[:1] == ["--one"] and len(args) == 2:
        return render_mod.render(render_mod.load(args[1]))
    if args[:1] == ["--letter"] and len(args) == 2:
        return letter_mod.render(letter_mod.load(args[1]))
    if args[:1] == ["--text"] and len(args) == 2:
        pages = pdf_text(args[1])
        text = "\n".join(pages)
        print(f"pages: {len(pages)}  words: {len(text.split())}\n")
        return print(text)
    if args:
        sys.exit(__doc__)

    data = sorted(glob.glob(str(ME / "cv-data" / "*.py")))
    if not data:
        sys.exit(f"No data files in {ME / 'cv-data'}")
    failed = False
    for f in data:
        try:
            render_mod.render(render_mod.load(f))
        except Exception as e:  # report every broken file, not just the first
            print(f"BUILD FAILED  {f}\n  {e}")
            failed = True
    if failed:
        sys.exit("\nFix the error above, then run again.")
    problems = check(data)
    print()
    print("  ALL GOOD" if not problems else "  PROBLEMS:\n    " + "\n    ".join(problems))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
