"""Compute the Ep01 script's study numbers from the main-run measures, so no figure is typed by hand.

    python lab/ep01/script_numbers.py > lab/ep01/results/script_numbers_v0.9.json

Run analyse.py --set main first. Values are written for spoken narration and for NOTE/SOURCE lines.
v0.7 numbers: results/script_numbers.json. v0.8 added the DESC-1 keys (TELL_*, MILD_*, LEX_TERMS_*): descriptive
counts of named phrases, for the script that drops the author's own terms (D35). The phrases shown on screen were
chosen after seeing the data, so every frozen-lexicon term's count is reported too (LEX_TERMS_*).
v0.9 (after the v0.8 fact-check):
- TELL_* adds "pivotal".
- MILD_* uses the lexicon's own patterns, and the exact phrase "excited to announce".
- LEX_TERMS_* is split into drafts (A) and rewrites (B); for B it gives how many of the hits were already in the input.
- L2_FULL gives the full-list version of L2.
- JUDGE_DETAIL's label is updated for VAL-1.
v1.0 (E1, design E1 v1.0): `python lab/ep01/analyse.py --set main --tag e1` first, then
    python lab/ep01/script_numbers.py > lab/ep01/results/script_numbers_v1.0.json
This adds the E1_* and ALL_* keys: the three OpenAI models, and all ten models together.
v1.1: the same keys after the DEV-E1-2 fix (markdown "### 1." headings were counted as invented numbers in
nine GPT-4o Orwell-check replies). Write it to results/script_numbers_v1.1.json; v1.0 is kept as it was.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analyse  # noqa: E402

WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def in_ten(p):
    if p >= 0.995:
        return "every single time"
    n = round(p * 10)
    return "nearly nine times in ten" if 0.85 <= p < 0.9 else f"about {WORDS.get(n, n)} times in ten"


def per_cent_words(p):
    n = int(round(p * 100 / 5) * 5)
    tens = {10: "ten", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
            80: "eighty", 90: "ninety"}
    return f"{tens.get(n, n)} per cent"


def fraction_words(p):
    if 0.5 <= p < 0.6:
        return "more than half"
    if 0.45 <= p < 0.5:
        return "nearly half"
    return f"about {WORDS.get(round(p * 10), round(p * 10))} in ten"


def small_words(p):
    if p < 0.035:
        return "almost never"
    if p < 0.075:
        return "about one time in twenty"
    if p < 0.15:
        return "about one time in ten"
    return f"in about {round(p * 100)}% of replies"


def e1_numbers(latest_v1, cnt, tells):
    """E1 keys (design E1 v1.0): the three OpenAI models, and the ten models together. Empty until the E1 run exists."""
    mpath, rpath = HERE / "results" / "main_e1_measures.csv", HERE / "data" / "runs_main_e1.jsonl"
    if not (mpath.exists() and rpath.exists()):
        return {}
    v = {}
    rows = list(csv.DictReader(mpath.open(encoding="utf-8")))
    for r in rows:
        for k in ("words", "lex_per100", "lex_core_per100", "invented_any", "questions", "asks", "ai_words_per100",
                  "em_any", "em_per100", "en_spaced_any", "prefab_rate", "specifics_per100"):
            r[k] = float(r[k])
        r["invented_per100"] = 100 * float(r["invented"]) / r["words"]
    A = [r for r in rows if r["exp"] == "A"]
    B = [r for r in rows if r["exp"] == "B"]
    mean = lambda rs: sum(rs) / len(rs)
    e1 = {}
    for line in rpath.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("ok"):
            e1[rec["key"]] = rec
    v["E1_N"] = f"{len(e1):,}"
    v["E1_STOPS"] = ", ".join(f"{s}: {n}" for s, n in sorted(
        {s: sum(1 for x in e1.values() if x.get('stop_reason') == s) for s in {x.get('stop_reason') for x in e1.values()}}.items()))
    v["E1_SNAPSHOTS"] = ", ".join(sorted({x["model_id"] for x in e1.values()}))
    allrecs = list(latest_v1.values()) + list(e1.values())
    v["ALL_N"] = f"{len(allrecs):,}"
    v["ALL_TELLS"] = "; ".join(f"'{k}' {cnt(p, [x['text'] for x in allrecs])} (GPT models {cnt(p, [x['text'] for x in e1.values()])})"
                               for k, p in tells.items()) + f" of {len(allrecs):,} outputs from 10 models"
    by = defaultdict(list)
    for x in allrecs:
        by[x["model"]].append(x)
    v["ALL_EM_BY_MODEL"] = "; ".join(f"{m} {sum('—' in x['text'] for x in xs)} of {len(xs)} "
                                     f"({100 * sum('—' in x['text'] for x in xs) / len(xs):.0f}%)" for m, xs in sorted(by.items()))
    gpt = [m for m in by if m.startswith("gpt")]
    v["GPT_EM_ANY"] = (f"{sum('—' in x['text'] for m in gpt for x in by[m])} of {sum(len(by[m]) for m in gpt)} GPT outputs "
                       f"contain an em dash")
    # the pre-registered E1 table, with Holm across it (same tests as analyse.py --tag e1)
    tests = [
        ("R-L2", A, "lex_per100", lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("R-L2b", A, "lex_core_per100", lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("R-L2c", A, "prefab_rate", lambda r: r["instr"] == "plain", "brief", "specific", "vague"),
        ("R-L4a", A, "lex_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("R-L4c", A, "prefab_rate", lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("R-L4b", A, "specifics_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid"),
        ("R-L3a", B, "invented_any", lambda r: True, "instr", "clearer", "specific"),
        ("R-L5a", B, "invented_any", lambda r: True, "instr", "specific", "orwell"),
        ("R-L5b", B, "questions", lambda r: True, "instr", "specific", "orwell"),
        ("E1a", A, "ai_words_per100", lambda r: True, "model", "gpt-6-sol", "gpt-4o"),
        ("E1b", A, "em_any", lambda r: True, "model", "gpt-6-sol", "gpt-4o"),
    ]
    res = [(n, analyse.paired(rs, m, f, ck, ca, cb)) for n, rs, m, f, ck, ca, cb in tests]
    adj = analyse.holm([t["p"] for _, t in res])
    for (n, t), ph in zip(res, adj):
        ok = ph < 0.05 and (t["ci"][0] > 0 or t["ci"][1] < 0)
        v[f"E1_{n.replace('-', '_')}"] = (f"{t['mean_a']:.3f} -> {t['mean_b']:.3f} (diff {t['diff']:+.3f}, 95% CI "
                                          f"[{t['ci'][0]:+.3f}, {t['ci'][1]:+.3f}]), same direction in {t['same_dir']} of "
                                          f"{t['n_scen']}, p {t['p']:.4f}, Holm p {ph:.4f}: {'SUPPORTED' if ok else 'not supported'}")
    byB = defaultdict(list)
    for r in B:
        byB[(r["instr"], r["model"])].append(r)
    v["E1_B_BY_MODEL"] = "; ".join(
        f"{m}: specific invents {100 * mean([r['invented_any'] for r in byB[('specific', m)]]):.0f}%, clearer "
        f"{100 * mean([r['invented_any'] for r in byB[('clearer', m)]]):.0f}%, Orwell check asks "
        f"{100 * mean([r['asks'] for r in byB[('orwell', m)]]):.0f}% and invents "
        f"{100 * mean([r['invented_any'] for r in byB[('orwell', m)]]):.0f}%" for m in sorted({r['model'] for r in B}))
    spec = mean([r["invented_any"] for r in B if r["instr"] == "specific"])
    v["E1_L3_POOLED"] = f"{100 * spec:.0f}% of GPT 'more specific' rewrites added an invented number or date"

    # ALL10_*: the seven v1.0 models and the three E1 models together, for narration that says "ten models".
    # Descriptive: each arm's own pre-registered tests are in E1_* and the v1.0 keys. Every model has the same n.
    v1 = list(csv.DictReader((HERE / "results" / "main_measures.csv").open(encoding="utf-8")))
    allrows = []
    for r in v1 + list(csv.DictReader(mpath.open(encoding="utf-8"))):
        for k in ("words", "lex_per100", "invented_any", "invented", "asks", "questions"):
            r[k] = float(r[k])
        r["invented_per100"] = 100 * r["invented"] / r["words"]
        allrows.append(r)
    A10 = [r for r in allrows if r["exp"] == "A"]
    B10 = [r for r in allrows if r["exp"] == "B"]
    share = lambda rs, k: mean([r[k] for r in rs])
    sp = [r for r in B10 if r["instr"] == "specific"]
    cl = [r for r in B10 if r["instr"] == "clearer"]
    ow = [r for r in B10 if r["instr"] == "orwell"]
    t = analyse.paired(B10, "invented_any", lambda r: True, "instr", "clearer", "specific")
    v["ALL10_L3"] = (f"'more specific' {100 * share(sp, 'invented_any'):.0f}% ({int(sum(r['invented_any'] for r in sp))} of {len(sp)}) "
                     f"vs 'clearer' {100 * share(cl, 'invented_any'):.0f}% ({int(sum(r['invented_any'] for r in cl))} of {len(cl)}) "
                     f"added an invented number, date or deadline; higher in {t['same_dir']} of {t['n_scen']} tasks")
    v["ALL10_L5"] = (f"Orwell check: asked at least one question in {int(sum(r['asks'] for r in ow))} of {len(ow)}; "
                     f"invented a number or date in {int(sum(r['invented_any'] for r in ow))} of {len(ow)} "
                     f"({100 * share(ow, 'invented_any'):.1f}%)")
    t = analyse.paired(A10, "lex_per100", lambda r: r["instr"] == "plain", "brief", "specific", "vague")
    v["ALL10_L2"] = (f"{t['mean_b']:.2f} vs {t['mean_a']:.2f} listed phrases per 100 words ({t['mean_b'] / t['mean_a']:.1f}x), "
                     f"vague higher in {t['same_dir']} of {t['n_scen']} tasks")
    t = analyse.paired(A10, "lex_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid")
    v["ALL10_L4A"] = (f"avoid clichés: {100 * (1 - t['mean_b'] / t['mean_a']):.0f}% fewer listed phrases, lower in "
                      f"{t['same_dir']} of {t['n_scen']} tasks")
    t = analyse.paired(A10, "invented_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid")
    v["ALL10_L4X"] = (f"avoid clichés: invented numbers and dates per 100 words {t['mean_a']:.2f} -> {t['mean_b']:.2f} "
                      f"({100 * (t['mean_b'] / t['mean_a'] - 1):+.0f}%), higher in {t['same_dir']} of {t['n_scen']} tasks "
                      f"(exploratory in v1.0; E1 replicates the direction, see E1_R_L4b)")
    vp10 = [x["text"] for x in allrecs if x["exp"] == "A" and x["brief"] == "vague" and x["instr"] == "plain"]
    mild = {"enhance": r"enhanc(?:e|es|ed|ing)", "streamline": r"streamlin(?:e|es|ed|ing)", "reach out": r"reach out",
            "excited to announce": r"excited to announce"}
    v["ALL10_MILD"] = "; ".join(f"'{k}' {cnt(p, vp10)}" for k, p in mild.items()) + \
        f" of {len(vp10):,} vague-brief drafts with no style instruction (ten models)"
    v["ALL10_CLAUDE55_EM"] = (f"{sum('—' in x['text'] for m in ('claude-opus-5.5', 'claude-sonnet-5.5', 'claude-haiku-5.5') for x in by[m])} "
                              f"of {sum(len(by[m]) for m in ('claude-opus-5.5', 'claude-sonnet-5.5', 'claude-haiku-5.5'))} Claude 5.5 outputs")
    return v


def e2_numbers():
    """E2 keys (design E2 v1.0, exploratory genre probe). Empty until runs_e2.jsonl exists."""
    path = HERE / "data" / "runs_e2.jsonl"
    if not path.exists():
        return {}
    sys.path.insert(0, str(HERE))
    import analyse_e2 as e2
    latest = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("ok"):
            latest[r["key"]] = r
    recs = list(latest.values())
    sel = lambda genres, model: [r for r in recs if r["genre"] in genres and r["model"] == model]
    k = lambda rs, rx: f"{sum(bool(rx.search(r['text'])) for r in rs)} of {len(rs)}"
    em = lambda rs: f"{sum('—' in r['text'] for r in rs)} of {len(rs)}"
    nb = ("abstract", "encyclopedia", "essay", "fiction", "explainer")
    return {
        "E2_N": f"{len(recs)}",
        "E2_DELVE_ALL": f"'delve' in {k(recs, e2.DELVE)} E2 outputs (all genres, all three models)",
        "E2_ERA_GPT4O": (f"GPT-4o, distinctive GPT-4-era words: abstracts {k(sel(('abstract',), 'gpt-4o'), e2.ERA)}, encyclopedia "
                         f"{k(sel(('encyclopedia',), 'gpt-4o'), e2.ERA)}, business control {k(sel(('business',), 'gpt-4o'), e2.ERA)}"),
        "E2_ERA_MINI": (f"GPT-4o mini: abstracts {k(sel(('abstract',), 'gpt-4o-mini'), e2.ERA)}, non-business pooled "
                        f"{k(sel(nb, 'gpt-4o-mini'), e2.ERA)}, business {k(sel(('business',), 'gpt-4o-mini'), e2.ERA)}"),
        "E2_ERA_GPT6": (f"GPT-6 Sol: non-business pooled {k(sel(nb, 'gpt-6-sol'), e2.ERA)}, business "
                        f"{k(sel(('business',), 'gpt-6-sol'), e2.ERA)}"),
        "E2_EM_GPT4O": (f"GPT-4o em dash: essays {em(sel(('essay',), 'gpt-4o'))}, stories {em(sel(('fiction',), 'gpt-4o'))}, "
                        f"essays and stories {em(sel(('essay', 'fiction'), 'gpt-4o'))}, business {em(sel(('business',), 'gpt-4o'))}"),
        "E2_EM_GPT6": f"GPT-6 Sol em dash: non-business {em(sel(nb, 'gpt-6-sol'))}, business {em(sel(('business',), 'gpt-6-sol'))}",
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = list(csv.DictReader((HERE / "results" / "main_measures.csv").open(encoding="utf-8")))
    num = ("words", "lex_per100", "lex_core_per100", "prefab_rate", "specifics_per100", "invented",
           "invented_any", "questions", "asks", "lex_author", "lex_ai_literature")
    for r in rows:
        for k in num:
            r[k] = float(r[k])
        r["invented_per100"] = 100 * r["invented"] / r["words"]
    A = [r for r in rows if r["exp"] == "A"]
    B = [r for r in rows if r["exp"] == "B"]
    mean = lambda rs: sum(rs) / len(rs)
    v = {"N_OUT": f"{len(rows):,}"}

    import re
    vague = [r for r in A if r["brief"] == "vague"]
    any_author = sum(r["lex_author"] > 0 for r in vague)
    latest = {}
    for line in (HERE / "data" / "runs_main.jsonl").read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("ok"):
            latest[rec["key"]] = rec
    texts = [rec["text"] for rec in latest.values() if rec["exp"] == "A" and rec["brief"] == "vague"]
    spoken = {"heighten engagement": r"heighten(s|ed|ing)? engagement", "move the dial": r"mov(e|es|ed|ing) the dial",
              "unlock potential": r"unlock(s|ed|ing)? (the |our |your |its )?(full )?potential",
              "unified approach": r"unified approach", "at a high level": r"at a high level"}
    counts = {k: sum(bool(re.search(rf"\b{p}\b", t, re.I)) for t in texts) for k, p in spoken.items()}
    v["AUTHOR_ZERO"] = ("; ".join(f"'{k}' {c}" for k, c in counts.items()) +
                       f" of {len(texts)} vague-brief drafts; any of the author's terms in {any_author} of {len(vague)}")
    v["_author_spoken_all_zero"] = all(c == 0 for c in counts.values())
    sub_ = sum(bool(re.search(r"unlock", t_, re.I)) for t_ in texts)
    word_ = sum(bool(re.search(r"\bunlock\w*\b", t_, re.I)) for t_ in texts)
    v["UNLOCK_ANY"] = (f"'unlock' as a word in {word_} of {len(texts)}; as a substring anywhere in {sub_} "
                       f"(the hashtag #AchievementUnlocked)")
    v["AI_LIT_VAGUE"] = f"{sum(r['lex_ai_literature'] > 0 for r in vague)} of {len(vague)}"

    t = analyse.paired(A, "lex_core_per100", lambda r: r["instr"] == "plain", "brief", "specific", "vague")
    v["L2_DETAIL"] = (f"{t['mean_b']:.2f} vs {t['mean_a']:.2f} per 100 words ({t['mean_b'] / t['mean_a']:.1f}x), "
                      f"vague higher in {t['same_dir']} of {t['n_scen']} tasks, sign-flip p {t['p']:.4f}")

    t = analyse.paired(A, "lex_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid")
    drop = 1 - t["mean_b"] / t["mean_a"]
    v["L4A_SPOKEN"] = per_cent_words(drop)
    v["L4A_DETAIL"] = f"-{100 * drop:.0f}% stock phrases per 100 words, lower in {t['same_dir']} of {t['n_scen']} tasks"
    t = analyse.paired(A, "invented_per100", lambda r: r["brief"] == "vague", "instr", "plain", "avoid")
    v["L4X_DETAIL"] = (f"invented specifics per 100 words {t['mean_a']:.2f} -> {t['mean_b']:.2f} "
                       f"({100 * (t['mean_b'] / t['mean_a'] - 1):+.0f}%), higher in {t['same_dir']} of {t['n_scen']} "
                       f"tasks, p {t['p']:.3f}")

    by = defaultdict(list)
    for r in B:
        by[r["instr"]].append(r)
    spec, clear, orw = (mean([r["invented_any"] for r in by[k]]) for k in ("specific", "clearer", "orwell"))
    t3 = analyse.paired(B, "invented_any", lambda r: True, "instr", "clearer", "specific")
    v["L3_SPOKEN"] = fraction_words(spec)
    v["L3_CLEARER_SPOKEN"] = "one in ten" if 0.07 <= clear < 0.15 else f"{100 * clear:.0f} per cent"
    v["L3_DETAIL"] = (f"{100 * spec:.0f}% of 'more specific' vs {100 * clear:.0f}% of 'clearer' rewrites added an "
                      f"invented specific; higher in {t3['same_dir']} of {t3['n_scen']} tasks")
    asks = mean([r["asks"] for r in by["orwell"]])
    t5 = analyse.paired(B, "invented_any", lambda r: True, "instr", "specific", "orwell")
    v["L5_ASK_SPOKEN"] = in_ten(asks)
    v["L5_INV_SPOKEN"] = small_words(orw)
    v["L5_DETAIL"] = (f"asked >=1 question in {100 * asks:.0f}%, mean {mean([r['questions'] for r in by['orwell']]):.1f} "
                      f"questions; invented a specific in {100 * orw:.0f}% vs {100 * spec:.0f}% for 'more specific'; "
                      f"lower in {t5['same_dir']} of {t5['n_scen']} tasks")

    judged = {}
    for line in (HERE / "data" / "judge_main.jsonl").read_text(encoding="utf-8").splitlines():
        x = json.loads(line)
        run = latest.get(x["key"])
        if x.get("ok") and run and (x.get("run_ts") == run.get("ts") or (x.get("run_ts") is None and not run.get("regen"))):
            judged[x["key"]] = x
    sp = [judged[k]["invented_as"] for k, rec in latest.items() if rec["exp"] == "B" and rec["instr"] == "specific" and k in judged]
    v["JUDGE_DETAIL"] = (f"LLM judge (secondary; VAL-1: response type agreed with the author's blind coding 82%, kappa 0.73; the invented-as comparison was invalid): of {len(sp)} 'more specific' rewrites, invented facts were "
                         f"stated as the writer's position in {100 * sp.count('assertion') / len(sp):.0f}% and offered as examples or options in "
                         f"{100 * sp.count('example') / len(sp):.0f}%")
    cl = [m for m in {r["model"] for r in B} if m.startswith("claude")]
    other = [m for m in {r["model"] for r in B} if not m.startswith("claude")]
    rng = lambda ms, k: (min(mean([r[k] for r in by["specific"] if r["model"] == m]) for m in ms),
                         max(mean([r[k] for r in by["specific"] if r["model"] == m]) for m in ms))
    ci, co = rng(cl, "invented_any"), rng(other, "invented_any")
    li, lo = rng(cl, "lex_per100"), rng(other, "lex_per100")
    v["CAMO_DETAIL"] = (f"on 'more specific', the Claude models invented facts in {100 * ci[0]:.0f}-{100 * ci[1]:.0f}% "
                        f"of rewrites with {li[0]:.1f}-{li[1]:.1f} stock phrases per 100 words; the Amazon and Qwen "
                        f"models invented in {100 * co[0]:.0f}-{100 * co[1]:.0f}% but used {lo[0]:.1f}-{lo[1]:.1f} "
                        f"stock phrases per 100 words")
    v["N_VAGUE_DRAFTS"] = f"{len(texts):,}"
    orw_recs = [rec for rec in latest.values() if rec["exp"] == "B" and rec["instr"] == "orwell"]
    v["ORWELL_ASKS_N"] = f"{sum(1 for rec in orw_recs if any(s.endswith('?') for s in analyse.sentences(rec['text'])))} of {len(orw_recs)}"
    v["ORWELL_INV_N"] = f"{int(sum(r['invented_any'] for r in by['orwell']))} of {len(by['orwell'])}"
    t2 = analyse.paired(A, "prefab_rate", lambda r: r["instr"] == "plain", "brief", "specific", "vague")
    v["L2_PREFAB"] = f"prefabricated wording {t2['mean_b']:.3f} vs {t2['mean_a']:.3f} ({100 * (t2['mean_b'] / t2['mean_a'] - 1):+.0f}%), higher in {t2['same_dir']} of {t2['n_scen']} tasks"

    # DESC-1 (descriptive, post hoc selection of phrases; see deviations.md): named phrases across every output
    recs = list(latest.values())
    allt = [rec["text"] for rec in recs]
    vp = [rec["text"] for rec in recs if rec["exp"] == "A" and rec["brief"] == "vague" and rec["instr"] == "plain"]
    ap = r"(?:'|’)"
    tells = {"delve": r"delv(?:e|es|ed|ing)", "tapestry": r"tapestr(?:y|ies)", "pivotal": r"pivotal",
             "a pivotal moment": r"a pivotal moment", "in today's fast-paced world": rf"in today{ap}s fast[- ]paced world",
             "in today's": rf"in today{ap}s", "low-hanging fruit": r"low[- ]hanging fruit",
             "game-changer": r"game[- ]chang(?:er|ers|ing)", "think outside the box": r"think(?:ing)? outside the box",
             "paradigm shift": r"paradigm shifts?", "synergy": r"synerg(?:y|ies)", "circle back": r"circl(?:e|es|ed|ing) back"}
    cnt = lambda pat, ts: sum(bool(re.search(rf"\b{pat}\b", t_, re.I)) for t_ in ts)
    v["TELL_COUNTS_ALL"] = "; ".join(f"'{k}' {cnt(p, allt)}" for k, p in tells.items()) + f" of {len(allt):,} outputs"
    spoken = ("delve", "tapestry", "a pivotal moment", "game-changer", "low-hanging fruit", "in today's fast-paced world")
    v["_tells_spoken_zero"] = all(cnt(tells[k], allt) == 0 for k in spoken)
    # the lexicon's own patterns (one count per phrase), plus the exact phrase that is spoken
    mild = {"enhance": r"enhanc(?:e|es|ed|ing)", "streamline": r"streamlin(?:e|es|ed|ing)", "reach out": r"reach out",
            "excited to announce": r"excited to announce"}
    v["MILD_COUNTS"] = "; ".join(f"'{k}' {cnt(p, vp)}" for k, p in mild.items()) + \
        f" of {len(vp)} vague-brief drafts with no style instruction"
    t = analyse.paired(A, "lex_per100", lambda r: r["instr"] == "plain", "brief", "specific", "vague")
    v["L2_FULL"] = (f"full list: {t['mean_b']:.2f} vs {t['mean_a']:.2f} per 100 words ({t['mean_b'] / t['mean_a']:.1f}x), "
                    f"vague higher in {t['same_dir']} of {t['n_scen']} tasks, sign-flip p {t['p']:.3f}")
    lexj = json.loads((HERE / "lexicon v0.1.json").read_text(encoding="utf-8"))
    At = [rec["text"] for rec in recs if rec["exp"] == "A"]
    Br = [rec for rec in recs if rec["exp"] == "B"]
    for cat in ("business", "ai_literature", "ai_practitioner"):
        pats = lexj["categories"][cat]
        anyv = sum(any(re.search(rf"\b(?:{p})\b", t_, re.I) for p in pats) for t_ in vp)
        perA = sorted(((cnt(f"(?:{p})", At), p) for p in pats), reverse=True)
        perB = []
        for p in pats:
            hits = [rec for rec in Br if re.search(rf"\b(?:{p})\b", rec["text"], re.I)]
            inp = sum(bool(re.search(rf"\b(?:{p})\b", rec["prompt"], re.I)) for rec in hits)
            perB.append((len(hits), inp, p))
        perB.sort(reverse=True)
        v[f"LEX_TERMS_{cat.upper()}"] = (
            f"any term in {anyv} of {len(vp)} vague-brief drafts (no style instruction). Drafts (A, {len(At):,}): "
            + "; ".join(f"{p} {n}" for n, p in perA)
            + f". Rewrites (B, {len(Br):,}; in brackets, how many had the phrase in the input): "
            + "; ".join(f"{p} {n} ({i})" for n, i, p in perB))
    v.update(e1_numbers(latest, cnt, tells))
    v.update(e2_numbers())
    print(json.dumps(v, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
