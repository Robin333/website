"""Run the Ep01 E2 genre probe (design E2 v1.0): OpenAI models writing in the genres where "delve" was documented.

    python lab/ep01/run_e2.py [--workers 8] [--dry-run]

Resumable: results append to lab/ep01/data/runs_e2.jsonl, and done keys are skipped.
"""
import argparse
import itertools
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "core"))
sys.path.insert(0, str(HERE))
from models import Models  # noqa: E402
from run import prompt_a  # noqa: E402  (E1's own prompt builder, for the business control)

MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-6-sol"]
GENRES = {
    "abstract": ("Write a 150-word abstract for a research paper on {t}.",
                 ["sleep and memory in teenagers", "urban heat islands", "soil microbes and crop yields"]),
    "encyclopedia": ("Write a 150-word encyclopedia-style introduction to {t}.",
                     ["the city of Porto", "the Silk Road", "the Highland games"]),
    "essay": ("Write the opening paragraph of an essay on {t}. Keep it under 150 words.",
              ["the future of remote work", "why cities need more trees", "the ethics of self-driving cars"]),
    "fiction": ("Write the first 150 words of a short story about {t}.",
                ["a lighthouse keeper's last night on duty", "a child who finds an old map", "a chef who loses their sense of taste"]),
    "explainer": ("Explain {t} to a general audience in about 150 words.",
                  ["how vaccines train the immune system", "why the sky is blue", "how inflation works"]),
}
BUSINESS = ["S06", "S08", "S16"]
REPS, CAP = 5, 4000


def tasks():
    scen = {s["id"]: s for s in json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))["scenarios"]}
    prompts = [(g, i, tpl.format(t=t)) for g, (tpl, ts) in GENRES.items() for i, t in enumerate(ts, 1)]
    prompts += [("business", i, prompt_a(scen[sid], "vague", "plain")) for i, sid in enumerate(BUSINESS, 1)]
    for (g, i, p), m, r in itertools.product(prompts, MODELS, range(1, REPS + 1)):
        yield {"key": f"E2|{g}|{i}|{m}|{r}", "exp": "E2", "genre": g, "topic": i, "model": m, "rep": r,
               "prompt": p, "max_tokens": CAP}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    out = HERE / "data" / "runs_e2.jsonl"
    done = {json.loads(l)["key"] for l in out.read_text(encoding="utf-8").splitlines()
            if json.loads(l).get("ok")} if out.exists() else set()
    todo = [t for t in tasks() if t["key"] not in done]
    print(f"E2: {len(todo)} calls to make ({len(done)} already done) -> {out}")
    if a.dry_run or not todo:
        return
    client, lock = Models(), threading.Lock()

    def work(t):
        try:
            return {**t, **client.call(t["model"], t["prompt"], t["max_tokens"]), "ok": True}
        except Exception as e:  # recorded and retried on the next run
            return {**t, "ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}

    n = 0
    with ThreadPoolExecutor(a.workers) as ex, out.open("a", encoding="utf-8") as fh:
        for fut in as_completed([ex.submit(work, t) for t in todo]):
            rec = {**fut.result(), "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
    print(f"finished {n} calls")


if __name__ == "__main__":
    main()
