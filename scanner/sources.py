"""Public job-board APIs. Each fetcher returns a list of raw postings, or None if the board did not answer.

Every endpoint here is the public JSON feed the platform itself offers for company career pages.
No login, no scraping of HTML.
"""
import datetime
import json
import time
import urllib.request

UA = {"User-Agent": "cluj-job-kit (+https://github.com/Cezart3/cluj-job-kit)"}


def get(url, timeout=25):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.load(r)
    except Exception:
        return None


def day(value):
    """Any board timestamp to YYYY-MM-DD, or ""."""
    if not value:
        return ""
    if isinstance(value, (int, float)):
        return str(datetime.datetime.fromtimestamp(value / 1000, datetime.timezone.utc).date())
    return str(value)[:10]


def job(title, loc, url, posted="", remote=False, level="", kind=""):
    return dict(title=(title or "").strip(), loc=(loc or "").strip(), url=url,
                posted=day(posted), remote=bool(remote), level_hint=level or "", type_hint=kind or "")


def greenhouse(slug):
    d = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    if d is None:
        return None
    return [job(j["title"], (j.get("location") or {}).get("name", ""), j["absolute_url"],
                j.get("first_published") or j.get("updated_at"))
            for j in d.get("jobs", [])]


def lever(slug):
    d = get(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if not isinstance(d, list):
        return None
    out = []
    for j in d:
        c = j.get("categories") or {}
        loc = " / ".join(c.get("allLocations") or [c.get("location", "")])
        out.append(job(j["text"], loc, j["hostedUrl"], j.get("createdAt"),
                       j.get("workplaceType") == "remote", kind=c.get("commitment", "")))
    return out


def ashby(slug):
    d = get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
    if d is None:
        return None
    out = []
    for j in d.get("jobs", []):
        locs = [j.get("location", "")] + [x.get("location", "") for x in j.get("secondaryLocations") or []]
        out.append(job(j["title"], " / ".join(x for x in locs if x), j["jobUrl"], j.get("publishedAt"),
                       j.get("isRemote"), kind=j.get("employmentType", "")))
    return out


def smartrecruiters(slug):
    # country=ro: SmartRecruiters filters server side, so only Romanian postings come back.
    out, offset = [], 0
    while True:
        d = get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings"
                f"?limit=100&offset={offset}&country=ro")
        if d is None:
            return None if offset == 0 else out
        for j in d.get("content", []):
            loc = j.get("location") or {}
            out.append(job(j["name"], loc.get("fullLocation") or loc.get("city", ""),
                           f"https://jobs.smartrecruiters.com/{slug}/{j['id']}", j.get("releasedDate"),
                           loc.get("remote"), (j.get("experienceLevel") or {}).get("id", ""),
                           (j.get("typeOfEmployment") or {}).get("label", "")))
        offset += 100
        if offset >= d.get("totalFound", 0):
            return out
        time.sleep(0.2)


def workable(slug):
    d = get(f"https://apply.workable.com/api/v1/widget/accounts/{slug}")
    if d is None:
        return None
    return [job(j["title"], " / ".join(", ".join(x for x in (l.get("city"), l.get("country")) if x)
                                      for l in j.get("locations") or [j]),
                j.get("url") or f"https://apply.workable.com/{slug}/j/{j['shortcode']}/",
                j.get("published_on"), j.get("telecommuting"), (j.get("experience") or "").lower(),
                j.get("employment_type", ""))
            for j in d.get("jobs", [])]


def recruitee(slug):
    d = get(f"https://{slug}.recruitee.com/api/offers/")
    if d is None:
        return None
    return [job(j["title"], j.get("location", ""), j.get("careers_url", ""), j.get("published_at"),
                j.get("remote"), j.get("experience_code", ""), j.get("employment_type_code", ""))
            for j in d.get("offers", [])]


SOURCES = dict(greenhouse=greenhouse, lever=lever, ashby=ashby,
               smartrecruiters=smartrecruiters, workable=workable, recruitee=recruitee)
