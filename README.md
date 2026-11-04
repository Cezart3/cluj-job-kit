# Cluj Job Kit

**[Română](#română) · [English](#english)**

Tech jobs for students in Romania, collected every morning from companies' public job boards,
plus a kit that builds a clean, honest CV and tells you whether a job is worth applying to.

---

## Română

### Ce face

1. **Site cu joburi, actualizat zilnic.** Un script citește în fiecare dimineață board-urile
   publice de joburi (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee) și păstrează
   joburile tech din România sau remote din Europa. Pe site alegi orașul, nivelul (internship,
   junior, mid, senior) și domeniul (backend, frontend, data, devops, QA, embedded...), iar
   butonul **Aplică** te duce direct la anunțul firmei.
2. **Kit pentru CV** (folderul [`kit/`](kit/)). Cu Claude Code, kit-ul te intervievează, îți
   construiește 2-4 CV-uri pe focus (de exemplu backend și data) din aceleași fapte și îți dă un
   verdict GO / SKIP pentru orice job pe care îl lipești. Nu inventează nimic: tot ce apare pe CV
   vine din răspunsurile tale.

Filtrele sunt în link, deci poți trimite direct o căutare, de exemplu
`/#city=cluj&level=intern,junior` = internship-uri și joburi junior în Cluj.

### Folosește site-ul

Deschide linkul site-ului (vezi descrierea repo-ului). Nu trebuie instalat nimic.

### Folosește kit-ul de CV

Ai nevoie de Python 3.9+ și [Claude Code](https://claude.com/claude-code). Merge pe Windows,
macOS și Linux.

```
git clone https://github.com/Cezart3/cluj-job-kit
cd cluj-job-kit/kit
python setup.py
claude
```

Apoi spune-i lui Claude: *Read SETUP.md and set me up.* Dacă ai deja un CV, dă-i fișierul și
pornește de la el. Detalii în [`kit/README.md`](kit/README.md).

### Lipsește o firmă?

Adaugă un rând în [`scanner/boards-ro.txt`](scanner/boards-ro.txt) și deschide un pull request.
Vezi [CONTRIBUTING.md](CONTRIBUTING.md). Fiecare firmă adăugată ajută toți studenții.

---

## English

### What it does

1. **A job site, updated daily.** Every morning a script reads public job boards (Greenhouse,
   Lever, Ashby, SmartRecruiters, Workable, Recruitee) and keeps tech jobs in Romania or remote in
   Europe. On the site you pick the city, level (internship, junior, mid, senior) and field
   (backend, frontend, data, devops, QA, embedded...), and **Apply** takes you straight to the
   company's posting.
2. **A CV kit** (the [`kit/`](kit/) folder). With Claude Code, it interviews you, builds 2-4 focus
   CVs (say, backend and data) from one set of facts, and gives a GO / SKIP verdict for any job you
   paste. It invents nothing: every line on the CV comes from your answers.

Filters live in the link, so you can share a search, for example
`/#city=cluj&level=intern,junior` = internships and junior jobs in Cluj.

### Use the site

Open the site link (see the repo description). Nothing to install.

### Use the CV kit

You need Python 3.9+ and [Claude Code](https://claude.com/claude-code). Works on Windows, macOS
and Linux.

```
git clone https://github.com/Cezart3/cluj-job-kit
cd cluj-job-kit/kit
python setup.py
claude
```

Then tell Claude: *Read SETUP.md and set me up.* If you already have a CV, hand it the file to start
from. Details in [`kit/README.md`](kit/README.md).

### Missing a company?

Add a line to [`scanner/boards-ro.txt`](scanner/boards-ro.txt) and open a pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md).

---

## How it is built

| Part | Where | Runs |
|---|---|---|
| Scanner | `scanner/` (Python, standard library only) | GitHub Actions, every morning |
| Site | `site/` (static HTML, CSS, JS) | Vercel, redeployed on each data commit |
| CV kit | `kit/` (Python + reportlab, pypdf) | Your computer, with Claude Code |

Run the scanner yourself: `python scanner/run.py` (all boards, ~5 minutes) or
`python scanner/run.py --ro-only` (Romanian boards, ~15 seconds). Tests:
`python -m unittest discover -s scanner`. Preview the site: `python -m http.server -d site 8000`.

The scanner only uses the public JSON feeds these platforms provide for company career pages.
It does not log in anywhere and does not read LinkedIn, eJobs or Indeed; the site links to their
searches instead. Jobs belong to the companies that post them: always check the original posting.

## Credits

Built on [**job-hunt-kit-template**](https://github.com/jpita/job-hunt-kit-template) by
Gabriel Pita (MIT). The CV builder, the job-fit skill, the interview in `kit/SETUP.md` and the
seed list of international companies come from it. This repo adds the Romanian job site, more
job-board sources, Windows and Linux support, and a student-oriented setup.

## License

[MIT](LICENSE). Copyright (c) 2026 Gabriel Pita, Copyright (c) 2026 Cezar Tocaciu.
