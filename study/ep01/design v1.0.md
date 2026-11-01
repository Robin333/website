# Ep01 study design v1.0 (FROZEN): do AI models reach for stock phrases to cover gaps?

Status: **FROZEN 30 Oct 2026. Approved by the author ("Yes, run the study").** This is design v0.2 verbatim, plus three decisions made at approval:
1. Use only the models reachable through current access. No OpenAI or Google models (decision Q4).
2. Publication doesn't need to disclose how models were accessed (Q3). The methods note lists the model IDs and run dates.
3. The lexicon's "unlock … potential" moves from business to the author's terms, after the author confirmed it is one of their own habitual phrases (Q5).

Nothing changes after this point. Any further analysis is labelled exploratory.

---

# Ep01 study design v0.2: do AI models reach for stock phrases to cover gaps?

Status: **draft pre-registration, ready for the author's approval.** 30 Oct 2026. It supersedes `design v0.1.md`, which is kept for the audit trail. On approval: copy this file to `design v1.0.md`, set `"frozen": true` in the lexicon, then run the main study. Nothing below changes after the main run starts. Any later analysis is labelled exploratory.

## Changes from v0.1 (all made after the pilot and before any main-run data exists)

1. **Scenarios: 16 → 24.**
   - The pilot's scenario-level effect sizes for the stock-phrase tests (dz 0.74–1.08) imply that 9–17 scenarios are needed for 80% power.
   - 24 gives margin.
   - The 8 new scenarios (S17–S24) were written without reference to pilot outputs.
2. **New co-primary measure: prefabricated wording.**
   - It's defined by the data, not by our phrase list: a trigram is prefabricated if it appears (not copied from the prompt) in outputs for at least a quarter of the scenarios. That's wording that recurs whatever the topic, Orwell's "prefabricated hen-house".
   - Why: the pilot showed that current frontier models rarely use classic jargon ("move the dial": 0 of 112 drafts), so a fixed lexicon may measure yesterday's clichés.
   - The lexicon stays as a co-primary measure, and both are reported.
3. **L1 phrase ranking** uses vague-brief drafts only, ranked by how many different scenarios a phrase appears in. In v0.1 it was swamped by facts paraphrased from the specific briefs.
4. **Orwell check prompt changed** to ask for up to three questions, so it matches the script's demo (the cold-viewer found the mismatch). The pilot used the new wording.
5. **New secondary measure: response type** for Experiment B.
   - The pilot showed that some models invent facts *as labelled options* ("if you mean participation: '…from 60% to 85%'"), while others present a single confident rewrite.
   - The script must not treat these as the same thing.
   - Coded by an LLM judge with the rubric below, and validated by the author's blind hand-coding.
6. **Equivalence bounds for the "no change" hypotheses** (L4b, L4c), so that "doesn't add detail" is a tested claim, not an absence of evidence.

## Hypotheses

| ID | Hypothesis | Primary measure(s) | Supported if | Script beat |
|---|---|---|---|---|
| L1 | *(descriptive)* Which of the author's terms, and which recurring phrases, do models use? | share of vague-brief drafts; phrase ranking | (no test) | §2; the cold-open trio |
| L2 | Vague briefs produce more stock phrasing than specific briefs (A, plain) | lexicon per 100 words (core, excluding practitioner list); prefab rate | Holm-adjusted p < .05 and the CI excludes 0, for either measure | §5 "covering a gap" |
| L3 | "More specific" invents facts more often than "clearer" (B) | share of outputs with an invented specific | as L2 | §7 "it made it for you" |
| L4a | "Avoid clichés" cuts listed stock phrases (A, vague) | lexicon per 100 words | as L2 | §6 |
| L4b | …but doesn't add concrete detail | specifics per 100 words | 95% CI upper bound < +1.0 | §6 "can't prompt your way out" |
| L4c | …and doesn't cut prefabricated wording | prefab rate | 95% CI within ±0.02 | §6 |
| L5a | The Orwell check invents fewer facts than "more specific" (B) | share with an invented specific | as L2 | §7 |
| L5b | The Orwell check asks more questions than "more specific" (B) | questions per output | as L2 | §7 |
| L6 | *(descriptive)* Same-prompt wording overlap, within and across models | trigram Jaccard | (no test) | §3 supporting colour only |

The primary family for the Holm adjustment is L2 (two measures), L3, L4a, L5a and L5b: 6 tests. L4b and L4c are equivalence tests.

## Design (unchanged except for the scenario count)

