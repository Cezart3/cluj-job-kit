# Contributing / Contribuții

## Add a company / Adaugă o firmă

1. Open the company's careers page and click a job. Look at the link:

   | Link looks like | Line to add |
   |---|---|
   | `job-boards.greenhouse.io/acme/...` or `boards.greenhouse.io/acme` | `greenhouse:acme \| Acme` |
   | `jobs.lever.co/acme/...` | `lever:acme \| Acme` |
   | `jobs.ashbyhq.com/acme/...` | `ashby:acme \| Acme` |
   | `jobs.smartrecruiters.com/Acme/...` | `smartrecruiters:acme \| Acme` |
   | `apply.workable.com/acme/...` | `workable:acme \| Acme` |
   | `acme.recruitee.com/...` | `recruitee:acme \| Acme` |

2. Add the line to `scanner/boards-ro.txt`, in its section.
3. Check it: `python scanner/run.py --ro-only` should print your company's jobs in the count.
4. Open a pull request. The test workflow runs on it.

Workday, Teamtailor and custom career sites are not supported yet. Open an issue with the link
anyway: it helps decide what to add next.

**RO:** Deschide pagina de cariere a firmei, uită-te la linkul unui job, adaugă rândul potrivit din
tabel în `scanner/boards-ro.txt` și deschide un pull request.

## Fix a wrong label / Etichetă greșită

City, level and field come from `scanner/classify.py`. If a job lands in the wrong place, add a
test case for its title to `scanner/test_classify.py`, make it pass, and open a pull request.

## Rules

- No personal data in the repo: nothing from anyone's `kit/me/`.
- Only public job-board APIs. No scraping of sites that forbid it (LinkedIn, eJobs, Indeed...).
- Standard library only in `scanner/`, so it runs anywhere with plain Python.
