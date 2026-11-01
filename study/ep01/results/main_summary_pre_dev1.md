# Ep01 study: main results

5880 outputs from 7 models, 24 scenarios. Lexicon 0.1 (frozen).

## Experiment A (drafting): by condition
| brief | instr | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| specific | avoid | 840 | 93.62 | 0.07 | 0.05 | 0.03 | 6.08 | 16% | 0.86 |
| specific | plain | 840 | 100.96 | 0.40 | 0.16 | 0.04 | 5.42 | 13% | 1.03 |
| vague | avoid | 840 | 102.55 | 0.16 | 0.09 | 0.04 | 2.44 | 54% | 2.89 |
| vague | plain | 840 | 108.74 | 0.78 | 0.34 | 0.05 | 1.79 | 48% | 4.03 |

## Experiment B (rewriting): by condition
| instr | n | words | lex_per100 | prefab_rate | invented_any | invented | questions | asks |
|---|---|---|---|---|---|---|---|---|
| clearer | 840 | 68.22 | 1.73 | 0.11 | 10% | 0.21 | 0.15 | 12% |
| orwell | 840 | 92.00 | 1.17 | 0.20 | 6% | 0.12 | 3.62 | 87% |
| specific | 840 | 89.33 | 1.71 | 0.09 | 53% | 2.22 | 0.27 | 14% |

## By model
### A, vague brief, plain instruction
| vendor | model | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| Alibaba | qwen3-32b | 120 | 104.44 | 1.17 | 0.53 | 0.05 | 1.60 | 56% | 2.23 |
| Amazon | nova-lite | 120 | 82.53 | 1.72 | 0.62 | 0.06 | 1.18 | 26% | 2.63 |
| Amazon | nova-pro | 120 | 58.21 | 1.69 | 0.62 | 0.06 | 1.65 | 41% | 1.22 |
| Anthropic | claude-haiku-5.5 | 120 | 110.92 | 0.11 | 0.06 | 0.05 | 2.54 | 59% | 4.62 |
| Anthropic | claude-opus-5.5 | 120 | 125.59 | 0.16 | 0.07 | 0.05 | 1.62 | 50% | 7.34 |
| Anthropic | claude-sonnet-4.6 | 120 | 136.70 | 0.42 | 0.33 | 0.05 | 1.94 | 54% | 3.64 |
| Anthropic | claude-sonnet-5.5 | 120 | 142.78 | 0.19 | 0.11 | 0.05 | 1.98 | 53% | 6.53 |

### B, by instruction
| instr | model | n | invented_any | questions | lex_per100 |
|---|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 120 | 1% | 0.11 | 0.74 |
| clearer | claude-opus-5.5 | 120 | 43% | 0.24 | 0.71 |
| clearer | claude-sonnet-4.6 | 120 | 0% | 0.58 | 0.98 |
| clearer | claude-sonnet-5.5 | 120 | 28% | 0.15 | 0.68 |
| clearer | nova-lite | 120 | 0% | 0.00 | 2.85 |
| clearer | nova-pro | 120 | 0% | 0.00 | 3.55 |
| clearer | qwen3-32b | 120 | 0% | 0.00 | 2.62 |
| orwell | claude-haiku-5.5 | 120 | 2% | 0.23 | 0.86 |
| orwell | claude-opus-5.5 | 120 | 32% | 3.29 | 0.72 |
| orwell | claude-sonnet-4.6 | 120 | 0% | 4.07 | 1.14 |
| orwell | claude-sonnet-5.5 | 120 | 8% | 2.37 | 0.87 |
| orwell | nova-lite | 120 | 0% | 5.29 | 1.54 |
| orwell | nova-pro | 120 | 0% | 5.12 | 1.62 |
| orwell | qwen3-32b | 120 | 1% | 5.01 | 1.40 |
| specific | claude-haiku-5.5 | 120 | 82% | 0.17 | 0.17 |
| specific | claude-opus-5.5 | 120 | 95% | 0.31 | 0.42 |
| specific | claude-sonnet-4.6 | 120 | 71% | 0.92 | 0.60 |
| specific | claude-sonnet-5.5 | 120 | 92% | 0.50 | 0.31 |
| specific | nova-lite | 120 | 5% | 0.00 | 3.61 |
| specific | nova-pro | 120 | 18% | 0.00 | 4.10 |
| specific | qwen3-32b | 120 | 9% | 0.01 | 2.73 |

