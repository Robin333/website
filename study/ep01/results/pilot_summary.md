# Ep01 study: pilot results

392 outputs from 7 models, 4 scenarios. Lexicon 0.1 (frozen).

**Pilot:** these numbers are for checking the procedure and estimating variance only. They are NOT findings, and they must not be quoted in the script. Pilot scenarios are excluded from the main run.

## Experiment A (drafting): by condition
| brief | instr | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| specific | avoid | 56 | 87.59 | 0.06 | 0.04 | 0.05 | 7.91 | 32% | 0.38 |
| specific | plain | 56 | 96.62 | 0.48 | 0.20 | 0.06 | 7.29 | 27% | 0.50 |
| vague | avoid | 56 | 114.64 | 0.15 | 0.12 | 0.09 | 2.35 | 70% | 5.29 |
| vague | plain | 56 | 114.09 | 1.08 | 0.41 | 0.08 | 2.23 | 57% | 5.32 |

## Experiment B (rewriting): by condition
| instr | n | words | lex_per100 | prefab_rate | invented_any | invented | questions | asks |
|---|---|---|---|---|---|---|---|---|
| clearer | 56 | 68.62 | 0.36 | 0.09 | 9% | 0.12 | 0.16 | 9% |
| orwell | 56 | 94.11 | 0.89 | 0.19 | 5% | 0.11 | 3.88 | 96% |
| specific | 56 | 88.66 | 0.84 | 0.08 | 55% | 2.61 | 0.25 | 11% |

## By model
### A, vague brief, plain instruction
| vendor | model | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| Alibaba | qwen3-32b | 8 | 106.00 | 1.36 | 0.62 | 0.09 | 3.68 | 100% | 0.50 |
| Amazon | nova-lite | 8 | 88.88 | 2.13 | 0.60 | 0.08 | 2.50 | 88% | 1.12 |
| Amazon | nova-pro | 8 | 62.12 | 2.66 | 0.47 | 0.06 | 3.19 | 75% | 0.62 |
| Anthropic | claude-haiku-5.5 | 8 | 117.50 | 0.08 | 0.08 | 0.09 | 2.10 | 38% | 9.38 |
| Anthropic | claude-opus-5.5 | 8 | 133.50 | 0.28 | 0.28 | 0.07 | 0.08 | 12% | 12.88 |
| Anthropic | claude-sonnet-4.6 | 8 | 138.12 | 0.97 | 0.70 | 0.12 | 2.85 | 25% | 4.25 |
| Anthropic | claude-sonnet-5.5 | 8 | 152.50 | 0.09 | 0.09 | 0.09 | 1.21 | 62% | 8.50 |

### B, by instruction
| instr | model | n | invented_any | questions | lex_per100 |
|---|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 8 | 0% | 0.00 | 0.19 |
| clearer | claude-opus-5.5 | 8 | 50% | 0.00 | 0.36 |
| clearer | claude-sonnet-4.6 | 8 | 0% | 1.12 | 0.52 |
| clearer | claude-sonnet-5.5 | 8 | 12% | 0.00 | 0.33 |
| clearer | nova-lite | 8 | 0% | 0.00 | 1.14 |
| clearer | nova-pro | 8 | 0% | 0.00 | 0.00 |
| clearer | qwen3-32b | 8 | 0% | 0.00 | 0.00 |
| orwell | claude-haiku-5.5 | 8 | 0% | 2.00 | 0.18 |
| orwell | claude-opus-5.5 | 8 | 12% | 3.62 | 0.09 |
| orwell | claude-sonnet-4.6 | 8 | 0% | 6.25 | 0.82 |
| orwell | claude-sonnet-5.5 | 8 | 12% | 3.38 | 1.18 |
| orwell | nova-lite | 8 | 0% | 3.88 | 1.51 |
| orwell | nova-pro | 8 | 0% | 4.00 | 1.00 |
| orwell | qwen3-32b | 8 | 12% | 4.00 | 1.42 |
| specific | claude-haiku-5.5 | 8 | 100% | 0.00 | 0.00 |
| specific | claude-opus-5.5 | 8 | 88% | 0.00 | 0.14 |
| specific | claude-sonnet-4.6 | 8 | 88% | 0.38 | 0.08 |
| specific | claude-sonnet-5.5 | 8 | 100% | 1.38 | 0.07 |
| specific | nova-lite | 8 | 0% | 0.00 | 1.95 |
| specific | nova-pro | 8 | 12% | 0.00 | 2.63 |
| specific | qwen3-32b | 8 | 0% | 0.00 | 1.02 |

