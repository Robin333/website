# Ep01 study: deviations from the frozen design (`design v1.0.md`)

Every departure from the frozen design is recorded here and reported in the published methods note.

## DEV-1: Output truncation by the token limit, regenerated (30 Oct 2026)

**What happened**
- The runner capped output at 700 tokens (Experiment A) and 500 tokens (Experiment B).
- The Claude 5.5 models (Opus, Sonnet and Haiku) spend hidden reasoning tokens before answering, and those count against the cap.
- As a result, many of their outputs stopped mid-answer, with `stop_reason = max_tokens`.
- In the main run this hit 10 model × condition cells, worst in the Orwell check: 117, 108 and 119 of 120 outputs truncated for Haiku 5.5, Opus 5.5 and Sonnet 5.5.

**Why it matters**
- Truncated replies under-count questions, which biases *against* L5b.
- They may also under-count invented facts, if the cut-off removed an example rewrite. That could bias *in favour of* L5a.
- The prompt asked for under 150 words, so the cap was meant as a safety limit, not as a measure.

**How it was missed**
- The pilot showed the same pattern: 7 of 8 Orwell-check outputs were truncated for each of these models.
- The pilot checks looked at outputs and measures, but not at `stop_reason`.
- **Lesson:** check stop reasons during the pilot. This has been added to `brand/research.md`.

**Correction**
- Every output in each affected cell (all 120, not just the truncated ones) was regenerated with a 4,000-token cap.
- That gives each cell a clean sample under a single setting: 1,200 calls, flagged `regen: truncation-v1` in `data/runs_main.jsonl`. The original records are kept above them for the audit trail.
- Cells where no output hit the cap were left unchanged, because raising a cap that was never reached doesn't change those outputs.
- The judge re-codes the regenerated outputs, and labels are matched to the exact output they coded.

**Reporting**
- The results are reported on the corrected data.
- The pre-correction results are kept in `results/main_summary_pre_dev1.md` for comparison.

## DEV-2: Sentence splitting broken by markdown bold (30 Oct 2026)

**What happened**
- Many models write questions in bold, e.g. `**What does "engagement" mean here?** The words…`.
- The pre-registered measures split replies into sentences and treat a sentence ending in "?" as a question. They also skip questions when counting invented facts.
- The splitter didn't break after `?**`, so a bold question merged with the next sentence and wasn't counted.

**Why it matters**
- Questions were under-counted, which biased *against* L5b. Claude Haiku 5.5's Orwell-check average was 1.2 questions before the fix and 4.1 after.
- Numbers inside bold questions could be counted as invented facts, which biased *against* L5a.
- So both errors were conservative, but they were still errors.

**Correction**
- Markdown emphasis markers are removed before sentence splitting (`analyse.sentences`).
- This brings the code into line with the pre-registered definition. It doesn't change the definition.
- **Part 1 (bold questions):** Orwell-check replies with at least one question went from 94% to 100% (840 of 840). Mean question-sentences went from 4.85 to 5.70.
- **Part 2 (bold list numbers):** the same root cause hid list numbers. In "**1.**" the bold markers stopped the list-marker filter, so 1, 2 and 3 were counted as invented facts. Emphasis is now stripped before list markers are removed, which matches the frozen definition ("list markers… are excluded").
  - Orwell-check invented facts went from 8% to **3%** (24 of 840). Opus 5.5 went from 38% to 9%.
  - Without this fix, the script would have said "about one time in ten" instead of "almost never". (Corrected 30 Oct 2026, after the v0.4 fact-check caught an error in this log entry.)
- The pre-fix summary is kept as `results/main_summary_pre_dev2.md`.
- The blind hand-coding (the author) independently checks these measures.

## DEV-3: How the pre-registered "options" rule was applied in §7 (30 Oct 2026)

**The rule (design v1.0)**
- If the response-type coding showed that invented facts were mostly offered as options, §7's line "It made it for you" was to become "It offered to make it for you, and a busy reader takes the first option".

**What happened**
- The rule was triggered. Of "more specific" rewrites, 37% offered invented facts as examples or options, against 24% that stated them as the writer's position.

**How it was applied**
- **The shown example keeps its decisive framing,** because that real output *did* state invented facts as the writer's position (judge: assertion). It now reads in full: "It made one for you, and then offered to change it if you told it more." That includes the model's own follow-up offer.
- **The general claim spoken over the study numbers says invented facts *often* come as a menu of options,** each of which is still a decision the writer hadn't made. All 7 of the human-coded "menu" replies to "more specific" came from Claude models. ("Usually" was corrected to "often" after the v0.6 fact-check.)
- **The prescribed clause "a busy reader takes the first option" was dropped.** It's an untested claim about readers, which this study can't support.

**Why it's reported here:** this is a wording choice that departs from the letter of a frozen rule, though it keeps the rule's intent.

## VAL-1: Human validation outcome, and what changed as a result (30 Oct 2026)

