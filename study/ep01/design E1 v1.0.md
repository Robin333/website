# Ep01 study extension E1, design v1.0 (FROZEN): the OpenAI models, and the em dash

_**Frozen 30 Oct 2026, approved by the author (D37), before any E1 main-run output existed.** v0.1 was written before any E1 output; v0.2 added the pilot (procedure only). The author's decision D36: add OpenAI's GPT models (the ones behind ChatGPT) and the em-dash giveaway. The frozen v1.0 study (`design v1.0.md`, seven models) is unchanged; E1 extends it with the same prompts and analysis, in separate data files._

## What was already seen before this design (honesty note)
- **DESC-1:** counts of the named words and phrases ("delve", "tapestry", "pivotal", the office classics) in the seven v1.0 models. All are zero.
- **DESC-2:** em dashes in the seven v1.0 models. Claude 5.5: 2 of 2,520 outputs. Claude Sonnet 4.6: 316 of 840. Qwen3-32B: 304 of 840. Nova: 14 of 1,680.
- **The route smoke test:** one invitation email from each GPT model. GPT-6 Sol's contained one em dash.

So every E1 hypothesis about dashes and named words is formed *after* seeing the seven-model data. The seven-model dash figures stay descriptive. Only the OpenAI-arm tests below are confirmatory.

## Models (3, one vendor, via an OpenAI-compatible API)

| Key | Snapshot served | Why it's in |
|---|---|---|
| `gpt-4o` | gpt-4o-2024-11-20 | The 2024 model behind most of the "delve" and em-dash complaints. Retired from ChatGPT in Feb 2026, still on the API. |
| `gpt-5.5` | gpt-5.5-2026-04-24 | ChatGPT's model for most of 2026 (removed 14 Oct 2026) |
| `gpt-6-sol` | gpt-6-sol-2026-09-22 | The current generation. ChatGPT's main model is "GPT-6"; the API provider lists several GPT-6 variants, and which one ChatGPT uses isn't confirmed. The video names the exact API model. |

- Every call is one user turn, with no system prompt and default sampling (no temperature or reasoning-effort setting). That's what an API user gets, not the ChatGPT app, which adds its own instructions.
- **The token cap is 4,000 from the start** (`--cap 4000`), because GPT-5.5 and GPT-6 Sol spend hidden reasoning tokens (DEV-1). `finish_reason` is checked for every output, and `reasoning_tokens` is recorded.

## Design (identical to v1.0)
- **Same 24 main scenarios, same prompts word for word** (`run.py`), same five repetitions.
  - **Experiment A:** 24 × brief (vague / specific) × instruction (plain / avoid clichés) × 3 models × 5 = **1,440 drafts**.
  - **Experiment B:** 24 × (clearer / more specific / Orwell check) × 3 × 5 = **1,080 rewrites**.
  - **Total: 2,520 calls**, written to `data/runs_main_e1.jsonl`.
- **Pilot:** the 4 pilot scenarios × 2 reps (168 calls), to `data/runs_pilot_e1.jsonl`. It checks the procedure only (truncation, empty replies, refusals). Pilot numbers are never findings.
- **Confound:** these three models differ in generation *and* size and price tier. Generation contrasts are model comparisons on identical prompts, not a measured trend over time.

## Measures
- **All v1.0 measures, unchanged:** lexicon v0.1 (frozen), prefab rate, invented specifics, questions, placeholders. The prefab rate is computed within the E1 outputs (topic-recurrence threshold as in v1.0).
- **New, pre-registered here:**
  - **`em_any`:** the output contains at least one em dash (U+2014). Also `em_per100`, em dashes per 100 words.
  - **`en_spaced_any`:** the output contains a spaced en dash (U+2013 with a space either side), the UK "en rule" used as a dash. Ranges such as "4–5" aren't counted.
  - **`ai_words_per100`:** hits from the lexicon's `ai_literature` + `ai_practitioner` lists per 100 words. These are the "AI words" people mock; the practitioner list is unsourced, so it's reported as such.
  - **Named-word counts** (descriptive): "delve", "tapestry", "pivotal", "game-changer", "low-hanging fruit", "in today's fast-paced world", per model.
- No prompt contains an em dash or a spaced en dash (checked for the v1.0 prompts, which E1 reuses).

## Pilot (30 Oct 2026, 168 calls, `data/runs_pilot_e1.jsonl`): procedure only
- **Clean:**
  - Every output finished normally (`stop`), with no empty replies and no refusals.
  - Hidden reasoning peaked at 333 tokens (GPT-5.5) and 233 (GPT-6 Sol), with means of 41 and 89. The largest output was 391 tokens, so the 4,000 cap leaves plenty of room.
  - The served snapshots were stable: gpt-4o-2024-11-20, gpt-5.5-2026-04-24, gpt-6-sol-2026-09-22.
