# Least Likely, Episode 1: does AI still write in clichés?

The data, code and pre-registered designs behind the Least Likely video **"We Tested Whether AI Still Writes in Clichés"** (2026). Everything spoken in the video comes from these files. `results/video_figures.json` holds every figure the video uses, computed by `script_numbers.py`.

## The study in brief

- **Main study (pre-registered, frozen before the run):** 7 models from 3 vendors (Anthropic, Amazon, Alibaba), 24 business-writing tasks and 5,880 outputs.
  - **Experiment A (drafting):** a vague or specific brief, written plainly or with an instruction to avoid clichés.
  - **Experiment B (rewriting one sentence):** "make it more specific", "make it clearer", or the hen-house check.
- **Extension E1 (pre-registered separately):** the same protocol on three OpenAI models (GPT-4o, GPT-5.5, GPT-6 Sol), with 2,520 outputs.
- **Follow-up E2 (exploratory, design frozen before the run):** three OpenAI models across five genres (research abstracts, encyclopedia entries, essays, stories, explainers), with 270 outputs.
- **Human validation (VAL-1):** the author blind-coded a random sample of 60 replies, with the model and instruction hidden. See `data/coding_key_main.json` and `data/coding_compare_main.json`.

"Delve" (any form) appears **0 times in the 8,400 outputs** from the 10 models. That includes the 6,000 written with no instruction to avoid clichés. It is also 0 in the 270 follow-up pieces.

## What's here

| Path | What it is |
|---|---|
| `design v1.0.md`, `design E1 v1.0.md`, `design E2 v1.0.md` | The frozen designs (pre-registrations) |
| `deviations.md` | Every deviation from the designs, with what changed and why (DEV-, DESC-, VAL- entries) |
| `scenarios.json`, `lexicon v0.1.json` | The 24 tasks, and the frozen stock-phrase lexicon (83 patterns in four categories) |
| `data/runs_*.jsonl` | Every model output, one JSON record each: the prompt, model, model ID, condition, text, tokens and timestamp. Pilot runs are included but never counted. |
| `data/judge_*.jsonl` | The LLM-judge's response-type codes (a secondary measure) |
| `results/` | Summaries and per-output measures. `*_pre_dev*` files are the results before each documented deviation. |
| `run.py`, `run_e2.py`, `judge.py`, `analyse.py`, `analyse_e2.py`, `script_numbers.py`, `make_coding_sheet.py` | The code that ran and analysed the study |
| `../core/models.py` | A stand-in for the model-access layer, which isn't published. Plug in your own API client to re-run. |

## Re-running the analysis

Python 3.12 with numpy. From this folder:

```
python analyse.py --set main            # Experiments A and B: results/main_summary.md, main_measures.csv
python analyse.py --set main --tag e1   # the OpenAI extension
python analyse_e2.py                    # the genre follow-up
python script_numbers.py                # every figure used in the video
```

Re-running the *models* needs your own API access (see `../core/models.py`). Outputs will differ in detail, because the models are sampled and change over time. The published outputs are the ones the video reports.

## Limitations, in plain words

- Google's models weren't included. The OpenAI models were tested through the API with no system prompt, not through the ChatGPT app, which adds its own instructions.
- The oldest OpenAI snapshots tested are from mid- and late 2024 (GPT-4o mini, 18 Jul 2024; GPT-4o, 20 Nov 2024). That is after the period when "delve" was most noted (2023 to early 2024).
- The "ten models" figures pool the main study and the extension. Each arm's own pre-registered tests are reported separately.
- The automated count of invented facts covers numbers and dates only, and fell short of the pre-registered agreement bar against one human's blind reading of 60 outputs. That reading found *more* invention.
- 11 of the 83 lexicon patterns come from the author's own writing habits (the `author` category), a category kept from the original design.
- The prompts were single-turn. Vendor overlaps with model size and age.
- Codes such as D37 or Q3 in the designs refer to the project's own decision log. They're kept as an audit trail, and the decisions they record are described where they're used.

## Licence

The data and documents are licensed **CC BY 4.0** (please credit "Least Likely"), and the code **MIT**. See `LICENSE.md`.

Contact: hello@leastlikelyai.com
