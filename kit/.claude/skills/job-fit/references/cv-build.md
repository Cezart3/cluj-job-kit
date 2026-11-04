# Building the CV and the cover letter

`$KIT/cv/README.md` is the authority. Read it first, in the same turn.

## Order of work

1. Copy the closest `me/cv-data/*.py` to `me/tmp/<company>.py`. Never edit the original.
2. Change only OUT, TITLE, ROLE, TAGLINE, SUMMARY, SKILLS, CURRENT.
3. Build: `python "$KIT/build.py" --one "$KIT/me/tmp/<company>.py"`.
4. Run `python "$KIT/build.py"` too if anything in `me/profile.py` changed. Done only at `ALL GOOD`.
5. Delete the `me/tmp/` data file. The PDF stays in `me/cvs/`.
6. If the posting CV needed a new fact, add it to `work-history.txt` and a focus CV first.

## Check the result

```
python "$KIT/build.py" --text "$KIT/me/cvs/<name>.pdf"
```

- 1 or 2 pages.
- Each job reads `Role · Employer · Dates` on one line.

## Writing rules

- The first three SKILLS rows carry the ad's must-haves, in the ad's words where true.
- The summary positions, the bullets prove, the skills list. No claim twice.
- Never add a tool because the ad lists it.
- Match the pitch to the level of the ad.
- No em or en dashes.

## Cover letters

Only when asked. Copy `$KIT/cv/examples/letter.py` to `$KIT/me/tmp/`, build with `python "$KIT/build.py" --letter <file>`. Follow the "Cover letters" section of `cv/README.md`.
