#!/usr/bin/env python3
"""One-time setup for the CV kit. Safe to run again: it never overwrites files in me/.

    python setup.py            copy templates/me to me/, make me/.venv with reportlab and pypdf
    python setup.py --global   also link the job-fit skill into ~/.claude/skills (use it from any folder)

Works on Windows, macOS and Linux.
"""
import os
import pathlib
import shutil
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent
ME = KIT / "me"
VENV = ME / ".venv"
VPY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
PACKAGES = ["reportlab", "pypdf"]


def copy_templates():
    src = KIT / "templates" / "me"
    for f in src.rglob("*"):
        if f.is_file():
            dst = ME / f.relative_to(src)
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                print("created", dst.relative_to(KIT))
    (ME / "tmp").mkdir(parents=True, exist_ok=True)


def make_venv():
    if not VPY.exists():
        if subprocess.run([sys.executable, "-m", "venv", str(VENV)]).returncode != 0:
            shutil.rmtree(VENV, ignore_errors=True)
            sys.exit("\nCould not make me/.venv. On Debian or Ubuntu, install the venv module first:\n"
                     "    sudo apt install python3-venv\nthen run python3 setup.py again.")
        print("created me/.venv")
    subprocess.run([str(VPY), "-m", "pip", "install", "-q", "--disable-pip-version-check", *PACKAGES], check=True)
    for p in PACKAGES:
        ok = subprocess.run([str(VPY), "-c", f"import {p}"], capture_output=True).returncode == 0
        print(("ok " if ok else "MISSING ") + p)


def link_skill():
    target = KIT / ".claude" / "skills" / "job-fit"
    link = pathlib.Path.home() / ".claude" / "skills" / "job-fit"
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.exists() or link.is_symlink():
        print(f"{link} exists. Left it alone.")
        return
    if os.name == "nt":
        # A junction needs no admin rights, unlike a symlink.
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)
    else:
        link.symlink_to(target, target_is_directory=True)
    print("linked", link)


def main():
    if sys.version_info < (3, 9):
        sys.exit("Python 3.9 or newer is needed.")
    copy_templates()
    make_venv()
    if "--global" in sys.argv:
        link_skill()
    print("ok claude" if shutil.which("claude") else
          "MISSING claude CLI (needed for the interview and job verdicts): https://claude.com/claude-code")
    print("\nNext: open Claude Code in this folder and say: Read SETUP.md and set me up.")


if __name__ == "__main__":
    main()
