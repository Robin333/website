# Ep01 probe E2, design v1.0 (FROZEN before any data): does "delve" come back outside business writing?

_30 Oct 2026. The author's comment C1 on script v1.1: "You're going to need to figure out what may be going on here. It definitely used to use terms like 'delve' a lot. Is it the types of writing tasks we are asking it to do? Have OpenAI adapted the model? Or something else?" This probe tests the task-type explanation. It's frozen by Claude before any E2 output exists, under that instruction; the author to ratify. It's **exploratory and descriptive**: no confirmatory tests._

## What's already known (desk research, 30 Oct 2026)
- **S11 (Wikipedia, "Signs of AI writing"):**
  - "Delve" belongs to the "2023 to mid-2024 (GPT-4)" vocabulary. It was "famously overused by ChatGPT in 2023 and early 2024", "became less frequent later in 2024, then dropped off sharply in 2025".
  - The studies behind these lists "analyzed scientific abstracts or fiction".
  - The GPT-4o list (mid-2024 to mid-2025) is "align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant". E1's GPT-4o used "enhance", "foster" and "streamline" most.
- **S6 (Kobak et al.):** the "delves" excess was measured in 2024 biomedical abstracts.
- **The API provider:** the GPT-4 era models (GPT-4, GPT-4 Turbo, GPT-3.5) aren't available (HTTP 500 on 30 Oct 2026). The earliest OpenAI snapshot available is gpt-4o-mini-2024-07-18, then gpt-4o-2024-11-20.
- **E1's tasks were business messages.** E1 found "delve", "tapestry" and "pivotal" at 0 in 8,400 outputs, 0 of them in GPT-4o.

## Question
In the genres where these words were documented (abstracts, encyclopedia-style text, fiction, essays, explainers), do OpenAI's models use them, when they don't in business messages?

## Models (OpenAI only, as the question is about ChatGPT)
| Key | Snapshot | Why |
|---|---|---|
| `gpt-4o-mini` | gpt-4o-mini-2024-07-18 | The earliest OpenAI snapshot available, the closest to the "delve" era |
| `gpt-4o` | gpt-4o-2024-11-20 | The E1 GPT-4o |
| `gpt-6-sol` | gpt-6-sol-2026-09-22 | The E1 current-generation model |

One user turn, no system prompt, default sampling, a 4,000-token cap, `finish_reason` checked (as E1).

## Prompts (6 genres × 3 topics = 18, written before any output)
1. **Scientific abstract:** "Write a 150-word abstract for a research paper on {t}." Topics:
   - sleep and memory in teenagers
   - urban heat islands
   - soil microbes and crop yields
2. **Encyclopedia-style introduction:** "Write a 150-word encyclopedia-style introduction to {t}." Topics:
   - the city of Porto
   - the Silk Road
   - the Highland games
3. **Essay opening:** "Write the opening paragraph of an essay on {t}. Keep it under 150 words." Topics:
   - the future of remote work
   - why cities need more trees
   - the ethics of self-driving cars
4. **Fiction opening:** "Write the first 150 words of a short story about {t}." Topics:
   - a lighthouse keeper's last night on duty
   - a child who finds an old map
   - a chef who loses their sense of taste
5. **Explainer:** "Explain {t} to a general audience in about 150 words." Topics:
   - how vaccines train the immune system
   - why the sky is blue
   - how inflation works
6. **Business control:** E1's own vague-brief, plain-instruction prompts, word for word, for:
   - S06, an internal announcement about a new IT helpdesk system
   - S08, a LinkedIn post about a team achievement
   - S16, a short strategy statement for my team's plan next year

5 repetitions each: 18 × 3 models × 5 = **270 calls**, written to `data/runs_e2.jsonl`.

## Measures (fixed now)
1. **Primary: `delve_any`.** The output contains "delve", "delves", "delved" or "delving".
2. **The spoken three:** the output contains any of "delve", "tapestry" or "pivotal".
3. **Distinctive GPT-4-era words**, from S11's 2023-to-mid-2024 list: delve, tapestry, pivotal, testament, intricate or intricacies, interplay, meticulous or meticulously, underscore, boast(s), garner, bolstered, vibrant, enduring.
   - Very common words on that list are excluded as too frequent in ordinary prose: "additionally", "crucial", "key", "landscape", "valuable", "emphasizing".
   - Reported as the share of outputs with any of them, and per 100 words.
4. **Em dash:** the share of outputs with at least one.

## Analysis (descriptive only)
- Counts and shares by genre × model, with Wilson 95% CIs for the shares. Each genre cell has 15 outputs per model.
- Comparison: the five non-business genres pooled against the business control, per model.
- No p values. The probe is small, and its job is to explain, not to confirm.

## What each result does to the script (§3, the GPT-4o line, C1)
- **The words appear in some non-business genres but stay near zero in the business control:** §3 adds a line saying that these words belong to certain kinds of writing. In business messages even GPT-4o didn't use them, but ask for an abstract or a story and some come back. The answer to C1 is the task type, together with S11's dating.
- **They stay near zero everywhere, in all three models:** §3 says the "delve" habit belonged to ChatGPT's 2023 model, which can no longer be tested, and had faded by GPT-4o (S11). The answer to C1 is that the model changed.
- **GPT-4o mini uses them but GPT-4o doesn't:** the timeline story, said as a comparison between models.
- **Any result is reported, including a null.** The words "delve", "tapestry" and "pivotal" were chosen for the script before E2 (DESC-1); the extra GPT-4-era words come from S11's list, fixed here.
