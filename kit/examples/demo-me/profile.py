# DEMO profile of a fictional student. Not a real person.
# Try it:  python build.py   with JOBKIT_ME=examples/demo-me  (see kit/README.md)

NAME = "Ana Pop"

CONTACT = ("ana.pop@example.com &middot; github.com/example &middot; "
           "Cluj-Napoca,&nbsp;Romania")

EDUCATION = "BSc Computer Science, Example University &middot; Oct 2023 - Present, third year"

SPEAKING = "Romanian (native), English (fluent)"

TOOLS = "Git, GitHub, Linux, Docker"

BANNED = []

ACCENT = "#1F4E99"

JOBS = [
    {"key": "tutor", "title": "Teaching Assistant, Data Structures",
     "company": "Example University &middot; part-time", "dates": "Feb 2025 - Present",
     "bullets": [
         "Run two weekly lab groups of 25 students; review their C++ homework and explain the fixes.",
         "Wrote an automated grader with 40 test cases that cut grading time per assignment from 3 hours to 30 minutes.",
     ]},
    {"key": "planner", "section": "PROJECTS", "title": "Study Planner, web app",
     "company": "Python, FastAPI, PostgreSQL, React", "dates": "github.com/example/planner",
     "bullets": [
         "Lets students import their timetable and plan exam revision; 120 students used it last session.",
         "REST API with 35 pytest tests and JWT login; deployed on a free cloud tier.",
     ]},
    {"key": "hackathon", "section": "PROJECTS", "title": "Bus Delay Predictor, hackathon",
     "company": "Python, pandas, scikit-learn", "dates": "2nd place, Mar 2025",
     "bullets": [
         "Built a model on six months of public transport data that predicts delays within 3 minutes for 70% of trips.",
     ]},
]
