# CV kit

One file of facts about you, several focused CVs, and an honest GO / SKIP verdict for any job.
Adapted from [job-hunt-kit-template](https://github.com/jpita/job-hunt-kit-template) by Gabriel Pita.

## Start

```
python setup.py        # once: makes me/ and a private Python with reportlab and pypdf
claude                 # open Claude Code in this folder
```

Tell Claude: **Read SETUP.md and set me up.** It interviews you (give it your current CV to go
faster), writes your facts into `me/`, and builds your CVs into `me/cvs/`.

On Debian or Ubuntu, if `setup.py` asks for it: `sudo apt install python3-venv`.

## Every day after that

- **Paste a job link into Claude.** It reads the posting, researches the company, compares the
  requirements to your real history and answers GO, GO WITH CAVEATS or SKIP. Only after you say
  go does it pick or build the right CV.
- **Changed a fact?** Edit `me/work-history.txt` and `me/profile.py`, then `python build.py`.
- **Cover letter?** Ask Claude for one. Rules are in `cv/README.md`.

## Commands

| Command | Does |
|---|---|
| `python build.py` | Rebuild every CV in `me/cv-data/` and check them. Done at `ALL GOOD`. |
| `python build.py --one me/tmp/x.py` | Build one throwaway CV for a single posting |
| `python build.py --letter me/tmp/l.py` | Build one cover letter |
| `python build.py --text me/cvs/X.pdf` | Print a PDF's pages, word count and text |

The build fails on things recruiters notice: the same claim twice, a tool you never used
(`BANNED` in `me/profile.py`), more than 2 pages, or em dashes.

## See a demo first

`examples/demo-me/` is a fictional student. Build her CV without any setup interview:

```
# macOS / Linux
JOBKIT_ME=examples/demo-me python3 build.py
# Windows PowerShell
$env:JOBKIT_ME="examples/demo-me"; python build.py; Remove-Item Env:JOBKIT_ME
```

The PDF lands in `examples/demo-me/cvs/`.

## Privacy

Everything about you lives in `me/`, which git ignores. Never commit it and never push a fork
with it. If you fork this repo, keep personal changes out of it.