## Hypothesis tests (scenario-level, paired)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |
|---|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 4 | specific: 0.484 | vague: 1.083 | +0.599 | [-0.051, +1.248] | 0.375 | 3/4 | 0.74 | 17 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 4 | specific: 0.199 | vague: 0.406 | +0.208 | [+0.057, +0.359] | 0.250 | 3/4 | 1.08 | 9 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 4 | specific: 0.056 | vague: 0.085 | +0.028 | [+0.004, +0.056] | 0.250 | 3/4 | 0.91 | 12 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 4 | plain: 1.083 | avoid: 0.151 | -0.932 | [-1.704, -0.159] | 0.250 | 3/4 | -0.98 | 11 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 4 | plain: 0.085 | avoid: 0.090 | +0.005 | [-0.010, +0.020] | 0.625 | 2/4 | 0.30 | 92 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 4 | plain: 2.229 | avoid: 2.347 | +0.118 | [-0.631, +0.809] | 0.750 | 2/4 | 0.13 | 443 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 4 | clearer: 0.089 | specific: 0.554 | +0.464 | [+0.429, +0.500] | 0.125 | 4/4 | 11.26 | 3 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 4 | specific: 0.554 | orwell: 0.054 | -0.500 | [-0.554, -0.446] | 0.125 | 4/4 | -8.57 | 3 |
| L5b Orwell check asks more questions than 'more specific' (B) | 4 | specific: 0.250 | orwell: 3.875 | +3.625 | [+3.071, +4.179] | 0.125 | 4/4 | 5.64 | 3 |

## L6 Sameness (A): word-trigram overlap between outputs for the same prompt
- Same model, repeated: mean Jaccard 0.193 (112 pairs)
- Different models: mean Jaccard 0.060 (1344 pairs)

## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one
| term | drafts | share |
|---|---|---|
| move the dial | 0 | 0.0% |
| moving the dial | 0 | 0.0% |
| heighten(s|ed|ing)? engagement | 0 | 0.0% |
| optimi[sz](e|es|ed|ing|ation) | 3 | 2.7% |
| at scale | 0 | 0.0% |
| scal(e|es|ed|ing) up | 0 | 0.0% |
| scalab(le|ility) | 0 | 0.0% |
| at a high level | 0 | 0.0% |
| unified approach | 0 | 0.0% |
| leverag(e|es|ed|ing) | 1 | 0.9% |
| unlock(s|ed|ing)? (the |our |your |its )?(full )?potential | 0 | 0.0% |

