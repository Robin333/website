"""Build the author's blind hand-coding workbook, and score it once it's filled in.

    python lab/ep01/make_coding_sheet.py build --set main     # writes the workbook and the hidden key
    python lab/ep01/make_coding_sheet.py score --set main     # once the author has filled it in

Build: draws 60 Experiment B replies, 20 per instruction, spread across models, with a fixed seed.
The rows are shuffled. The coder never sees the instruction or the model; that key is kept in
data/_coding_key_<set>.json. Score: compares the author's codes with the regex measure (invented fact,
yes/no) and with the LLM judge (response type, invented-as). It reports percentage agreement and
Cohen's kappa.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
F = "Arial"
YELLOW = PatternFill("solid", fgColor="FFF2CC")
GREY = PatternFill("solid", fgColor="EDEDED")
THIN = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
TYPES = ["Single rewrite", "Options", "Questions first", "Other"]
AS = ["Assertion", "Example", "None"]
TYPE_CODE = dict(zip(TYPES, ["single_rewrite", "options", "questions_first", "other"]))
AS_CODE = dict(zip(AS, ["assertion", "example", "none"]))


def latest(path, filt=lambda r: True):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("ok") and filt(r):
            out[r["key"]] = r
    return out


def build(set_):
    scen = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]}
    runs = latest(HERE / "data" / f"runs_{set_}.jsonl", lambda r: r["exp"] == "B")
    rng = random.Random(20261030)
    picked = []
    for instr in ("clearer", "specific", "orwell"):
        pool = defaultdict(list)
        for r in runs.values():
            if r["instr"] == instr:
                pool[r["model"]].append(r)
        models = sorted(pool)
        for m in models:
            rng.shuffle(pool[m])
        i = 0
        while sum(1 for p in picked if p["instr"] == instr) < 20:  # round-author across models
            m = models[i % len(models)]
            if pool[m]:
                picked.append(pool[m].pop())
            i += 1
    rng.shuffle(picked)
    key = {}
    wb = Workbook()
    guide = wb.active
    guide.title = "How to code"
    lines = [
        ("Blind coding sheet: Second Order Ep01 study", True),
        ("", False),
        ("What this is: 60 replies from AI models. Each one was asked to help with a single sentence. "
         "You don't know which model wrote each reply, or what it was asked to do. Please keep it that way.", False),
        ("Time: about 30 minutes. Fill in only the yellow cells on the 'Code' sheet (columns D, E and F). "
         "Column G is optional notes.", False),
        ("", False),
        ("D. Invented fact? Choose Yes if the reply contains any specific fact that isn't in the original sentence: "
         "a number, percentage, date, deadline, time period, target, or a named person or team. Count it even if it's "
         "inside an example. Don't count bracketed placeholders like [date], or facts that appear only inside a "
         "question to the writer.", False),
        ("E. Response type:", False),
        ("     Single rewrite: one rewritten sentence or paragraph, presented as the answer", False),
        ("     Options: two or more alternative rewrites, usually depending on what the writer meant", False),
        ("     Questions first: asks the writer questions before (or instead of) rewriting", False),
        ("     Other: none of the above", False),
        ("F. Invented facts stated as:", False),
        ("     Assertion: at least one invented fact is stated as the writer's position in the main rewrite", False),
        ("     Example: invented facts appear only as illustrations or options the writer can choose or replace", False),
        ("     None: no invented facts (use this whenever D is No)", False),
        ("", False),
        ("Row C00 on the 'Code' sheet is a worked EXAMPLE (grey). It isn't part of the sample.", False),
        ("When you're done, save the file and tell Claude. Agreement with the automatic coding is then calculated.", False),
    ]
    for i, (t, bold) in enumerate(lines, 1):
        c = guide.cell(row=i, column=1, value=t)
        c.font = Font(name=F, size=14 if i == 1 else 11, bold=bold)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    guide.column_dimensions["A"].width = 120

    ws = wb.create_sheet("Code")
    heads = ["ID", "Original sentence", "AI reply", "D. Invented fact? (Yes/No)",
             "E. Response type", "F. Invented facts stated as", "G. Notes (optional)"]
    for j, h in enumerate(heads, 1):
        c = ws.cell(row=1, column=j, value=h)
        c.font = Font(name=F, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="404040")
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = THIN
    example = ["C00 (EXAMPLE)", "We need to heighten engagement with the training programme.",
               'Here\'s a more specific version: "We need to raise attendance at the training programme by 25% '
               'by the end of Q2."', "Yes", "Single rewrite", "Assertion", "25% and Q2 were not in the original"]
    rows = [example] + [[f"C{i:02d}", scen[r["scenario"]]["vague_sentence"], r["text"], None, None, None, None]
                        for i, r in enumerate(picked, 1)]
    for i, r in enumerate(picked, 1):
        key[f"C{i:02d}"] = {"run_key": r["key"], "instr": r["instr"], "model": r["model"], "scenario": r["scenario"]}
    for ri, row in enumerate(rows, 2):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=ri, column=j, value=v)
            c.font = Font(name=F, size=10, italic=(ri == 2))
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = THIN
            if ri == 2:
                c.fill = GREY
            elif j in (4, 5, 6):
                c.fill = YELLOW
        ws.row_dimensions[ri].height = min(400, 15 * (1 + len(str(row[2])) // 75))
    for col, w in zip("ABCDEFG", (9, 30, 90, 14, 18, 18, 30)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "D2"
    last = len(rows) + 1
    for col, opts in (("D", ["Yes", "No"]), ("E", TYPES), ("F", AS)):
        dv = DataValidation(type="list", formula1='"' + ",".join(opts) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col}3:{col}{last}")
    out = HERE / "results" / f"Ep01 blind coding sheet ({set_}).xlsx"
    out.parent.mkdir(exist_ok=True)
    wb.save(out)
    (HERE / "data" / f"_coding_key_{set_}.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print(out, f"({len(picked)} rows; by instruction: {dict(Counter(k['instr'] for k in key.values()))})")


def kappa(pairs):
    n = len(pairs)
    if not n:
        return float("nan"), float("nan")
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def score(set_):
    import analyse  # for the regex measure
    key = json.loads((HERE / "data" / f"_coding_key_{set_}.json").read_text(encoding="utf-8"))
    runs = latest(HERE / "data" / f"runs_{set_}.jsonl")
    judged = latest(HERE / "data" / f"judge_{set_}.jsonl")
    ws = load_workbook(HERE / "results" / f"Ep01 blind coding sheet ({set_}).xlsx")["Code"]
    d_pairs, e_pairs, f_pairs = [], [], []
    for row in ws.iter_rows(min_row=3, values_only=True):
        cid, d, e, f = row[0], row[3], row[4], row[5]
        if cid not in key or d is None:
            continue
        run = runs[key[cid]["run_key"]]
        _, invented = analyse.specifics(run["text"], run["prompt"])
        d_pairs.append((d == "Yes", bool(invented)))
        j = judged.get(key[cid]["run_key"])
        if j and e:
            e_pairs.append((TYPE_CODE[e], j["response_type"]))
        if j and f:
            f_pairs.append((AS_CODE[f], j["invented_as"]))
    for name, pairs in (("D invented fact: the author vs regex", d_pairs), ("E response type: the author vs judge", e_pairs),
                        ("F invented-as: the author vs judge", f_pairs)):
        po, k = kappa(pairs)
        print(f"{name}: n={len(pairs)}, agreement {100 * po:.0f}%, kappa {k:.2f} "
              f"-> {'OK' if po >= 0.85 and k >= 0.6 else 'BELOW THRESHOLD: fix the measure and report it'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"build": build, "score": score}[sys.argv[1]](sys.argv[sys.argv.index("--set") + 1])
