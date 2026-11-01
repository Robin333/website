# Ep01 E2 results note: the genre probe (30 Oct 2026)

_Design: `design E2 v1.0.md`, frozen before any data. It's exploratory and descriptive. Data: `data/runs_e2.jsonl` (270 outputs, all `stop`). Tables: `e2_summary.md`. Script figures: `script_numbers_v1.2.json` (`E2_*`)._

**The author's question (C1):** ChatGPT definitely used to say "delve". Why didn't GPT-4o in our study?

**Findings:**
1. **"Delve" itself: 0 of 270, in every genre** (abstracts, encyclopedia entries, essays, stories, explainers, business), in all three models, including GPT-4o mini (July 2024), the earliest OpenAI snapshot available.
   - This fits S11's dating: overused "in 2023 and early 2024", "less frequent later in 2024", "dropped off sharply in 2025".
   - The GPT-4-era models can't be tested through the API.
2. **Its cousins depend on the genre.** Distinctive GPT-4-era words (S11 list: pivotal, underscore, vibrant, intricate, testament…) appeared in:

   | Writing | GPT-4o | GPT-4o mini |
   |---|---|---|
   | Research abstracts | 12 of 15 | 12 of 15 |
   | Encyclopedia entries | 10 of 15 | — |
   | Business control | 3 of 15 | 2 of 15 |

3. **The newest model we tested barely uses them in any genre.** GPT-6 Sol: 2 of 75 non-business outputs and 0 of 15 business.
4. **The em dash depends on genre too.** GPT-4o used one in 23 of 30 essays and stories, against 5 of 15 business messages. GPT-6 Sol: 7 of 75 non-business.

**What it does to the script** (pre-specified in the design): it combines the "task type" and "the model changed" results. §3 answers the "but ChatGPT used to say 'delve'" objection directly (voice V11): "delve" belongs to 2023, before the oldest model we could test. Its cousins still turn up in abstracts and encyclopedia-style writing from 2024-era models, but hardly at all in the newest one.

**Not claimed:**
- Why the words faded (we can't see training).
- Anything about the ChatGPT app.
- Any generalisation beyond these 18 prompts. It's 15 outputs per cell, with wide CIs.
