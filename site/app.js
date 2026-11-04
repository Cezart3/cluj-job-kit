"use strict";

const REPO = "https://github.com/Cezart3/cluj-job-kit";
const PAGE = 60;

const T = {
  ro: {
    eyebrow: "Joburi tech pentru studenți · actualizat zilnic",
    headline: "posturi deschise",
    sub: "Din board-urile publice ale firmelor. Ultima actualizare:",
    f_city: "Oraș", f_level: "Nivel", f_field: "Domeniu",
    search: "Caută după titlu sau firmă", search_ph: "Caută: python, Bosch, react…",
    fresh: "Doar din ultimele 7 zile", reset: "Șterge filtrele",
    col_day: "Văzut", col_job: "Post", col_city: "Oraș", col_level: "Nivel",
    apply: "Aplică", new: "NOU", today: "azi", yesterday: "ieri",
    more: n => `Arată încă ${n}`,
    empty: "Niciun post pentru filtrele alese. Scoate un filtru sau caută pe site-urile de mai jos.",
    failed: "Datele nu s-au încărcat. Reîncarcă pagina.",
    elsewhere_h: "Caută și aici",
    elsewhere_p: "Site-urile astea nu au API public, așa că nu le citim automat. Linkurile deschid căutarea gata filtrată.",
    how_h: "Cum funcționează",
    how_p: "În fiecare dimineață un script citește board-urile publice (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee) și păstrează joburile tech din România sau remote din Europa. Linkul „Aplică” duce direct la anunțul firmei.",
    cv_h: "CV adaptat pe job",
    cv_p: `Repo-ul are și un kit pentru CV: îți construiește CV-uri pe focus (backend, frontend, data) din aceleași fapte și îți spune dacă merită să aplici la un job. Merge pe Windows, macOS și Linux. <a href="${REPO}/tree/main/kit">Instrucțiuni</a>.`,
    add_h: "Lipsește o firmă?",
    add_p: `Adaugă board-ul ei în <code>scanner/boards-ro.txt</code> printr-un pull request, sau <a href="${REPO}/issues/new?title=Firm%C4%83%20nou%C4%83">deschide un issue</a> cu linkul paginii de cariere.`,
    credits: `Făcut de un student, pentru studenți. Cod open source (MIT) pe <a href="${REPO}">GitHub</a>. Construit pe <a href="https://github.com/jpita/job-hunt-kit-template">job-hunt-kit-template</a> de Gabriel Pita. Joburile aparțin firmelor care le publică; verifică mereu anunțul original.`,
    cities: { all: "Toată țara", cluj: "Cluj-Napoca", bucuresti: "București", timisoara: "Timișoara", iasi: "Iași", brasov: "Brașov", sibiu: "Sibiu", oradea: "Oradea", craiova: "Craiova", constanta: "Constanța", "targu-mures": "Târgu Mureș", arad: "Arad", pitesti: "Pitești", romania: "România (alt oraș)", remote: "Remote" },
    levels: { intern: "Internship", junior: "Junior", mid: "Mid", senior: "Senior" },
    fields: { backend: "Backend", frontend: "Frontend", fullstack: "Full-stack", mobile: "Mobile", data: "Data / AI", devops: "DevOps / Cloud", qa: "QA / Test", embedded: "Embedded", security: "Securitate", software: "Software (general)" },
  },
  en: {
    eyebrow: "Tech jobs for students · updated daily",
    headline: "open positions",
    sub: "From companies' public job boards. Last update:",
    f_city: "City", f_level: "Level", f_field: "Field",
    search: "Search by title or company", search_ph: "Search: python, Bosch, react…",
    fresh: "Only from the last 7 days", reset: "Clear filters",
    col_day: "Seen", col_job: "Position", col_city: "City", col_level: "Level",
    apply: "Apply", new: "NEW", today: "today", yesterday: "yesterday",
    more: n => `Show ${n} more`,
    empty: "No positions match these filters. Remove a filter or search the sites below.",
    failed: "The data did not load. Reload the page.",
    elsewhere_h: "Also search here",
    elsewhere_p: "These sites have no public API, so they are not read automatically. The links open a search with the filters already set.",
    how_h: "How it works",
    how_p: "Every morning a script reads public job boards (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee) and keeps tech jobs in Romania or remote in Europe. The Apply link goes straight to the company's posting.",
    cv_h: "A CV tailored to the job",
    cv_p: `The repo also has a CV kit: it builds focus CVs (backend, frontend, data) from one set of facts and tells you whether a job is worth applying to. Works on Windows, macOS and Linux. <a href="${REPO}/tree/main/kit">Instructions</a>.`,
    add_h: "Missing a company?",
    add_p: `Add its board to <code>scanner/boards-ro.txt</code> with a pull request, or <a href="${REPO}/issues/new?title=New%20company">open an issue</a> with its careers page link.`,
    credits: `Made by a student, for students. Open source (MIT) on <a href="${REPO}">GitHub</a>. Built on <a href="https://github.com/jpita/job-hunt-kit-template">job-hunt-kit-template</a> by Gabriel Pita. Jobs belong to the companies that post them; always check the original posting.`,
    cities: { all: "All of Romania", cluj: "Cluj-Napoca", bucuresti: "Bucharest", timisoara: "Timișoara", iasi: "Iași", brasov: "Brașov", sibiu: "Sibiu", oradea: "Oradea", craiova: "Craiova", constanta: "Constanța", "targu-mures": "Târgu Mureș", arad: "Arad", pitesti: "Pitești", romania: "Romania (other city)", remote: "Remote" },
    levels: { intern: "Internship", junior: "Junior", mid: "Mid", senior: "Senior" },
    fields: { backend: "Backend", frontend: "Frontend", fullstack: "Full-stack", mobile: "Mobile", data: "Data / AI", devops: "DevOps / Cloud", qa: "QA / Test", embedded: "Embedded", security: "Security", software: "Software (general)" },
  },
};

