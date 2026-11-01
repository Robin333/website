"""Secondary measure for the Ep01 study: code each Experiment B output's response type with an LLM judge.

The pre-registered rubric is in `design v1.0.md`. The judge sees only the original sentence and the
model's reply. It never sees which instruction was given or which model replied. Labels are
validated against the author's blind hand-coding (`make_coding_sheet.py`).

Usage:
    python lab/ep01/judge.py --set main [--workers 8] [--limit N] [--tag e1]
Resumable: writes data/judge_<set>[_<tag>].jsonl and skips keys that are already coded.
"""
import argparse
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "core"))
from models import MODELS, Models  # noqa: E402

JUDGE = "claude-opus-5.5"
RUBRIC = """You are coding replies for a research study. A writer gave an AI assistant one sentence and asked for help with it. You see the writer's original sentence and the assistant's reply. Code the reply using these definitions, exactly:

response_type:
- single_rewrite: one rewritten sentence or paragraph presented as the answer (extra commentary is fine)
- options: two or more alternative rewrites, usually conditional on what the writer meant
- questions_first: asks the writer questions before (or instead of) rewriting; any example rewrite is secondary
- other: none of the above

invented_facts: list every specific fact in the reply that is NOT in the original sentence: numbers, percentages, dates, deadlines, time periods, targets, named people or teams. Include ones inside rewrites or examples. Exclude bracketed placeholders like [date] and facts that only appear inside questions to the writer.

invented_as:
- assertion: at least one invented fact is stated as the writer's position in the main rewrite
- example: invented facts appear only as illustrations, options or examples the writer is invited to choose from or replace
- none: no invented facts

flags_ambiguity: true if the reply explicitly says the original is vague/ambiguous or that the right rewrite depends on information the writer has not given."""

SCHEMA = {
    "type": "object",
    "properties": {
        "response_type": {"type": "string", "enum": ["single_rewrite", "options", "questions_first", "other"]},
        "invented_facts": {"type": "array", "items": {"type": "string"}},
        "invented_as": {"type": "string", "enum": ["assertion", "example", "none"]},
        "flags_ambiguity": {"type": "boolean"},
    },
    "required": ["response_type", "invented_facts", "invented_as", "flags_ambiguity"],
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["pilot", "main"], required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tag", default="", help="extension tag, e.g. e1")
    a = ap.parse_args()
    scen = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]}
    latest = {}
    for line in (HERE / "data" / (f"runs_{a.set}_{a.tag}.jsonl" if a.tag else f"runs_{a.set}.jsonl")).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("ok") and r["exp"] == "B":
            latest[r["key"]] = r
    out = HERE / "data" / (f"judge_{a.set}_{a.tag}.jsonl" if a.tag else f"judge_{a.set}.jsonl")
    done = set()
    if out.exists():
        for l in out.read_text(encoding="utf-8").splitlines():
            x = json.loads(l)
            if x.get("ok"):
                done.add((x["key"], x.get("run_ts")))
    def is_done(k, r):
        # A coding applies to the exact output it saw. Early codings have no run_ts. They are valid only
        # for original outputs, never for outputs regenerated after the truncation fix.
        return (k, r.get("ts")) in done or (not r.get("regen") and (k, None) in done)

    todo = [r for k, r in sorted(latest.items()) if not is_done(k, r)]
    if a.limit:
        todo = todo[:a.limit]
    print(f"judge {a.set}: {len(todo)} to code ({len(done)} done) with {JUDGE}")
    client, lock = Models(), threading.Lock()
    tool = {"name": "record_coding", "description": "Record the coding for this reply.", "input_schema": SCHEMA}

    def work(r):
        sentence = scen[r["scenario"]]["vague_sentence"]
        prompt = f'{RUBRIC}\n\nORIGINAL SENTENCE:\n"{sentence}"\n\nASSISTANT REPLY:\n"""\n{r["text"]}\n"""'
        # Opus 5.5 via the API rejects forced tool_choice, so ask for the tool and retry if it's skipped.
        prompt += "\n\nRespond only by calling the record_coding tool."
        try:
            for _ in range(3):
                resp = client.anthropic.messages.create(
                    model=MODELS[JUDGE][1], max_tokens=1200, tools=[tool], tool_choice={"type": "auto"},
                    messages=[{"role": "user", "content": prompt}])
                block = next((b for b in resp.content if b.type == "tool_use"), None)
                if block and all(k in block.input for k in SCHEMA["required"]):
                    return {"key": r["key"], "run_ts": r.get("ts"), "ok": True, "judge": JUDGE, **block.input}
            return {"key": r["key"], "ok": False, "error": "no valid record_coding call after 3 tries"}
        except Exception as e:
            return {"key": r["key"], "ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}

    n = 0
    with ThreadPoolExecutor(a.workers) as ex, out.open("a", encoding="utf-8") as fh:
        for fut in as_completed([ex.submit(work, r) for r in todo]):
            with lock:
                fh.write(json.dumps(fut.result(), ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
                if n % 100 == 0 or n == len(todo):
                    print(f"  {n}/{len(todo)}", flush=True)


if __name__ == "__main__":
    main()