## L1 Most common phrases in AI drafts (A, vague briefs), excluding words copied from the prompt
Ranked by the number of different scenarios a phrase appears in (topic-independent wording), then by drafts.
| phrase | scenarios | drafts |
|---|---|---|
| e g | 4 | 29 |
| let me know | 3 | 18 |
| best regards | 3 | 15 |
| best regards your name | 3 | 15 |
| regards your name | 3 | 15 |
| next steps | 3 | 14 |
| next week | 3 | 14 |
| reason e g | 3 | 14 |
| reason e | 3 | 14 |
| here's a draft | 3 | 9 |
| fill in the bracketed | 3 | 8 |
| feel free | 3 | 7 |
| new team | 3 | 7 |
| because reason | 3 | 7 |
| start date | 3 | 6 |
| one or two | 3 | 5 |
| bracketed details | 3 | 4 |
| we're doing | 3 | 4 |
| team members | 3 | 3 |
| hi team | 2 | 28 |
| thanks your name | 2 | 17 |
| next month | 2 | 15 |
| best your name | 2 | 13 |
| team i'm | 2 | 12 |
| let you know | 2 | 11 |
| hi team i'm | 2 | 10 |
| starting date | 2 | 10 |
| hard work | 2 | 10 |
| hi everyone | 2 | 9 |
| i'm excited | 2 | 8 |
| we'll find | 2 | 8 |
| date hi | 2 | 7 |
| you'd like | 2 | 7 |
| date we're | 2 | 7 |
| questions or concerns | 2 | 7 |
| starting next | 2 | 7 |
| team i’m | 2 | 7 |
| hi team i’m | 2 | 7 |
| team we're | 2 | 6 |
| free to reach | 2 | 5 |

## Secondary: response type, coded by LLM judge (168 of 168 B outputs coded; validate against human coding)
- **clearer** (56): single_rewrite / invented as none 46%; options / invented as none 39%; options / invented as example 11%; single_rewrite / invented as example 4%
- **orwell** (56): questions_first / invented as none 96%; other / invented as none 4%
- **specific** (56): single_rewrite / invented as assertion 41%; single_rewrite / invented as none 34%; options / invented as example 18%; single_rewrite / invented as example 7%

| instr | model | invented as assertion | as example | none |
|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 0% | 12% | 88% |
| clearer | claude-opus-5.5 | 0% | 62% | 38% |
| clearer | claude-sonnet-4.6 | 0% | 0% | 100% |
| clearer | claude-sonnet-5.5 | 0% | 25% | 75% |
| clearer | nova-lite | 0% | 0% | 100% |
| clearer | nova-pro | 0% | 0% | 100% |
| clearer | qwen3-32b | 0% | 0% | 100% |
| orwell | claude-haiku-5.5 | 0% | 0% | 100% |
| orwell | claude-opus-5.5 | 0% | 0% | 100% |
| orwell | claude-sonnet-4.6 | 0% | 0% | 100% |
| orwell | claude-sonnet-5.5 | 0% | 0% | 100% |
| orwell | nova-lite | 0% | 0% | 100% |
| orwell | nova-pro | 0% | 0% | 100% |
| orwell | qwen3-32b | 0% | 0% | 100% |
| specific | claude-haiku-5.5 | 50% | 50% | 0% |
| specific | claude-opus-5.5 | 75% | 25% | 0% |
| specific | claude-sonnet-4.6 | 50% | 50% | 0% |
| specific | claude-sonnet-5.5 | 50% | 50% | 0% |
| specific | nova-lite | 0% | 0% | 100% |
| specific | nova-pro | 50% | 0% | 50% |
| specific | qwen3-32b | 12% | 0% | 88% |

## Sample of invented specifics (B, 'more specific')
- P1 / claude-opus-5.5: 45%; 80%; Q3; 45%; 80%; Q3
- P1 / claude-opus-5.5: 45%; 80%; Q3; 15; 45%; 80%
- P1 / claude-sonnet-5.5: 60%; 85%; Q3; 90
- P1 / claude-sonnet-5.5: 60%; 85%; Q3
- P1 / claude-haiku-5.5: 45%; 70%; Q3
- P1 / claude-haiku-5.5: 60%; 85%; Q3; 24
- P1 / claude-sonnet-4.6: 25%; next quarter; 25%; next quarter
- P1 / claude-sonnet-4.6: 25%; Q3; 25%; Q3
- P2 / claude-opus-5.5: 70%; March; 15; February; 20
- P2 / claude-sonnet-5.5: 70%; March; 15; February; 10
- P2 / claude-haiku-5.5: 3
- P2 / claude-sonnet-5.5: 80%; 80%; March; 15; end of the month