// Searches on sites with no API, per city. {q} is the search words.
const ELSEWHERE = [
  ["LinkedIn", c => `https://www.linkedin.com/jobs/search/?keywords=software&location=${encodeURIComponent((c ? CITY_EN[c] + ", " : "") + "Romania")}&f_E=1%2C2&f_TPR=r604800`],
  ["Hipo", c => `https://www.hipo.ro/locuri-de-munca/cautajob/Internship,IT-Software/${c ? HIPO[c] || "Toate-Orasele" : "Toate-Orasele"}/`],
  ["BestJobs", c => `https://www.bestjobs.eu/locuri-de-munca${c ? "-in-" + SLUG[c] : ""}/internship`],
  ["eJobs", c => `https://www.ejobs.ro/locuri-de-munca/${c ? SLUG[c] + "/" : ""}internship`],
  ["Indeed", c => `https://ro.indeed.com/jobs?q=software+intern&l=${encodeURIComponent(c ? CITY_EN[c] : "Romania")}`],
];
const CITY_EN = { cluj: "Cluj-Napoca", bucuresti: "Bucharest", timisoara: "Timisoara", iasi: "Iasi", brasov: "Brasov", sibiu: "Sibiu", oradea: "Oradea", craiova: "Craiova", constanta: "Constanta", "targu-mures": "Targu Mures", arad: "Arad", pitesti: "Pitesti" };
const SLUG = { cluj: "cluj-napoca", bucuresti: "bucuresti", timisoara: "timisoara", iasi: "iasi", brasov: "brasov", sibiu: "sibiu", oradea: "oradea", craiova: "craiova", constanta: "constanta", "targu-mures": "targu-mures", arad: "arad", pitesti: "pitesti" };
const HIPO = { cluj: "Cluj-Napoca", bucuresti: "BUCURESTI", timisoara: "Timisoara", iasi: "Iasi", brasov: "Brasov", sibiu: "Sibiu", oradea: "Oradea", craiova: "Craiova", constanta: "Constanta", "targu-mures": "Targu-Mures", arad: "Arad", pitesti: "Pitesti" };

