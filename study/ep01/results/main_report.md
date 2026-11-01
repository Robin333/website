# Ep01 study: main results report

Run 30 Oct 2026. The design was frozen beforehand (`design v1.0.md`). This report uses the **final, corrected data** (DEV-1 and DEV-2), records the wording decision DEV-3, and incorporates the author's blind human validation (VAL-1). All four are in `deviations.md`. The full tables are in `main_summary.md`, and the per-output measures in `main_measures.csv`. The script figures are computed in `script_numbers.json`.

**Scale:** 5,880 outputs: 3,360 drafts and 2,520 rewrites, from **7 models from 3 companies** (Anthropic Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 and Sonnet 4.6; Amazon Nova Pro and Nova Lite; Alibaba Qwen3-32B), across **24 everyday business-writing tasks**, 5 repetitions each. A further 1,200 outputs were regenerated under DEV-1.

**Statistics:**
- The unit of analysis is the task, not the output.
- Monte-Carlo sign-flip tests (20,000 flips) and bootstrap 95% CIs over tasks.
- Holm adjustment across the 6 primary tests.

**Status:** final.
- **Human validation (VAL-1):** the author's blind coding of 60 rewrites reproduced every finding, with larger differences.
- The automated invented-fact count agreed with the human 80% of the time (kappa 0.51), below the pre-registered bar. The disagreements were about scope: the human also counted invented features and plans. So the automated measure is reported by its true scope, **invented numbers, dates and deadlines**, and it is conservative.
- The human "invented-as" column was invalid because its instruction was ambiguous.

## Headlines