- **The analysis code ran end to end** (`analyse.py --set pilot --tag e1`). The E1 table, Holm adjustment and ten-model descriptive table all work.
- **Sizing (hints only; pilot numbers are never findings):**
  - The replications and E1a ran in the same direction in 4 of 4 pilot scenarios.
  - **E1b (the GPT-4o vs GPT-6 Sol em-dash difference) looked small**: 2 of 4 scenarios, dz near 0. With 24 scenarios it may be underpowered. A null E1b is reported as "no clear difference between generations", not as "the same".
  - The dash *levels* are descriptive and need no test.
- **No change to the design** as a result of the pilot.

## Hypotheses
Thresholds as in v1.0: Holm-adjusted p < .05 *and* the 95% CI excludes 0. Holm is applied across the whole E1 table.

| # | Hypothesis (OpenAI arm, pooled over the three models unless stated) | Measure | What it does to the script |
|---|---|---|---|
| R-L2 | Vague briefs produce more stock phrasing than specific briefs (A, plain) | lexicon per 100 words | §3 "they gather where the information is missing" can say "in all four companies' models" |
| R-L3 | "More specific" invents facts more often than "clearer" (B) | share with an invented specific | §5 "It made one for you" holds for ChatGPT's models, or must be scoped |
| R-L4a | "Avoid clichés" cuts listed stock phrases (A, vague) | lexicon per 100 words | §5 |
| R-L5a | The Orwell check invents fewer facts than "more specific" (B) | share with an invented specific | §7: the tool works in ChatGPT's models, or the advice is scoped |
| R-L5b | The Orwell check asks more questions than "more specific" (B) | questions per output | §7 |
| E1a | GPT-4o uses more AI words than GPT-6 Sol (A, all conditions; directional) | `ai_words_per100` | §3: "the older ChatGPT model still did; the newest barely does", or no generation difference |
| E1b | GPT-4o and GPT-6 Sol differ in em-dash use (A, all conditions; two-sided) | `em_any` | the em-dash beat (see below) |

R-L4b and R-L4c are reported as in v1.0, without thresholds of their own. The judge coding and L6 are secondary and descriptive.

**Descriptive (no test):**
- dashes and named words for all ten models side by side (the seven v1.0 rows were seen first);
- the effect of "avoid clichés" on dashes;
- GPT-5.5 against the other two.

## What each result does to the script
- **The named words stay at or near zero in all three GPT models:** §3's "not once" extends to "ten models from four companies, including three generations of the models behind ChatGPT". It's stronger, and it answers "no ChatGPT?".
- **GPT-4o uses them, but GPT-6 Sol barely does (E1a supported):** §3 gains one line: the older ChatGPT model still reached for them, the newest hardly does. That partly answers "why are they missing?". Said as a model comparison, never "OpenAI trained them out".
- **GPT-6 Sol uses them often:** §3 changes. "Not once" is scoped to the other models, and ChatGPT's models become "the exception", the guilty party the author suspected. The thumbnail may change.
- **The em dash:**
  - If any GPT model uses it in a large share of outputs, it joins the opening ("Delve. Tapestry. —") and §3: "the em dash survives where the words didn't", with the per-model counts.
  - If it's rare in all three, it becomes "even the em dash is mostly gone, except in two of ten models".
- **A replication fails (R-L2 to R-L5):** the affected claim is scoped to the models where it held, and the contrary result is reported with equal prominence (research.md 6). If the Orwell check fails in ChatGPT's models, §7 must say so, because most viewers will use it there.
- **The sample line changes either way:** "seven models from three companies" becomes "ten models from four companies".

## Human validation
Not run for E1 (the author's decision, D37). The author's VAL-1 coding (60 outputs from the seven v1.0 models) stays the reference for what counts as invented content. E1 claims rest on the automated measures, scoped as in VAL-1 ("invented numbers and dates"), plus the LLM judge as a secondary measure. Nothing about the GPT models is described as human-validated.

## Reporting
- Rules as in v1.0. "The models we tested", never "AI" or "ChatGPT" on its own. Say "GPT-6 Sol, tested through the API".
- Published files: `runs_main_e1.jsonl`, `main_e1_measures.csv`, `main_e1_summary.md`, and this design.

## Approval
the author approved this design on 30 Oct 2026 (D37). The main run: `python lab/ep01/run.py --set main --reps 5 --models gpt-4o,gpt-5.5,gpt-6-sol --tag e1 --cap 4000`. Any change after this point is a reported deviation.