## Hypothesis tests (scenario-level, paired)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |
|---|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 24 | specific: 0.400 | vague: 0.779 | +0.379 | [+0.166, +0.598] | 0.002 | 19/24 | 0.67 | 20 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 24 | specific: 0.159 | vague: 0.335 | +0.177 | [+0.092, +0.270] | 0.000 | 18/24 | 0.77 | 16 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 24 | specific: 0.038 | vague: 0.052 | +0.014 | [+0.006, +0.022] | 0.003 | 16/24 | 0.68 | 20 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 24 | plain: 0.779 | avoid: 0.159 | -0.620 | [-0.861, -0.396] | 0.000 | 22/24 | -1.02 | 10 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 24 | plain: 0.052 | avoid: 0.042 | -0.009 | [-0.016, -0.003] | 0.010 | 15/24 | -0.57 | 26 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 24 | plain: 1.786 | avoid: 2.443 | +0.657 | [+0.158, +1.201] | 0.022 | 19/24 | 0.49 | 35 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 24 | clearer: 0.102 | specific: 0.531 | +0.429 | [+0.381, +0.474] | 0.000 | 24/24 | 3.61 | 3 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 24 | specific: 0.531 | orwell: 0.061 | -0.470 | [-0.532, -0.411] | 0.000 | 24/24 | -3.03 | 3 |
| L5b Orwell check asks more questions than 'more specific' (B) | 24 | specific: 0.273 | orwell: 3.625 | +3.352 | [+3.185, +3.526] | 0.000 | 24/24 | 7.73 | 3 |

## L6 Sameness (A): word-trigram overlap between outputs for the same prompt
- Same model, repeated: mean Jaccard 0.196 (6720 pairs)
- Different models: mean Jaccard 0.054 (50400 pairs)

## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one
| term | drafts | share |
|---|---|---|
| move the dial | 0 | 0.0% |
| moving the dial | 0 | 0.0% |
| heighten(s|ed|ing)? engagement | 0 | 0.0% |
| optimi[sz](e|es|ed|ing|ation) | 33 | 2.0% |
| at scale | 0 | 0.0% |
| scal(e|es|ed|ing) up | 0 | 0.0% |
| scalab(le|ility) | 3 | 0.2% |
| at a high level | 0 | 0.0% |
| unified approach | 0 | 0.0% |
| leverag(e|es|ed|ing) | 14 | 0.8% |
| unlock(s|ed|ing)? (the |our |your |its )?(full )?potential | 0 | 0.0% |

## L1 Most common phrases in AI drafts (A, vague briefs), excluding words copied from the prompt
Ranked by the number of different scenarios a phrase appears in (topic-independent wording), then by drafts.
| phrase | scenarios | drafts |
|---|---|---|
| e g | 18 | 246 |
| feel free | 16 | 97 |
| next week | 15 | 96 |
| make sure | 15 | 37 |
| best your name | 14 | 155 |
| you'd like | 14 | 55 |
| best regards | 13 | 276 |
| let me know | 12 | 269 |
| regards your name | 12 | 255 |
| best regards your name | 12 | 214 |
| please let | 11 | 132 |
| thanks your name | 11 | 119 |
| look forward | 11 | 43 |
| i'd like | 10 | 76 |
| work together | 10 | 26 |
| please let me know | 9 | 129 |
| next steps | 9 | 98 |
| looking forward | 9 | 94 |
| hope you're | 9 | 78 |
| doing well | 9 | 40 |
| here's a draft | 9 | 38 |
| support team | 9 | 34 |
| get back | 9 | 33 |
| two weeks | 9 | 31 |
| company name | 8 | 103 |
| name your position | 8 | 78 |
| hi name | 8 | 74 |
| phone number | 8 | 69 |
| contact information | 8 | 60 |
| i'm happy | 8 | 56 |
| six months | 8 | 56 |
| finds you well | 8 | 53 |
| two days | 8 | 40 |
| p m | 8 | 35 |
| few things | 8 | 16 |
| i'll tailor | 8 | 13 |
| help thanks | 8 | 11 |
| name i hope | 7 | 98 |
| reply to this email | 7 | 66 |
| we're excited | 7 | 43 |

## Secondary: response type, coded by LLM judge (70 of 2520 B outputs coded; validate against human coding)
- **clearer** (35): single_rewrite / invented as none 43%; options / invented as none 40%; single_rewrite / invented as example 11%; options / invented as example 6%
- **orwell** (35): questions_first / invented as none 91%; other / invented as none 9%

| instr | model | invented as assertion | as example | none |
|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 0% | 0% | 100% |
| clearer | claude-opus-5.5 | 0% | 100% | 0% |
| clearer | claude-sonnet-4.6 | 0% | 20% | 80% |
| clearer | claude-sonnet-5.5 | 0% | 0% | 100% |
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

## Sample of invented specifics (B, 'more specific')
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 00
- S01 / claude-opus-5.5: 45; 45
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 00
- S01 / claude-opus-5.5: 45; 30; Tuesday; 10; April; 3
- S01 / claude-opus-5.5: 45; 30; Tuesday; 10; May 2; 3
- S01 / claude-sonnet-5.5: 60; Thursday; May 16; 2; 00; 60
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2
- S01 / claude-sonnet-5.5: 60; Thursday; 2
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2; 00
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2; 60; 60
- S01 / claude-haiku-5.5: Tuesday; March; 12; 2; 00; 3
- S01 / claude-haiku-5.5: Tuesday; March; 12; 2; 00; 3