1. **The obvious clichés barely appear.** (The study has no older baseline, so it can't show that they were trained out.)
   - "Heighten engagement", "move the dial", "unlock potential", "unified approach" and "at a high level" appeared **0 times in 1,680** drafts written from vague briefs.
   - Any of the author's Copilot-reported terms appeared in 44 of 1,680 (2.6%), almost all "optimise" or "leverage".
   - "Unlock" never appears as a word. Its one substring match is the hashtag #AchievementUnlocked.
   - The literature-sourced "AI words" (delve, underscore, showcase, meticulous…) appeared in 6 of 1,680 vague-brief drafts.
2. **Prefabricated phrasing hasn't gone away.** The wording that recurs across unrelated tasks is now polite filler: "let me know", "feel free", "look forward to", "next steps", "work together". (Descriptive, L1.)
3. **Vaguer briefs produce more stock phrasing (L2: confirmed).**
   - Core stock-phrase rate is **2.1× higher** with a vague brief (0.34 against 0.16 per 100 words), higher in 18 of 24 tasks (Holm p ≤ 0.0003).
   - Prefabricated wording is **+33%** (0.052 against 0.039), higher in 16 of 24 tasks (Holm p ≤ 0.0054).
4. **Asking for "more specific" invents facts (L3: confirmed).** **53%** of "make it more specific" rewrites added a number, date, deadline or target that wasn't in the original, against **10%** for "make it clearer". It was higher in **24 of 24 tasks** (Holm p ≤ 0.0003).
5. **Invention often arrives as a menu of options**, every one a decision the writer hadn't made.
   - In the author's blind coding, 7 of 20 "more specific" replies were options, all with invented content, and all from Claude models.
   - The LLM judge put it at 37% of "more specific" rewrites offering invented facts as examples or options, against 24% stating them as the writer's position. The human check of that split was invalid (VAL-1), so no figure is quoted.
6. **Two kinds of camouflage, by model.**
   - **The Claude models** invented facts in 71–93% of "more specific" rewrites, with few stock phrases (0.2–0.6 per 100 words).
   - **The Amazon and Qwen models** rarely invented numbers or dates (5–18%). Instead they piled on stock wording: 2.7–4.1 per 100 words, a rate that includes phrases kept from the input sentence.
   - **Human reading (VAL-1)** found that their filler invents content too: features, actions and claims nobody made.
   - *(Vendor is confounded with model size and age; see Limitations.)*
7. **"Avoid clichés" works on the clichés, not on the gap (L4).**
   - **L4a confirmed:** listed clichés fell **79%**, lower in 22 of 24 tasks (Holm p ≤ 0.0003).
   - **L4c (equivalence) supported:** prefabricated wording fell 15% (0.052 to 0.044), with the 95% CI inside the pre-registered ±0.02 bound.
   - **L4b NOT supported:** we predicted no change in concrete detail. It *rose*, by +0.67 specifics per 100 words (95% CI +0.28 to +1.08, past the +1.0 bound).
   - **Exploratory (not pre-registered):** with a vague brief there were no facts to add, so that detail was **invented**. Invented specifics per 100 words rose **37%** (1.81 to 2.49), higher in 18 of 24 tasks (p 0.003, unadjusted).
8. **The Orwell check works (L5: confirmed).**
   - It got questions back in **100%** of replies (840 of 840), an average of 5.7 question-sentences, against 15% for "more specific".
   - It invented facts in **3%**, against 53%. Both were better in **24 of 24 tasks** (Holm p ≤ 0.0003).
   - The judge coded 99% as "questions first", with no invented facts stated as the writer's position.

## Pre-registered hypotheses: verdicts

| ID | Hypothesis | Verdict |
|---|---|---|
| L1 | The author's terms and stock phrases in drafts (descriptive) | The author's terms are almost absent. The new stock phrases are polite filler. |
| L2 | Vague briefs mean more stock phrasing | **Confirmed** on both measures |
| L3 | "More specific" invents more than "clearer" | **Confirmed**, 24 of 24 |
| L4a | "Avoid clichés" cuts listed clichés | **Confirmed**, 22 of 24 |
| L4b | …without adding concrete detail | **Not supported.** Detail rose, and in vague briefs it was invented (exploratory). |
| L4c | …and without cutting prefabricated wording | **Supported** (equivalence) |
| L5a | The Orwell check invents fewer facts than "more specific" | **Confirmed**, 24 of 24 |
| L5b | The Orwell check asks more questions | **Confirmed**, 24 of 24 |
| L6 | Sameness (descriptive) | The same model repeated overlaps about 3.6× more than different models do (trigram Jaccard about 0.20 against 0.05). Each model has its own house style. |
| Response type (secondary) | Invention arrives as options or as decisions? | Often as options. The judge put it at 37% against 24%, and the human codes had 7 of 20 as options. The human invented-as check was invalid, so the claim is made only qualitatively (DEV-3). |
| Human validation (VAL-1) | Does a blind human reading reproduce the results? | **Yes, with larger differences.** Invented content: "more specific" 16 of 20, "clearer" 4 of 20, Orwell check 0 of 20. |

## What changed in the script (v0.4, per the pre-registered table)

- **§2:** doesn't claim that models use the author's phrases.
- **v0.4–v0.7 (study-led from v0.6):** concedes the objection with the data (0 in 1,680). Then the twist:
  - the habit remains: new phrases, and 2× stock phrasing on vague briefs
  - "avoid clichés" cuts them by 80% and adds invented detail (labelled exploratory)
  - the two camouflages are shown with real outputs
- **§7:** real outputs replace the invented illustrations. "More than half… about one in ten". The general claim is softened to "a menu of options… decisions you hadn't made". The Orwell check gets "questions every single time, almost never made facts up".
- **The named tool is validated.** No redesign is needed.

## Limitations

- **Seven models from three companies.** No OpenAI or Google models. Always say "the models we tested".
- **Vendor is confounded with size and age.** The Amazon and Qwen models tested are smaller or older-generation.
- **Text-pattern measures.** The invented-fact count is a regex for numbers, dates and deadlines only. It misses invented actions or features, and fell below the pre-registered agreement bar against the human coding (VAL-1). It's conservative: the human found more invention.
- **Two code fixes after the main run** (DEV-1, DEV-2), both disclosed. Both made the results *stronger* for L5b, and DEV-2 removed false "inventions" in Orwell-check replies. Neither changed any verdict.
- **Single-turn prompts,** with no system prompt and default settings. Real use often includes more context.
- **The scenarios were written by us.** They're generic business tasks.

## Reproducibility

Prompts, scenarios, lexicon, code, raw outputs, judge labels and deviations are all in `lab/ep01/`. Re-run with `python lab/ep01/analyse.py --set main` and `python lab/ep01/script_numbers.py`.