const MAIN_CITIES = ["cluj", "bucuresti", "timisoara", "iasi", "brasov", "remote"];
const LEVELS = ["intern", "junior", "mid", "senior"];

const $ = s => document.querySelector(s);
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
};

let DATA = { jobs: [] };
let lang = new URLSearchParams(location.search).get("lang") || store.get("lang") || (navigator.language || "ro").slice(0, 2);
if (!T[lang]) lang = "ro";
let shown = PAGE;

// Filters live in the URL hash, so a filtered view can be shared as a link.
function readHash() {
  const h = new URLSearchParams(location.hash.slice(1));
  const list = k => (h.get(k) || "").split(",").filter(Boolean);
  return { city: list("city"), level: list("level"), field: list("field"), q: h.get("q") || "", fresh: h.get("fresh") === "1" };
}
let F = readHash();

function writeHash() {
  const h = new URLSearchParams();
  for (const k of ["city", "level", "field"]) if (F[k].length) h.set(k, F[k].join(","));
  if (F.q) h.set("q", F.q);
  if (F.fresh) h.set("fresh", "1");
  history.replaceState(null, "", "#" + h.toString());
}

function jobCities(j) { return j.cities.length ? j.cities : []; }

function matches(j, skip) {
  const t = Date.now() - 7 * 864e5;
  if (skip !== "city" && F.city.length && !F.city.some(c => c === "remote" ? j.remote : j.cities.includes(c))) return false;
  if (skip !== "level" && F.level.length && !F.level.includes(j.level)) return false;
  if (skip !== "field" && F.field.length && !F.field.includes(j.field)) return false;
  if (F.fresh && new Date(j.first_seen).getTime() < t) return false;
  if (F.q) {
    const q = F.q.toLowerCase();
    if (!(j.title + " " + j.company).toLowerCase().includes(q)) return false;
  }
  return true;
}

function count(key, value) {
  return DATA.jobs.filter(j => matches(j, key) && (
    key === "city" ? (value === "remote" ? j.remote : jobCities(j).includes(value)) :
    j[key] === value)).length;
}

function chips(el, key, values, names) {
  el.replaceChildren(...values.map(v => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "chip";
    b.setAttribute("aria-pressed", F[key].includes(v));
    b.append(names[v] || v);
    const s = document.createElement("small"); s.textContent = count(key, v); b.append(s);
    b.onclick = () => {
      F[key] = F[key].includes(v) ? F[key].filter(x => x !== v) : [...F[key], v];
      shown = PAGE; render();
    };
    return b;
  }));
}

function dayLabel(d) {
  const t = T[lang];
  const today = new Date().toISOString().slice(0, 10);
  const y = new Date(Date.now() - 864e5).toISOString().slice(0, 10);
  if (d === today) return t.today;
  if (d === y) return t.yesterday;
  return new Date(d + "T12:00:00").toLocaleDateString(lang === "ro" ? "ro-RO" : "en-GB", { day: "numeric", month: "short" });
}