**Procedure**
- The author blind-coded 60 Experiment B replies (20 per instruction, spread across models).
- The instruction and model were hidden. The key is in `data/_coding_key_main.json`, and the comparison in `data/_coding_compare_main.json`.

**Pre-registered bar:** agreement of at least 85% and kappa of at least 0.6, or "the measure is fixed and the fix is reported".

| Measure | Agreement | Kappa | Verdict |
|---|---|---|---|
| D: invented fact (the author vs regex; the judge gives identical results) | 80% | 0.51 | **Below the bar** |
| E: response type (the author vs judge) | 82% | 0.73 | Below the agreement bar, above the kappa bar |
| F: invented-as (the author vs judge) | 35% | 0.10 | **Invalid comparison.** the author coded "Example" on 26 replies that were also coded as having *no* invented fact, against the sheet's instruction. The F instruction was ambiguous: it was read as "does the reply offer example rewrites?". This is a codebook failure, not evidence about the judge. |

**Diagnosis of D: the 12 disagreements are about the *construct*, not about errors**
- **9 where the author found invention and the regex didn't.** the author counted invented *substance*: features, actions and plans nobody gave. For example: "a redesigned user interface, enhanced performance algorithms…"; "targeted curriculum enhancements… specialized training for teachers"; "bold typography and a clean color palette". The regex counts only numbers, dates and deadlines, by design. Six of the nine came from Amazon and Qwen "more specific" replies. The other three were Claude "clearer" replies. (Corrected 30 Oct 2026 after the v0.6 fact-check.)
- **3 where the regex counted invention and the author didn't.** Two were invented numbers inside clearly labelled hypothetical templates ("For an app or software: …"). One was a regex false positive inside a question's explanation ("next month's target").

**Human-coded rates (n = 20 per arm, Wilson 95% CI)**

| Condition | Invented content |
|---|---|
| "More specific" | **80% [58–92%]** |
| "Clearer" | 20% [8–42%] |
| Orwell check | **0% [0–16%]** |

The author coded all 20 Orwell-check replies as "questions first". These rates show the same ordering as the automated measures, with *larger* differences. The automated count is conservative.

**Fix (reported, not hidden)**
1. The automated invented-fact measure is described by its actual scope wherever it's reported: **"invented numbers, dates and deadlines"**. The script's spoken claim is narrowed to match.
2. The author's coding is reported as an independent, broader human measure ("invented content"), with its small-sample CIs.
3. F isn't used. Claims about options versus assertions now rest on E (the human's own codes: 7 of 20 "more specific" replies were options), and are made only qualitatively ("often").
4. **The camouflage finding is revised in the light of the human reading.** The "filler" models also invent, just vaguely: promises and features rather than numbers. The script now says so.


## DESC-1: Descriptive phrase counts for script v0.8 (30 Oct 2026)

**What:** the author cut their own phrases from the episode (D35), so script v0.8 names other phrases and gives their counts. The counts use the frozen lexicon v0.1 and the same record selection as every other script number (the latest valid record per key). There are no new model calls. They are computed in `script_numbers.py` and written to `results/script_numbers_v0.8.json` (keys `TELL_COUNTS_ALL`, `MILD_COUNTS`, `LEX_TERMS_*`). The v0.7 keys reproduce exactly.

**Why it is a deviation:** these counts weren't pre-registered as hypotheses, and **the phrases named on screen were chosen after seeing the data.**
- The zeros ("in today's fast-paced world", "game-changer", "low-hanging fruit", "delve", "tapestry") are true across all 5,880 outputs. But a viewer could fairly suspect cherry-picking.

**How it is reported:**
1. The script names the phrases that *do* appear, alongside the zeros ("reach out", "excited to announce").
2. The description lists every lexicon term with its count.
3. The SOURCE lines label these counts DESC-1.
4. No inferential claim rests on them. The pre-registered stock-phrase tests (L2, L4a) are unchanged.

**DESC-1 update for script v0.9 (after the v0.8 fact-check, `reviews/_factcheck_v0.8.md`).** The numbers are in `results/script_numbers_v0.9.json`.
- **The spoken zeros** are "delve", "tapestry", "a pivotal moment", "game-changer", "low-hanging fruit" and "in today's fast-paced world". Each is 0 across all 5,880 outputs, so the zero holds in every condition, including the 1,680 drafts told to avoid clichés. The fact-checker reproduced the zeros independently over the raw file, including superseded DEV-1 records and the prompt fields.
- **One pattern per phrase:** the lexicon's own. "Reach out" is 61 of 840 vague-brief drafts with no style instruction. The spoken "excited to announce" is the exact phrase, 31 of 840. (The lexicon group "excited/thrilled/delighted to announce/share/launch/introduce" is 58.)
- **Per-term counts** are split into drafts (A) and rewrites (B). For B, the count shows how many hits were already in the input sentence; for example, "operational excellence" comes from one input sentence.
- **Housekeeping:**
  - "game-changer" sits in two lexicon categories (`business` and `ai_practitioner`), against the lexicon's one-category rule. Its count is 0, so no total is affected.
  - The single "synergy" hit is a mention ("avoids vague language about synergy"), not a use.
