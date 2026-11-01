"""Analyse the Ep01 E2 genre probe (design E2 v1.0). Descriptive only.

    python lab/ep01/analyse_e2.py      -> results/e2_summary.md
"""
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELVE = re.compile(r"\bdelv(?:e|es|ed|ing)\b", re.I)
SPOKEN = re.compile(r"\b(?:delv(?:e|es|ed|ing)|tapestr(?:y|ies)|pivotal)\b", re.I)
GPT4ERA = {"delve": r"delv(?:e|es|ed|ing)", "tapestry": r"tapestr(?:y|ies)", "pivotal": r"pivotal", "testament": r"testaments?",
           "intricate": r"intricat(?:e|ely)|intricac(?:y|ies)", "interplay": r"interplay", "meticulous": r"meticulous(?:ly)?",
           "underscore": r"underscor(?:e|es|ed|ing)", "boast": r"boast(?:s|ed|ing)?", "garner": r"garner(?:s|ed|ing)?",
           "bolstered": r"bolster(?:s|ed|ing)?", "vibrant": r"vibrant", "enduring": r"enduring"}
ERA = re.compile(r"\b(?:" + "|".join(GPT4ERA.values()) + r")\b", re.I)
GENRES = ["abstract", "encyclopedia", "essay", "fiction", "explainer", "business"]
MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-6-sol"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    latest = {}
    for line in (HERE / "data" / "runs_e2.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("ok"):
            latest[r["key"]] = r
    recs = list(latest.values())
    cell = defaultdict(list)
    for r in recs:
        cell[(r["genre"], r["model"])].append(r)
    fmt = lambda k, n: f"{k}/{n} [{100 * wilson(k, n)[0]:.0f}–{100 * wilson(k, n)[1]:.0f}%]"
    out = ["# Ep01 E2 genre probe: results (descriptive)", "",
           f"{len(recs)} outputs; design `design E2 v1.0.md`. Cells: 3 topics × 5 reps = 15 outputs per genre × model. "
           "Brackets: Wilson 95% CI.", ""]
    for title, test in [("\"delve\" (any form)", lambda t: bool(DELVE.search(t))),
                        ("any of the spoken three (delve, tapestry, pivotal)", lambda t: bool(SPOKEN.search(t))),
                        ("any distinctive GPT-4-era word (S11 list, design E2)", lambda t: bool(ERA.search(t))),
                        ("em dash", lambda t: "—" in t)]:
        out += [f"## Outputs containing {title}", "| genre | " + " | ".join(MODELS) + " |", "|---|" + "---|" * len(MODELS)]
        for g in GENRES:
            out.append(f"| {g} | " + " | ".join(fmt(sum(test(r['text']) for r in cell[(g, m)]), len(cell[(g, m)])) for m in MODELS) + " |")
        nb = {m: [r for g in GENRES[:-1] for r in cell[(g, m)]] for m in MODELS}
        out.append("| **non-business pooled** | " + " | ".join(fmt(sum(test(r['text']) for r in nb[m]), len(nb[m])) for m in MODELS) + " |")
        out.append("")
    out += ["## Which GPT-4-era words appeared (all outputs, by model)", "| word | " + " | ".join(MODELS) + " |",
            "|---|" + "---|" * len(MODELS)]
    for w, p in GPT4ERA.items():
        out.append(f"| {w} | " + " | ".join(str(sum(bool(re.search(rf'\b(?:{p})\b', r['text'], re.I)) for r in recs if r['model'] == m))
                                           for m in MODELS) + " |")
    out += ["", "## Every 'delve' in context"]
    for r in sorted(recs, key=lambda r: r["key"]):
        for mt in DELVE.finditer(r["text"]):
            a, b = max(0, mt.start() - 70), mt.end() + 50
            out.append(f"- {r['key']}: …{r['text'][a:b].replace(chr(10), ' ')}…")
    (HERE / "results" / "e2_summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
