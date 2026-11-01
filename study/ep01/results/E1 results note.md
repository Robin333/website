# Ep01 E1 results note: three OpenAI models (30 Oct 2026)

_Design: `design E1 v1.0.md` (frozen, D37). Data: `data/runs_main_e1.jsonl` (2,520 outputs), `data/judge_main_e1.jsonl`. Tables: `main_e1_summary.md`. Script figures: `script_numbers_v1.0.json` (`E1_*`, `ALL_*`, `ALL10_*`)._

## Run
- 2,520 of 2,520 calls succeeded, with no errors, no empty replies and no truncation. The largest output was 510 tokens; hidden reasoning peaked at 362.
- Snapshots served: gpt-4o-2024-11-20, gpt-5.5-2026-04-24, gpt-6-sol-2026-09-22.
- **Deviation note (DEV-E1-1):** three GPT-4o outputs (`B|S15|-|clearer|gpt-4o|1–3`) ended with `finish_reason: content_filter`, the platform's safety filter. All three are complete one-sentence rewrites, ending in a closing quote and full stop, so they are kept unchanged. The trigger is unknown ("keep things ticking over"?).

## Pre-registered tests (Holm across the E1 table; threshold: Holm p < .05 and the CI excludes 0)

| Test | Result |
|---|---|
| R-L2: vague briefs, more stock phrases | **Supported:** 0.64 vs 0.38 per 100 words, 1.7×, 17 of 24 tasks |
| R-L2b, R-L2c | **Supported** |
| R-L4a: "avoid clichés" cuts listed phrases | **Supported:** −79%, 22 of 24 |
| R-L4b: "avoid clichés" adds concrete detail | **Detail increased** (+0.6 per 100 words). Same direction as v1.0, where the pre-registered "no change" wasn't supported either |
| R-L4c: prefab wording unchanged | Not supported as a cut (the CI includes 0), as in v1.0 |
| R-L3a: "more specific" invents more than "clearer" | **Supported:** 15% vs 1%, 14 of 24 |
| R-L5a: the Orwell check invents less than "more specific" | **Supported pooled:** 2.5% vs 15%. **Not in GPT-4o:** 8% vs 2% |
| R-L5b: the Orwell check asks more questions | **Supported:** 24 of 24. It asked in 100% of replies for all three models |
| E1a: GPT-4o uses more AI words than GPT-6 Sol | **Supported:** 0.42 vs 0.01 per 100 words, 18 of 24 |
| E1b: GPT-4o and GPT-6 Sol differ in em dashes | **Supported:** drafts 29% vs 9%, 16 of 24 |

## Descriptive
- **Named words:** "delve", "tapestry", "pivotal", "game-changer", "low-hanging fruit" and "in today's fast-paced world" are 0 in all 2,520 GPT outputs. Across all ten models, that's 0 in 8,400.
- **The AI words GPT-4o did use:** "streamline", "enhance", "foster", "seamless", "elevate". These are the milder practitioner-list words.
- **Em dashes (share of outputs):**

  | Models | Outputs with an em dash |
  |---|---|
  | Claude 5.5 (Haiku, Sonnet, Opus) | 2 of 2,520 |
  | GPT-4o | 19% |
  | GPT-5.5 | 13% |
  | GPT-6 Sol | 11% |
  | All GPT models | 360 of 2,520 |
  | Claude Sonnet 4.6 | 38% |
  | Qwen3-32B | 36% |
  | Nova | 1% |

  The GPT models sit in the middle.
- **Camouflage in the GPT models ("more specific"):**
  - GPT-4o invents a number or date in 2% of rewrites, with 3.17 listed phrases per 100 words: vague filler, like Nova and Qwen.
  - GPT-5.5 invents in 29% (0.59 listed phrases per 100 words); GPT-6 Sol in 14% (0.03).
- **Judge (secondary; validated on the v1.0 models only):** the GPT models never offered options. When they invented, they stated it as the writer's position: GPT-4o 8%, GPT-5.5 42%, GPT-6 Sol 37%.

## What the pre-registered table says changes in the script
- **The named words stay at zero in all three GPT models**, so §3's "not once" extends to ten models from four companies, including GPT-4o.
- **E1a is supported**, so §3 gains the line "GPT-4o reached for words like these most; the newest hardly at all".
- **The em dash is in a large share of some models' outputs**, so it joins the opening and §3, with per-model figures. The honest headline: "it depends on the model". ChatGPT's models aren't the heaviest users here.
- **Every replication holds pooled.** The sample line becomes "ten models from four companies". The spoken §5 and §7 figures move to all ten models (`ALL10_*`, descriptive pooling; each arm's own tests are above).
- **Scoped claims:**
  - the "menu of options" is a Claude-model behaviour;
  - the Orwell check's lower invention doesn't hold for GPT-4o (8%), so the description must say so;
  - The author's hand reading covered the first seven models only.

## Not claimed
Nothing here says what the ChatGPT app does (it adds its own instructions), and nothing says "OpenAI trained them out". These are comparisons between models on identical prompts.

## Correction (30 Oct 2026, DEV-E1-2)
The v1.0 fact-check found that GPT-4o's 8% Orwell-check "invention" was a measurement artefact: "### 1." question headings were read as invented numbers.
- **After the fix:** the GPT models' Orwell-check replies invented a number or date in 0 of 360, and all ten models together in 24 of 1,200 (2.0%).
- **R-L5a is supported in all three GPT models,** so the earlier "not in GPT-4o" scoping and the description caveat are withdrawn.
- The figures are in `script_numbers_v1.1.json`. The pre-fix files are kept as `main_e1_pre_deve1_2_*`.
