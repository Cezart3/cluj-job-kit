#!/usr/bin/env python3
"""Build one CV from a data file.

    python build.py --one me/cv-data/backend.py
    python build.py --one me/tmp/acme.py      # a throwaway CV for one posting
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cvlib as cv  # noqa: E402

FIELDS = ("OUT", "TITLE", "ROLE", "TAGLINE", "SUMMARY", "SKILLS", "CURRENT")


def load(path):
    spec = importlib.util.spec_from_file_location("cvdata", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    missing = [f for f in FIELDS if not hasattr(mod, f)]
    if missing:
        sys.exit(f"{os.path.basename(path)} is missing: {', '.join(missing)}")
    return mod


def render(d):
    skills = [(head, cv.TOOLS if body == "TOOLS" else body) for head, body in d.SKILLS]
    bullets = cv.with_defaults(d.CURRENT, getattr(d, "OVERRIDES", None))

    story = []
    story += cv.header(d.ROLE, d.TAGLINE)
    story += cv.sec("SUMMARY")
    story += cv.summary(d.SUMMARY)
    story += cv.sec("CORE SKILLS")
    story += cv.skills(skills)
    section = None
    for i, job in enumerate(bullets):
        want = cv.JOBS[i].get("section", "EXPERIENCE")
        if want != section:
            story += cv.sec(want)
            section = want
        story += cv.job(i, job)
    story += cv.speaking()
    story += cv.education()
    cv.build(d.OUT, d.TITLE, story)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python build.py --one <data file>")
    render(load(sys.argv[1]))
