"""Run the Ep01 study: how AI models write, rewrite and question vague business text.

Experiment A (drafting): each scenario's task, with a vague or specific brief, and a plain or
"avoid clichés" instruction.
Experiment B (rewriting): each scenario's vague sentence, under "make it clearer", "make it more
specific" or the Orwell check (verbatim from the Ep01 script).

Usage:
    python lab/ep01/run.py --set pilot --reps 2 [--models all] [--workers 8] [--dry-run]
    python lab/ep01/run.py --set main  --reps 5

The run is resumable: results append to lab/ep01/data/runs_<set>.jsonl, and any key that is
already done is skipped, so if a run is interrupted, just start it again. A long main run
should be launched in the background.

Extensions (from 30 Oct 2026) keep their data apart from the frozen v1.0 study:
    python lab/ep01/run.py --set pilot --reps 2 --models gpt-4o,gpt-5.5,gpt-6-sol --tag e1 --cap 4000
    python lab/ep01/run.py --set main  --reps 5 --models gpt-4o,gpt-5.5,gpt-6-sol --tag e1 --cap 4000
--tag writes runs_<set>_<tag>.jsonl. --cap sets the starting token cap for every call (default: the
v1.0 caps, 700 for drafts and 500 for rewrites). The prompts are unchanged.
"""
import argparse
import itertools
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "core"))
from models import EXTRA_MODELS, MODELS, Models  # noqa: E402

AVOID = " Use plain English and avoid clichés and stock business phrases."
# Must match the prompt in the Ep01 script (v0.3+) word for word. It's frozen before the main run.
ORWELL_CHECK = ("Review this for clarity of meaning. List the questions my writing leaves unanswered, most "
                "important first, and no more than three. Quote the words that leave each one unclear. Ask me "
                "those questions before you rewrite anything, and don't invent missing facts.")
B_PROMPTS = {
    "clearer": 'Rewrite this sentence to make it clearer:\n\n"{s}"',
    "specific": 'Rewrite this sentence to make it more specific:\n\n"{s}"',
    "orwell": ORWELL_CHECK + '\n\n"{s}"',
}


def prompt_a(sc, brief, instr):
    p = f"Write {sc['task']}. Keep it under 150 words." + (AVOID if instr == "avoid" else "")
    if brief == "specific":
        p += "\n\nInclude these facts:\n" + "\n".join(f"- {f}" for f in sc["facts"])
    return p


def tasks(scenarios, models, reps, cap=None):
    for sc, m, r in itertools.product(scenarios, models, range(1, reps + 1)):
        for brief, instr in itertools.product(("vague", "specific"), ("plain", "avoid")):
            yield {"key": f"A|{sc['id']}|{brief}|{instr}|{m}|{r}", "exp": "A", "scenario": sc["id"],
                   "set": sc["set"], "brief": brief, "instr": instr, "model": m, "rep": r,
                   "prompt": prompt_a(sc, brief, instr), "max_tokens": cap or 700}
        for instr, tpl in B_PROMPTS.items():
            yield {"key": f"B|{sc['id']}|-|{instr}|{m}|{r}", "exp": "B", "scenario": sc["id"],
                   "set": sc["set"], "brief": "-", "instr": instr, "model": m, "rep": r,
                   "prompt": tpl.format(s=sc["vague_sentence"]), "max_tokens": cap or 500}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["pilot", "main"], required=True)
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--models", default="all", help="comma-separated keys from lab/core/models.py")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--regenerate-truncated", action="store_true",
                    help="regenerate EVERY output in any (exp, brief, instr, model) cell where an output hit the "
                         "token limit, with --max-tokens; a disclosed deviation (see deviations.md)")
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--tag", default="", help="extension tag: data go to runs_<set>_<tag>.jsonl")
    ap.add_argument("--cap", type=int, default=None, help="starting token cap for every call (default: v1.0 caps)")
    a = ap.parse_args()

    scenarios = [s for s in json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]
                 if s["set"] == a.set]
    models = list(MODELS) if a.models == "all" else a.models.split(",")
    unknown = [m for m in models if m not in MODELS and m not in EXTRA_MODELS]
    if unknown:
        sys.exit(f"unknown model keys: {unknown}")
    out = HERE / "data" / (f"runs_{a.set}_{a.tag}.jsonl" if a.tag else f"runs_{a.set}.jsonl")
    out.parent.mkdir(exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("ok"):
                done.add(rec["key"])
    todo = [t for t in tasks(scenarios, models, a.reps, a.cap) if t["key"] not in done]
    if a.regenerate_truncated:
        latest, regen_done = {}, set()
        for line in out.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("ok"):
                latest[rec["key"]] = rec
                if rec.get("regen") == "truncation-v1":
                    regen_done.add(rec["key"])
        cell = lambda r: (r["exp"], r["brief"], r["instr"], r["model"])
        hit = {cell(r) for r in latest.values()
               if r.get("stop_reason") in ("max_tokens", "length") and r.get("regen") != "truncation-v1"}
        todo = [{**t, "max_tokens": a.max_tokens, "regen": "truncation-v1"}
                for t in tasks(scenarios, models, a.reps) if cell(t) in hit and t["key"] not in regen_done]
        print(f"regenerating {len(hit)} truncated cells: {sorted(hit)}")
    print(f"{a.set}: {len(scenarios)} scenarios x {len(models)} models x {a.reps} reps -> "
          f"{len(todo)} calls to make ({len(done)} already done) -> {out}")
    if a.dry_run or not todo:
        return

    client, lock, n_ok, n_err, started = Models(), threading.Lock(), 0, 0, time.time()

    def work(t):
        try:
            res = client.call(t["model"], t["prompt"], t["max_tokens"])
            return {**t, **res, "ok": True}
        except Exception as e:  # recorded and retried on the next run
            return {**t, "ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}

    with ThreadPoolExecutor(a.workers) as ex, out.open("a", encoding="utf-8") as fh:
        for fut in as_completed([ex.submit(work, t) for t in todo]):
            rec = {**fut.result(), "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                n_ok, n_err = n_ok + rec["ok"], n_err + (not rec["ok"])
                if (n_ok + n_err) % 25 == 0 or n_ok + n_err == len(todo):
                    print(f"  {n_ok + n_err}/{len(todo)} done, {n_err} errors, {time.time() - started:.0f}s",
                          flush=True)
    print(f"finished: {n_ok} ok, {n_err} errors (re-run the same command to retry errors)")


if __name__ == "__main__":
    main()
