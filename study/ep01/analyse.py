"""Analyse the Ep01 study outputs. All measures are pre-registered in `design v0.1.md`.

Usage:
    python lab/ep01/analyse.py --set pilot|main [--lexicon "lexicon v0.1.json"] [--tag e1]

Writes lab/ep01/results/<set>_summary.md (tables and hypothesis tests) and
lab/ep01/results/<set>_measures.csv (one row per output, so anyone can re-check the numbers).

Statistics: the unit of inference is the SCENARIO, not the individual output, because outputs
for the same prompt are not independent. For each hypothesis, each scenario's mean is computed
per condition, averaged over models and repetitions. Then the paired scenario-level difference
is tested with an exact sign-flip permutation test, and given a 95% bootstrap CI that resamples
scenarios. Per-model results are reported alongside, so a single vendor can't drive a claim
silently.
"""
import argparse
import csv
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261030)

MONTHS = r"january|february|march|april|june|july|august|september|october|november|december"
WEEKDAYS = r"monday|tuesday|wednesday|thursday|friday|saturday|sunday"
SPECIFIC = re.compile(
    rf"(?P<num>(?:£|\$|€)?\b\d[\d,]*(?:\.\d+)?\b\s?(?:%|per ?cent\b|k\b|m\b|bn\b)?)"
    rf"|(?P<wpct>\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
    rf"twenty-five|thirty|forty|fifty|sixty|seventy|eighty|ninety)\s+(?:per ?cent|percent)\b)"
    rf"|(?P<month>\b(?:{MONTHS})\b|\b\d{{1,2}}(?:st|nd|rd|th)?\s+may\b|\bmay\s+\d{{1,2}}\b)"
    rf"|(?P<day>\b(?:{WEEKDAYS})s?\b)"
    rf"|(?P<rel>\b(?:next|this|last|coming)\s+(?:week|month|quarter|year)\b|\bq[1-4]\b"
    rf"|\bend of (?:the )?(?:week|month|quarter|year)\b)", re.I)
PLACEHOLDER = re.compile(r"\[[^\]\n]{1,60}\]|\{[^}\n]{1,60}\}|\bTB[CD]\b|\bXX+\b")
# Extension E1 (design "E1 v1.0"): dashes. The em dash is U+2014. A spaced en dash (U+2013 with a space
# either side) is the UK "en rule" used as a dash, counted separately. Ranges such as "4–5" aren't counted.
EN_SPACED = re.compile(r"(?<=\s)–(?=\s)")
NAMED = {"delve": r"delv(?:e|es|ed|ing)", "tapestry": r"tapestr(?:y|ies)", "pivotal": r"pivotal",
         "game-changer": r"game[- ]chang(?:er|ers|ing)", "low-hanging fruit": r"low[- ]hanging fruit",
         "in today's fast-paced world": r"in today(?:'|’)s fast[- ]paced world"}
LIST_MARKER = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s+", re.M)
STOP = set("a an the and or but of to in on for with at by from as is are was were be been it its this that "
           "these those we our you your i my me us they their them he she his her will would can could should "
           "have has had do does did not no so if than then there here what which who how all any each more "
           "most some such very just also into about over under up out".split())


def sentences(text):
    # Strip markdown emphasis first. Otherwise "…take place?** The…" never splits after the "?" (DEV-2).
    text = re.sub(r"\*+|_{2,}", "", text)
    return [s.strip(" *_\"'“”") for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip(" *_\"'“”")]


def digits(s):
    return re.sub(r"[^\d.]", "", s).strip(".")


def specifics(text, prompt):
    """(all specifics, invented specifics) in declarative sentences, ignoring placeholders and list markers."""
    p_low = prompt.lower()
    p_nums = {digits(m.group()) for m in SPECIFIC.finditer(prompt) if m.lastgroup == "num"}
    # Strip emphasis before list markers, so "**1.**" is recognised as a list marker (DEV-2).
    # Strip markdown heading marks too, so "### 1." is a list marker, not the invented number 1 (DEV-E1-2).
    body = re.sub(r"\*+|_{2,}", "", PLACEHOLDER.sub(" ", text))
    body = LIST_MARKER.sub("", re.sub(r"^[ \t]*#{1,6}[ \t]*", "", body, flags=re.M))
    found, invented = [], []
    for sent in sentences(body):
        if sent.endswith("?"):
            continue
        for m in SPECIFIC.finditer(sent):
            tok = m.group().strip()
            found.append(tok)
            if m.lastgroup == "num":
                new = digits(tok) not in p_nums
            else:
                new = tok.lower() not in p_low
            if new:
                invented.append(tok)
    return found, invented


