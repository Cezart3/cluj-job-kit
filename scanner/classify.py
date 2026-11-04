"""Turn a raw posting into city, level and field. Pure functions, no network.

Run the tests with:  python -m unittest discover scanner
"""
import re

# City id -> pattern. The id is what the site filters on.
CITIES = {
    "cluj": r"cluj",
    "bucuresti": r"bucharest|bucure[sșş]ti|bucuresti|ilfov|otopeni|voluntari|pipera",
    "timisoara": r"timi[sșş]oara",
    "iasi": r"\bia[sșş]i\b",
    "brasov": r"bra[sșş]ov",
    "sibiu": r"sibiu",
    "oradea": r"oradea",
    "craiova": r"craiova",
    "constanta": r"constan[tțţ]a",
    "targu-mures": r"t[aâi]rgu[ -]mure[sșş]",
    "arad": r"\barad\b",
    "pitesti": r"pite[sșş]ti",
}
CITY_RX = {k: re.compile(v, re.I) for k, v in CITIES.items()}
ROMANIA_STRICT = re.compile(r"rom[aâ]nia", re.I)
REMOTE = re.compile(r"\bremote(ly)?\b|work from home|home[- ]based|anywhere|\bwfh\b", re.I)
# A remote posting counts only if it is open to Romania: it names Romania, Europe, or anywhere.
# A bare "Remote" from a US company is usually US-only, so it is left out.
REMOTE_OK = re.compile(
    r"rom[aâ]nia|europe|\beu\b|emea|\bcet\b|\beet\b|worldwide|anywhere|global", re.I)
HYBRID = re.compile(r"hybrid|hibrid", re.I)

LEVELS = [
    ("intern", r"\bintern(ship)?s?\b|trainee|working student|\bstudent\b|practic[aă]|summer (program|school)|"
               r"\bco-?op\b|apprentice|stagiu|stagiar|internship"),
    ("senior", r"\bsenior\b|\bsr\.?\b|\blead\b|\bstaff\b|principal|\bhead\b|architect|manager|director|"
               r"\bexpert\b|\bvp\b|chief"),
    ("junior", r"\bjunior\b|\bjr\.?\b|entry[- ]level|graduate|new grad|early[- ]career|\bassociate\b|"
               r"\bI\b$|\b1\b$|beginner|debutant"),
]
LEVEL_RX = [(k, re.compile(v, re.I)) for k, v in LEVELS]
# Hints the boards send in their own fields (SmartRecruiters, Recruitee).
# Only the intern hint is trusted: some companies label every posting "entry level".
LEVEL_HINT = {"internship": "intern", "student": "intern"}

# Field id -> pattern, first match wins, so the specific ones come first.
FIELDS = [
    ("qa", r"\bqa\b|quality assurance|\btest(er|ing)?\b|\bsdet\b|automation engineer"),
    ("security", r"secur|penetration|\bsoc\b|cyber|\bappsec\b|devsecops"),
    ("devops", r"devops|\bsre\b|site reliability|\bcloud\b|platform engineer|infrastructure|"
               r"kubernetes|\bsysadmin\b|system administrator|network engineer"),
    ("data", r"\bdata\b|machine learning|\bml\b|\bai\b|artificial intelligence|scientist|analytics|"
             r"\bbi\b|business intelligence|\bllm\b|computer vision|\bnlp\b"),
    ("mobile", r"\bmobile\b|android|\bios\b|flutter|react native|kotlin|swift"),
    ("embedded", r"embedded|firmware|autosar|\bc\+\+\b|automotive|hardware|fpga|\brtos\b|electronics"),
    ("frontend", r"front[- ]?end|\bui\b|react\b|angular|\bvue\b|web developer|javascript"),
    ("fullstack", r"full[- ]?stack"),
    ("backend", r"back[- ]?end|\bjava\b|\.net\b|\bc#|python|golang|\bgo (developer|engineer)|node\.?js|"
                r"\bphp\b|ruby|scala|rust|\bapi\b|microservice"),
    # No bare "engineer": it pulls in construction, process and sales engineers.
    ("software", r"software|developer|programmer|\bswe\b|\bdev\b|programator|dezvoltator"),
]
FIELD_RX = [(k, re.compile(v, re.I)) for k, v in FIELDS]
# Titles that match the words above but are not tech jobs.
NOT_TECH = re.compile(
    r"sales|account (executive|manager)|business develop|recruit|talent|\bhr\b|marketing|legal|counsel|"
    r"finance|accountant|payroll|customer (success|support)|electrician|mechanic|technician|operator|"
    r"buyer|procurement|logistic|warehouse|driver|nurse|lawyer|office|receptionist|cashier|"
    r"civil engineer|mechanical engineer|process engineer|(?<!software )quality engineer|manufacturing|"
    r"data entry|collector|annotator|driver", re.I)


def cities(loc):
    """City ids named in a location string. "romania" when it names only the country."""
    found = [k for k, rx in CITY_RX.items() if rx.search(loc)]
    if not found and ROMANIA_STRICT.search(loc):
        found = ["romania"]
    return found


def place(loc, remote_flag=False):
    """(cities, remote) for a posting, or None if it is not open to someone in Romania."""
    found = cities(loc)
    remote = bool(remote_flag or REMOTE.search(loc))
    if found:
        return found, remote
    if remote and REMOTE_OK.search(loc):
        return [], True
    return None


def level(title, hint=""):
    h = LEVEL_HINT.get((hint or "").lower())
    for k, rx in LEVEL_RX:
        if rx.search(title):
            return k
    return h or "mid"


def field(title):
    """Field id, or None for a posting that is not a tech job."""
    if NOT_TECH.search(title):
        return None
    for k, rx in FIELD_RX:
        if rx.search(title):
            return k
    return None


def classify(raw):
    """A site row for one raw posting, or None to leave it out."""
    p = place(raw["loc"], raw.get("remote"))
    if p is None:
        return None
    f = field(raw["title"])
    if f is None:
        return None
    where, remote = p
    return dict(title=raw["title"], url=raw["url"], loc=raw["loc"], cities=where,
                remote=remote, hybrid=bool(HYBRID.search(raw["loc"] + " " + raw["title"])),
                level=level(raw["title"], raw.get("level_hint")), field=f, posted=raw.get("posted", ""))