- **"About twice as many"** now refers to the full list, as spoken ("the phrases on our list"): L2, 0.78 vs 0.40 per 100 words, 1.9×, vague higher in 19 of 24 tasks. The core-list version (2.1×, 18 of 24) is reported alongside it.
- **Public source for the opening's AI words:** S11, Wikipedia "Signs of AI writing" (accessed 30 Oct 2026). It lists "delve", "tapestry" and "pivotal".

## DESC-2: First look at em dashes in the existing outputs (30 Oct 2026)

**What:** after the v0.9 script, the author asked to add the em-dash "giveaway" and an OpenAI (ChatGPT) arm. Before any OpenAI design was written, I counted em dashes (U+2014) in the 5,880 existing outputs (latest valid record per key; no model calls).

| Model | Outputs with an em dash |
|---|---|
| Claude Haiku 5.5 | 0 of 840 |
| Claude Sonnet 5.5 | 0 of 840 |
| Claude Opus 5.5 | 2 of 840 |
| Claude Sonnet 4.6 | 316 of 840 |
| Qwen3-32B | 304 of 840 |
| Nova Pro | 6 of 840 |
| Nova Lite | 8 of 840 |

- No prompt contained an em dash.
- Spaced en dashes (the UK "en rule" used as a dash) were counted separately. Claude Sonnet 4.6 used them in 42% of drafts; the Claude 5.5 models in up to 6%.

**Why it's logged here:** the em dash wasn't a pre-registered measure. Any OpenAI-arm hypothesis about dashes is now formed *after* seeing these numbers. The extension's pre-registration must say so, and must treat the seven-model dash figures as descriptive.

**Scratch code:** `%TEMP%\so_ep01_emdash.py`. It will move into `script_numbers.py` if the script uses these figures.

## E1 (OpenAI arm, design E1 v1.0): deviations and notes (30 Oct 2026)
- **DEV-E1-1:** three GPT-4o rewrites (`B|S15|-|clearer|gpt-4o|1–3`) ended with `finish_reason: content_filter`, the platform's safety filter. All three are complete one-sentence rewrites, so they are kept unchanged and none was regenerated.
- **No E1 human coding (D37).** The judge's response-type labels are validated only on the v1.0 models (VAL-1).
- **ALL10_* figures** (the narration's "ten models") pool v1.0 and E1 descriptively. Each arm's own pre-registered tests stand on their own (`main_summary.md`, `main_e1_summary.md`).
- The results are in `results/E1 results note.md`.
- **DEV-E1-2: markdown headings counted as invented numbers. Found by the v1.0 fact-check (`reviews/_factcheck_v1.0.md`).**
  - **What happened:** nine GPT-4o Orwell-check replies numbered their questions as headings ("### 1.", "### 2.", "### 3."). The invented-specifics measure read "1, 2, 3" as invented numbers, because the list-marker rule didn't expect a heading mark in front. It's the same family as DEV-2.
  - **The fix:** `analyse.specifics` now strips heading marks before list markers.
  - **Effect on the frozen seven-model results:** none of the 5,880 v1.0 outputs changes (checked: 0 differ), because no v1.0 output uses that format.
  - **Effect on E1:**
    - GPT-4o's Orwell-check invention falls from 8% to 0%. The three GPT models go to 0 of 360, and the ten-model figure from 33 of 1,200 (2.8%) to 24 of 1,200 (2.0%).
    - R-L5a stays supported (0% vs 15%). Other Holm-adjusted p values shift slightly, because the family changed.
  - **Files:** the pre-fix files are kept as `results/main_e1_pre_deve1_2_*`. The new figures are in `results/script_numbers_v1.1.json`; v1.0 is kept.
- **Erratum (frozen `design E1 v1.0.md`, context table, not a design change):**
  - "GPT-5.5 was ChatGPT's model for most of 2026" overstates. It was a ChatGPT model in 2026 until its removal on 14 Oct 2026.
  - "GPT-4o, the 'delve' model" overstates. Wikipedia dates "delve" to the GPT-4 era (2023 to mid-2024). GPT-4o was ChatGPT's main model from May 2024 to Aug 2025.
  - The comments in `models.py` are corrected. The frozen design is left as it was, with this erratum.
- **Monte Carlo p values:** with more than 16 scenarios, the sign-flip p values use 20,000 random flips. So p values can differ in the third decimal between `main_e1_summary.md` and `script_numbers_*.json`, because the tests run in a different order. No support decision depends on that difference.

## E2 genre probe (design E2 v1.0, 30 Oct 2026)
- Run on the author's comment C1 ("figure out what may be going on"). The design was frozen by Claude before any data; the author is to ratify it (D38).
- It's exploratory and descriptive only: no hypothesis tests.
- The results are in `results/E2 results note.md`.
- GPT-4o mini was added to `EXTRA_MODELS` for E2 only.