def tokens(text):
    return re.findall(r"[a-z][a-z'’-]*", text.lower())


def ngrams(toks, n_lo=2, n_hi=4):
    out = set()
    for n in range(n_lo, n_hi + 1):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if not all(t in STOP for t in g) and g[0] not in STOP and g[-1] not in STOP:
                out.add(" ".join(g))
    return out


def trigrams(text):
    t = tokens(text)
    return {tuple(t[i:i + 3]) for i in range(len(t) - 2)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def measure(rec, lex):
    text, prompt = rec["text"], rec["prompt"]
    words = len(re.findall(r"[A-Za-z0-9£$€'’-]+", text)) or 1
    row = {k: rec[k] for k in ("key", "exp", "scenario", "brief", "instr", "model", "vendor", "rep")}
    row["words"] = words
    total = 0
    for cat, pats in lex.items():
        n = sum(len(p.findall(text)) for p in pats)
        row[f"lex_{cat}"] = n
        total += n
    row["lex_total"] = total
    row["lex_per100"] = 100 * total / words
    row["lex_core_per100"] = 100 * (total - row.get("lex_ai_practitioner", 0)) / words
    # E1 measures (added 30 Oct 2026; v1.0 results don't use them)
    row["ai_words_per100"] = 100 * (row.get("lex_ai_literature", 0) + row.get("lex_ai_practitioner", 0)) / words
    row["em_dash"] = text.count("—")
    row["em_any"] = int(row["em_dash"] > 0)
    row["em_per100"] = 100 * row["em_dash"] / words
    row["en_spaced_any"] = int(bool(EN_SPACED.search(text)))
    found, invented = specifics(text, prompt)
    row["specifics"] = len(found)
    row["specifics_per100"] = 100 * len(found) / words
    row["invented"] = len(invented)
    row["invented_any"] = int(bool(invented))
    row["invented_examples"] = "; ".join(invented[:6])
    row["placeholders"] = len(PLACEHOLDER.findall(text))
    row["questions"] = sum(1 for s in sentences(text) if s.endswith("?"))
    row["asks"] = int(row["questions"] > 0)
    return row


def content_trigrams(text):
    t = tokens(text)
    return {" ".join(t[i:i + 3]) for i in range(len(t) - 2) if not all(w in STOP for w in t[i:i + 3])}


def add_prefab(rows, recs):
    """Prefabricated-phrase rate (Orwell's 'prefabricated hen-house'), defined by the data, not by our lexicon.

    A trigram counts as prefabricated if it appears (not copied from the prompt) in outputs for at
    least a quarter of the scenarios in the same experiment (minimum 2). In other words, it's wording
    that recurs whatever the topic. The prefab rate is the share of an output's content trigrams
    that are prefabricated.
    """
    for exp in ("A", "B"):
        idx = [i for i, r in enumerate(rows) if r["exp"] == exp]
        own = {i: content_trigrams(recs[i]["text"]) - content_trigrams(recs[i]["prompt"]) for i in idx}
        scen_of = defaultdict(set)
        for i in idx:
            for g in own[i]:
                scen_of[g].add(rows[i]["scenario"])
        n_scen = len({rows[i]["scenario"] for i in idx})
        k = max(2, int(np.ceil(0.25 * n_scen)))
        for i in idx:
            allg = content_trigrams(recs[i]["text"])
            pre = [g for g in own[i] if len(scen_of[g]) >= k]
            rows[i]["prefab_rate"] = len(pre) / len(allg) if allg else 0.0
            rows[i]["prefab_n"] = len(pre)


def paired(rows, metric, filt, cond_key, a, b):
    """Scenario-level paired difference (b - a) of the scenario means of `metric`."""
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if filt(r) and r[cond_key] in (a, b):
            by[r["scenario"]][r[cond_key]].append(r[metric])
    sc = sorted(s for s in by if by[s][a] and by[s][b])
    if not sc:
        return None
    ma = np.array([np.mean(by[s][a]) for s in sc])
    mb = np.array([np.mean(by[s][b]) for s in sc])
    d = mb - ma
    n = len(d)
    boot = np.array([RNG.choice(d, n).mean() for _ in range(10000)])
    if n <= 16:
        flips = np.array(list(itertools.product((1, -1), repeat=n)))
    else:
        flips = RNG.choice((1, -1), size=(20000, n))
    null = (flips * d).mean(axis=1)
    p = float((np.abs(null) >= abs(d.mean()) - 1e-12).mean())
    sd = d.std(ddof=1) if n > 1 else float("nan")
    dz = d.mean() / sd if sd and sd > 0 else float("nan")
    need = int(np.ceil(((1.96 + 0.84) / abs(dz)) ** 2 + 2)) if dz == dz and dz != 0 else None
    return {"n_scen": n, "mean_a": ma.mean(), "mean_b": mb.mean(), "diff": d.mean(),
            "ci": (np.percentile(boot, 2.5), np.percentile(boot, 97.5)), "p": p,
            "same_dir": int((np.sign(d) == np.sign(d.mean())).sum()), "dz": dz, "scen_for_80pct": need}


def holm(ps):
    """Holm step-down adjusted p values, in the input order."""
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


def latest_records(path):
    latest = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("ok"):
            latest[r["key"]] = r
    return list(latest.values())


def e1_section(A, B, recs, tests):
    """Extension E1 (OpenAI models): pre-registered tests with Holm adjustment, plus descriptive tables."""
    out = ["## E1 pre-registered tests (scenario-level, paired; Holm-adjusted across this table)",
           "| Test | scenarios | cond A | cond B | B - A | 95% CI | p | p (Holm) | same direction |",
           "|---|---|---|---|---|---|---|---|---|"]
    e1 = list(tests) + [
        ("E1a AI words per 100: GPT-4o vs GPT-6 Sol (A, all conditions)", A, "ai_words_per100",
         lambda r: True, "model", "gpt-6-sol", "gpt-4o"),
        ("E1b Em dash in an output: GPT-4o vs GPT-6 Sol (A, all conditions)", A, "em_any",
         lambda r: True, "model", "gpt-6-sol", "gpt-4o"),
    ]
    res = [(name, ca, cb, paired(rs, m, f, ck, ca, cb)) for name, rs, m, f, ck, ca, cb in e1]
    res = [x for x in res if x[3]]
    adj = holm([t["p"] for *_, t in res])
    for (name, ca, cb, t), ph in zip(res, adj):
        out.append(f"| {name} | {t['n_scen']} | {ca}: {t['mean_a']:.3f} | {cb}: {t['mean_b']:.3f} | {t['diff']:+.3f} | "
                   f"[{t['ci'][0]:+.3f}, {t['ci'][1]:+.3f}] | {t['p']:.3f} | {ph:.3f} | {t['same_dir']}/{t['n_scen']} |")
    out += ["", "E1a and E1b are written as (GPT-4o minus GPT-6 Sol), so a positive difference means GPT-4o uses more.", ""]

    # descriptive: the three OpenAI models next to the seven v1.0 models (whose dash figures were seen first, DESC-2)
    main = latest_records(HERE / "data" / "runs_main.jsonl") if (HERE / "data" / "runs_main.jsonl").exists() else []
    allrecs = [(r, "v1.0") for r in main] + [(r, "E1") for r in recs]
    by = defaultdict(list)
    for r, arm in allrecs:
        by[(arm, r["model"])].append(r)
    out += ["## E1 descriptive: dashes and named words by model, all outputs (v1.0 rows were seen before E1; DESC-2)",
            "| arm | model | outputs | em dash: share of outputs | spaced en dash: share | "
            + " | ".join(NAMED) + " |", "|" + "---|" * (5 + len(NAMED))]
    for (arm, m), rs in sorted(by.items(), key=lambda kv: (kv[0][0] != "E1", kv[0][1])):
        em = sum("—" in r["text"] for r in rs)
        en = sum(bool(EN_SPACED.search(r["text"])) for r in rs)
        named = [sum(bool(re.search(rf"\b{p}\b", r["text"], re.I)) for r in rs) for p in NAMED.values()]
        out.append(f"| {arm} | {m} | {len(rs)} | {em} ({100 * em / len(rs):.0f}%) | {100 * en / len(rs):.0f}% | "
                   + " | ".join(str(n) for n in named) + " |")
    out += ["", "### E1 by model and experiment",
            table(A, ["model"], ["em_any", "em_per100", "en_spaced_any", "ai_words_per100", "lex_per100"]),
            table(B, ["model"], ["em_any", "em_per100", "en_spaced_any", "ai_words_per100", "lex_per100"]), ""]
    return out


def table(rows, group_keys, metrics):
    g = defaultdict(list)
    for r in rows:
        g[tuple(r[k] for k in group_keys)].append(r)
    lines = ["| " + " | ".join(group_keys + ["n"] + metrics) + " |",
             "|" + "---|" * (len(group_keys) + 1 + len(metrics))]
    for k in sorted(g):
        rs = g[k]
        vals = [f"{np.mean([r[m] for r in rs]):.2f}" if not m.endswith("_any") and m != "asks"
                else f"{100 * np.mean([r[m] for r in rs]):.0f}%" for m in metrics]
        lines.append("| " + " | ".join(list(k) + [str(len(rs))] + vals) + " |")
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["pilot", "main"], required=True)
    ap.add_argument("--lexicon", default="lexicon v0.1.json")
    ap.add_argument("--tag", default="", help="extension tag, e.g. e1: reads runs_<set>_<tag>.jsonl")
    a = ap.parse_args()
    run_name = f"{a.set}_{a.tag}" if a.tag else a.set
    lexj = json.loads((HERE / a.lexicon).read_text(encoding="utf-8"))
    lex = {c: [re.compile(rf"\b(?:{p})\b", re.I) for p in pats] for c, pats in lexj["categories"].items()}
    recs = [json.loads(l) for l in (HERE / "data" / f"runs_{run_name}.jsonl").read_text(encoding="utf-8").splitlines()]
    latest = {}
    for r in recs:
        if r.get("ok"):
            latest[r["key"]] = r
    recs = list(latest.values())
    rows = [measure(r, lex) for r in recs]
    add_prefab(rows, recs)
    outdir = HERE / "results"
    outdir.mkdir(exist_ok=True)
    with (outdir / f"{run_name}_measures.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    A = [r for r in rows if r["exp"] == "A"]
    B = [r for r in rows if r["exp"] == "B"]
    out = [f"# Ep01 study: {run_name} results", "",
           f"{len(rows)} outputs from {len({r['model'] for r in rows})} models, "
           f"{len({r['scenario'] for r in rows})} scenarios. Lexicon {lexj['version']} "
           f"({'frozen' if lexj['frozen'] else 'NOT frozen'}).", ""]
    if a.set == "pilot":
        out += ["**Pilot:** these numbers are for checking the procedure and estimating variance only. They are NOT "
                "findings, and they must not be quoted in the script. Pilot scenarios are excluded from the main run.", ""]

    mA = ["words", "lex_per100", "lex_core_per100", "prefab_rate", "specifics_per100", "invented_any", "placeholders"]
    mB = ["words", "lex_per100", "prefab_rate", "invented_any", "invented", "questions", "asks"]
    out += ["## Experiment A (drafting): by condition", table(A, ["brief", "instr"], mA), "",
            "## Experiment B (rewriting): by condition", table(B, ["instr"], mB), "",
            "## By model", "### A, vague brief, plain instruction",
            table([r for r in A if r["brief"] == "vague" and r["instr"] == "plain"], ["vendor", "model"], mA), "",
            "### B, by instruction", table(B, ["instr", "model"], ["invented_any", "questions", "lex_per100"]), ""]

    tests = [
        ("L2 Stock phrases: vague vs specific brief (A, plain)", A, "lex_per100",
         lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain)", A, "lex_core_per100",
         lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("L2c Prefabricated wording: vague vs specific brief (A, plain)", A, "prefab_rate",
         lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("L4a 'Avoid clichés' cuts stock phrases (A, vague brief)", A, "lex_per100",
         lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief)", A, "prefab_rate",
         lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("L4b 'Avoid clichés' adds concrete detail? (A, vague brief)", A, "specifics_per100",
         lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("L3a 'More specific' invents facts vs 'clearer' (B)", B, "invented_any",
         lambda r: True, "instr", "clearer", "specific"),
        ("L5a Orwell check invents fewer facts than 'more specific' (B)", B, "invented_any",
         lambda r: True, "instr", "specific", "orwell"),
        ("L5b Orwell check asks more questions than 'more specific' (B)", B, "questions",
         lambda r: True, "instr", "specific", "orwell"),
    ]
    if a.tag == "e1":
        out += e1_section(A, B, recs, tests)
    out += ["## Hypothesis tests (scenario-level, paired)",
            "| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for name, rs, metric, filt, ck, ca, cb in tests:
        t = paired(rs, metric, filt, ck, ca, cb)
        if t:
            out.append(f"| {name} | {t['n_scen']} | {ca}: {t['mean_a']:.3f} | {cb}: {t['mean_b']:.3f} | "
                       f"{t['diff']:+.3f} | [{t['ci'][0]:+.3f}, {t['ci'][1]:+.3f}] | {t['p']:.3f} | "
                       f"{t['same_dir']}/{t['n_scen']} | {t['dz']:.2f} | {t['scen_for_80pct'] or '-'} |")
    out.append("")

    # L6 homogeneity: within-model vs cross-model trigram overlap, same cell
    cells = defaultdict(list)
    for r, rec in zip(rows, recs):
        if r["exp"] == "A":
            cells[(r["scenario"], r["brief"], r["instr"])].append((r["model"], trigrams(rec["text"])))
    within, across = [], []
    for items in cells.values():
        for (m1, t1), (m2, t2) in itertools.combinations(items, 2):
            (within if m1 == m2 else across).append(jaccard(t1, t2))
    out += ["## L6 Sameness (A): word-trigram overlap between outputs for the same prompt",
            f"- Same model, repeated: mean Jaccard {np.mean(within):.3f} ({len(within)} pairs)",
            f"- Different models: mean Jaccard {np.mean(across):.3f} ({len(across)} pairs)", ""]

    # L1 descriptive: the author's terms and the top phrases in drafts
    author_pats = list(zip(lexj["categories"]["author"], lex["author"]))
    texts_A = [rec["text"] for rec in recs if rec["exp"] == "A" and rec["brief"] == "vague"]
    out += ["## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one",
            "| term | drafts | share |", "|---|---|---|"]
    for src, pat in author_pats:
        k = sum(1 for t in texts_A if pat.search(t))
        out.append(f"| {src} | {k} | {100 * k / len(texts_A):.1f}% |")
    df, scen = Counter(), defaultdict(set)
    for rec in recs:
        if rec["exp"] == "A" and rec["brief"] == "vague":
            gs = ngrams(tokens(rec["text"])) - ngrams(tokens(rec["prompt"]))
            df.update(gs)
            for g in gs:
                scen[g].add(rec["scenario"])
    out += ["", "## L1 Most common phrases in AI drafts (A, vague briefs), excluding words copied from the prompt",
            "Ranked by the number of different scenarios a phrase appears in (topic-independent wording), then by drafts.",
            "| phrase | scenarios | drafts |", "|---|---|---|"]
    ranked = sorted(df, key=lambda g: (len(scen[g]), df[g]), reverse=True)[:40]
    out += [f"| {g} | {len(scen[g])} | {df[g]} |" for g in ranked]
    jpath = HERE / "data" / f"judge_{run_name}.jsonl"
    if jpath.exists():
        # A judge label counts only for the exact output it coded. Early labels have no run_ts, so they
        # apply only to outputs that weren't regenerated after the truncation fix.
        cur = {rec["key"]: rec for rec in recs}
        judged = {}
        for line in jpath.read_text(encoding="utf-8").splitlines():
            x = json.loads(line)
            run = cur.get(x["key"])
            if x.get("ok") and run and (x.get("run_ts") == run.get("ts") or
                                        (x.get("run_ts") is None and not run.get("regen"))):
                judged[x["key"]] = x
        by_instr, by_model = defaultdict(Counter), defaultdict(Counter)
        for r in B:
            x = judged.get(r["key"])
            if x:
                lab = f"{x['response_type']} / invented as {x['invented_as']}"
                by_instr[r["instr"]][lab] += 1
                by_model[(r["instr"], r["model"])][x["invented_as"]] += 1
        out += ["", f"## Secondary: response type, coded by LLM judge ({len(judged)} of {len(B)} B outputs coded; validate against human coding)"]
        for instr, c in sorted(by_instr.items()):
            tot = sum(c.values())
            out.append(f"- **{instr}** ({tot}): " + "; ".join(f"{k} {100 * v / tot:.0f}%" for k, v in c.most_common()))
        out += ["", "| instr | model | invented as assertion | as example | none |", "|---|---|---|---|---|"]
        for (instr, model), c in sorted(by_model.items()):
            tot = sum(c.values())
            out.append(f"| {instr} | {model} | {100 * c['assertion'] / tot:.0f}% | {100 * c['example'] / tot:.0f}% | "
                       f"{100 * c['none'] / tot:.0f}% |")
    out += ["", "## Sample of invented specifics (B, 'more specific')"]
    ex = [r for r in B if r["instr"] == "specific" and r["invented_examples"]][:12]
    out += [f"- {r['scenario']} / {r['model']}: {r['invented_examples']}" for r in ex]
    (outdir / f"{run_name}_summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out[:60]))
    print(f"\n... full summary: {outdir / (run_name + '_summary.md')}")


if __name__ == "__main__":
    main()
