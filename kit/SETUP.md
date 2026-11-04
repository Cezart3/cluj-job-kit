# Setup (instructions for Claude)

This kit starts empty. Your job: interview the user for every fact below, then fill `me/` from
their answers. Never invent or assume a fact they did not give you.

If they hand you a CV/resume (pasted text or a file), read it first and pre-fill your best
answer to each question below from it, then confirm every one with them instead of asking cold.
Say plainly which answers came from their file and which still need an answer. Either way, do
not proceed past the interview until every question below is answered or explicitly skipped.

Most users are students. Personal, university and hackathon projects are real evidence: give
them the same care as jobs, under a PROJECTS heading.

Talk to the user in their language (Romanian or English). The CV itself is written in the
language they ask for, English by default.

## 1. Install

- Run `python setup.py` (or `python3 setup.py`). It copies `templates/me/` to `me/` and makes
  `me/.venv` with reportlab and pypdf. Works on Windows, macOS and Linux.
- Fix anything it prints as MISSING. Ask before installing software.

## 2. The interview

Ask in short batches, not all at once. Wait for real answers, do not guess a plausible one.

**About them**
- Full name, as it should appear on a CV.
- Email, phone (optional), city and country, LinkedIn, GitHub or portfolio, any other link
  worth showing.
- Languages spoken, with level.
- Education: degree, school, dates, year of study, for each.

**Where and how they can work**
- Countries they can legally work in (citizenship, residency). Be specific: "EU citizen".
- Which cities for on-site or hybrid, and whether remote is fine.
- Time zone (IANA name, e.g. `Europe/Bucharest`).
- Internship, part-time, full-time, or any. How many hours a week fit around university.
- Minimum acceptable pay, or "not now". Is unpaid acceptable?
- Any hard dealbreaker that should be an instant SKIP.

**What they're looking for**
- Target role(s) and level, in their own words: "backend internship", "junior frontend".
  Do not normalize this into a title they did not say.
- How many focus CVs they want (2 to 4 is normal for students) and what each should emphasize.

**Their history, the source of truth**
For each job, internship, volunteering role and project, newest first:
- Name, their role, dates, location and remote status, type (job, volunteer, freelance, project).
- One line on what the company or project does.
- What they actually did: facts they can defend in an interview, with numbers where true
  (users, tests, pull requests, speed-ups).
- Tools and technologies used, confirmed only.

**Odds and ends**
- Tools recruiters often assume for this role that they have never actually used
  (goes to `BANNED`, so no CV claims it by accident).
- Links worth citing: live demos, GitHub repos, publications.
- An accent color for the CV, or "default".

## 3. Fill `me/`

Write the interview into, in this order:

1. `me/work-history.txt`: the source of truth, in the format the template shows. Every fact
   that will ever appear on a CV or in a fit score must be here first.
2. `me/profile.py`: `NAME`, `CONTACT`, `EDUCATION`, `SPEAKING`, `TOOLS`, `BANNED`, `ACCENT`,
   `JOBS`. Every fact here must also be in `work-history.txt`, worded the same way.
   Projects go in `JOBS` with `"section": "PROJECTS"`, after the real jobs.
3. `me/preferences.md`: hard filter, where they can work, what they want, flags that are not
   kills.
4. `me/cv-data/*.py`: one file per focus CV they asked for. Copy
   `templates/me/cv-data/example.py`, never edit the original, delete `me/cv-data/example.py`,
   and never leave a bracketed placeholder in a file `build.py` will render.

The PDF fonts cover Western European letters only. Write Romanian names without ș, ț, ă
(for example "Iasi", "Brasov"), or they print as boxes.

## 4. Build the CVs

- Run `python build.py` until it prints `ALL GOOD`.
- Show them the PDFs in `me/cvs/`.
- Ask if a focus is missing or wrong. Change only `me/cv-data/*.py`.

## 5. Done

Tell them, in 3 lines:
- the daily job list is on the website in the repo README; filter by city and level there
- paste any job link into Claude to get a GO / SKIP verdict and the right CV
- `python build.py` rebuilds the CVs after a fact changes