**Models (7, from 3 vendors, via cloud APIs):**
- Claude Opus 5.5, Sonnet 5.5, Haiku 5.5 and Sonnet 4.6 (Anthropic)
- Nova Pro and Nova Lite (Amazon)
- Qwen3-32B (Alibaba)

Every call is one user turn with no system prompt and default sampling.

**Experiments:**
- **Experiment A:** 24 scenarios × brief (vague / specific) × instruction (plain / avoid clichés) × 7 models × 5 repetitions = **3,360 drafts**.
- **Experiment B:** 24 × (clearer / more specific / Orwell check) × 7 × 5 = **2,520 rewrites**.

**Main run: 5,880 calls.** Based on the pilot, that's about 0.4M input and 1.3M output tokens, and about 30–35 minutes of wall time with 8 workers. It's resumable.

**Confound to report, not hide:** vendor is partly confounded with model size and age. The Amazon and Qwen models tested are smaller or older-generation than the Claude 5.5 family. Results by model must be described as "these models", never as a vendor's general behaviour.

## Measures

The details are in `analyse.py`.
- **Lexicon rate:** hits per 100 words against `lexicon v0.1.json` (frozen at approval). There are four categories. The practitioner "AI tells" list is unsourced and is excluded from the core measure.
- **Prefab rate:** the share of an output's content trigrams that recur in outputs for at least a quarter of the scenarios (minimum 2), excluding wording copied from the prompt.
- **Invented specifics:** numbers, percentages, dates, weekdays, months and relative deadlines in *declarative* sentences that aren't in the prompt. Questions, list markers and bracketed placeholders are excluded. Placeholders are counted separately.
- **Questions:** the number of sentences ending in "?".
- **Concrete detail:** all specifics per 100 words.
- **Sameness:** word-trigram Jaccard overlap.
- **Response type (Experiment B, secondary):** coded by an LLM judge (Claude Opus 5.5, temperature default, rubric below) as:
  - `single_rewrite`
  - `options`
  - `questions_first`
  - `other`

  The judge also records `invented_as`: `assertion`, `example`, or `none`.
  - **Rubric:** "single_rewrite = one rewritten sentence or paragraph presented as the answer. options = two or more alternative rewrites, usually conditional on what the writer meant. questions_first = asks the writer questions before (or instead of) rewriting. invented_as = whether facts not in the input (numbers, dates, targets) are stated as the writer's position (assertion) or offered as illustrations or options (example)."
  - **Limitation:** the judge is from the same vendor as four of the models being judged. Its labels are validated against human coding.

**Human validation.** the author blind-codes a random 60 Experiment B outputs (stratified by instruction) for (a) an invented fact present (yes/no) and (b) response type, without seeing the code's or the judge's labels. We report percentage agreement and Cohen's kappa for both. If regex/human agreement is below 85%, or kappa is below 0.6, the measure is fixed and the fix is reported.

## Analysis

The method is unchanged from v0.1:
- the scenario is the unit of inference
- paired scenario-level differences
- exact or Monte-Carlo sign-flip permutation tests
- bootstrap CIs over scenarios
- "same direction in k of 24 scenarios"
- per-model tables always reported

## What the pilot hinted at

These hints are **not findings**. They come from 4 scenarios, and the pilot is excluded from the main analysis:
- Classic jargon (the author's terms) was almost absent from the models' drafts.
- The Amazon and Qwen models filled gaps with generic enthusiasm ("Exciting news!", "crucial for our continued success"). When asked to be "more specific", they often added *more* abstract wording rather than facts.
- The Claude models filled drafting gaps with visible placeholders ("[date]"). When asked to be "more specific", most of them invented numbers, often as labelled options.
- "Avoid clichés" cut listed clichés sharply but didn't change prefabricated wording or concrete detail.
- The Orwell check produced questions in 88% of outputs and invented facts in 9%.

If the main run confirms these, the episode gains a stronger twist: the obvious clichés have been trained out, but the gap they covered hasn't gone away. It's now covered by better camouflage, either more abstract filler or confident invented detail.

## What each result does to the script

This is as in v0.1, plus:
- If the response-type coding shows that invented facts are mostly offered as *options*, then §7's line "It made it for you" becomes "It offers to make it for you, and a busy reader takes the first option". This would need care and testing.
- If L1 confirms the near-absence of the author's terms, then §2 doesn't claim that models use the author's phrases. Instead it says the models have been trained away from them, which sets up the camouflage twist in §5.

## Reporting

- Publish the prompts, scenarios, lexicon, code, raw outputs and the human-coding sheet with the video.
- Report null and contrary results with equal prominence.
- Always use "the seven models we tested", never "AI".