function row(j, i) {
  const t = T[lang];
  const li = document.createElement("li");
  li.style.setProperty("--i", Math.min(i, 20));
  const fresh = Date.now() - new Date(j.first_seen + "T00:00:00").getTime() < 2 * 864e5;

  const job = document.createElement("div"); job.className = "job";
  const b = document.createElement("b"); b.textContent = j.title;
  const s = document.createElement("span"); s.textContent = j.company + (j.hybrid ? " · hybrid" : "");
  job.append(b, s);

  const meta = document.createElement("div"); meta.className = "meta";
  const day = document.createElement("span"); day.className = "day";
  if (fresh) { const n = document.createElement("span"); n.className = "new"; n.textContent = t.new; day.append(n); }
  else day.textContent = dayLabel(j.first_seen);
  const city = document.createElement("span"); city.className = "city";
  city.textContent = [...jobCities(j).map(c => t.cities[c] || c), ...(j.remote ? [t.cities.remote] : [])].join(", ");
  const lvl = document.createElement("span"); lvl.className = "lvl"; lvl.dataset.l = j.level; lvl.textContent = t.levels[j.level];
  meta.append(day, city, lvl);

  const a = document.createElement("a"); a.className = "go"; a.href = j.url; a.target = "_blank"; a.rel = "noopener";
  a.textContent = t.apply + " →";
  a.setAttribute("aria-label", `${t.apply}: ${j.title}, ${j.company}`);

  li.append(job, meta, a);
  return li;
}

function render() {
  const t = T[lang];
  writeHash();
  const cityKeys = [...MAIN_CITIES, ...Object.keys(t.cities).filter(c => !MAIN_CITIES.includes(c) && c !== "all" && count("city", c) > 0)];
  chips($("#f-city"), "city", cityKeys, t.cities);
  chips($("#f-level"), "level", LEVELS, t.levels);
  chips($("#f-field"), "field", Object.keys(t.fields), t.fields);

  // Student levels first, then newest first.
  const list = DATA.jobs.filter(j => matches(j)).sort((a, b) => LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level) || b.first_seen.localeCompare(a.first_seen));
  $("#count").textContent = list.length;
  $("#list").replaceChildren(...list.slice(0, shown).map(row));
  $("#empty").hidden = list.length > 0;
  $("#empty").textContent = t.empty;
  const rest = list.length - shown;
  $("#more").hidden = rest <= 0;
  $("#more").textContent = t.more(Math.min(rest, PAGE));

  const one = F.city.length === 1 && F.city[0] !== "remote" ? F.city[0] : "";
  $("#links").replaceChildren(...ELSEWHERE.map(([name, url]) => {
    const li = document.createElement("li"), a = document.createElement("a");
    a.href = url(one); a.target = "_blank"; a.rel = "noopener";
    a.textContent = `${name}: ${one ? t.cities[one] : t.cities.all} ↗`;
    li.append(a); return li;
  }));
}

function translate() {
  const t = T[lang];
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t[el.dataset.i18n]; });
  document.querySelectorAll("[data-i18n-html]").forEach(el => { el.innerHTML = t[el.dataset.i18nHtml]; });
  $("#q").placeholder = t.search_ph;
  document.querySelectorAll(".lang button").forEach(b => b.setAttribute("aria-pressed", b.dataset.lang === lang));
  if (DATA.updated) $("#updated").textContent = new Date(DATA.updated).toLocaleString(lang === "ro" ? "ro-RO" : "en-GB", { dateStyle: "medium", timeStyle: "short" });
  render();
}

document.querySelectorAll(".lang button").forEach(b => b.onclick = () => { lang = b.dataset.lang; store.set("lang", lang); translate(); });
$("#q").value = F.q;
$("#fresh").checked = F.fresh;
let typing;
$("#q").oninput = e => { clearTimeout(typing); typing = setTimeout(() => { F.q = e.target.value.trim(); shown = PAGE; render(); }, 150); };
$("#fresh").onchange = e => { F.fresh = e.target.checked; shown = PAGE; render(); };
$("#reset").onclick = () => { F = { city: [], level: [], field: [], q: "", fresh: false }; $("#q").value = ""; $("#fresh").checked = false; shown = PAGE; render(); };
$("#more").onclick = () => { shown += PAGE; render(); };
window.addEventListener("hashchange", () => { F = readHash(); render(); });

translate();
fetch("data/jobs.json", { cache: "no-cache" })
  .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
  .then(d => { DATA = d; translate(); })
  .catch(() => { $("#empty").hidden = false; $("#empty").textContent = T[lang].failed; $("#count").textContent = "—"; });
