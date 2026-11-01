# Ep01 study: main results

5880 outputs from 7 models, 24 scenarios. Lexicon 0.1 (frozen).

## Experiment A (drafting): by condition
| brief | instr | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| specific | avoid | 840 | 96.15 | 0.07 | 0.05 | 0.03 | 6.05 | 16% | 0.86 |
| specific | plain | 840 | 101.55 | 0.40 | 0.16 | 0.04 | 5.40 | 12% | 1.04 |
| vague | avoid | 840 | 111.19 | 0.16 | 0.09 | 0.04 | 2.52 | 58% | 2.84 |
| vague | plain | 840 | 110.34 | 0.78 | 0.34 | 0.05 | 1.85 | 49% | 4.02 |

## Experiment B (rewriting): by condition
| instr | n | words | lex_per100 | prefab_rate | invented_any | invented | questions | asks |
|---|---|---|---|---|---|---|---|---|
| clearer | 840 | 68.22 | 1.73 | 0.11 | 10% | 0.21 | 0.16 | 12% |
| orwell | 840 | 132.40 | 1.13 | 0.22 | 3% | 0.04 | 5.70 | 100% |
| specific | 840 | 89.52 | 1.71 | 0.09 | 53% | 2.19 | 0.28 | 15% |

## By model
### A, vague brief, plain instruction
| vendor | model | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| Alibaba | qwen3-32b | 120 | 104.44 | 1.17 | 0.53 | 0.05 | 1.60 | 56% | 2.23 |
| Amazon | nova-lite | 120 | 82.53 | 1.72 | 0.62 | 0.06 | 1.18 | 26% | 2.63 |
| Amazon | nova-pro | 120 | 58.21 | 1.69 | 0.62 | 0.06 | 1.65 | 41% | 1.22 |
| Anthropic | claude-haiku-5.5 | 120 | 110.92 | 0.11 | 0.06 | 0.04 | 2.54 | 59% | 4.62 |
| Anthropic | claude-opus-5.5 | 120 | 136.77 | 0.15 | 0.09 | 0.05 | 2.09 | 57% | 7.26 |
| Anthropic | claude-sonnet-4.6 | 120 | 136.70 | 0.42 | 0.33 | 0.05 | 1.94 | 54% | 3.64 |
| Anthropic | claude-sonnet-5.5 | 120 | 142.78 | 0.19 | 0.11 | 0.05 | 1.98 | 53% | 6.53 |

### B, by instruction
| instr | model | n | invented_any | questions | lex_per100 |
|---|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 120 | 1% | 0.11 | 0.74 |
| clearer | claude-opus-5.5 | 120 | 43% | 0.26 | 0.71 |
| clearer | claude-sonnet-4.6 | 120 | 0% | 0.58 | 0.98 |
| clearer | claude-sonnet-5.5 | 120 | 28% | 0.15 | 0.68 |
| clearer | nova-lite | 120 | 0% | 0.00 | 2.85 |
| clearer | nova-pro | 120 | 0% | 0.00 | 3.55 |
| clearer | qwen3-32b | 120 | 0% | 0.00 | 2.62 |
| orwell | claude-haiku-5.5 | 120 | 2% | 4.11 | 0.99 |
| orwell | claude-opus-5.5 | 120 | 9% | 6.83 | 0.58 |
| orwell | claude-sonnet-4.6 | 120 | 0% | 6.95 | 1.14 |
| orwell | claude-sonnet-5.5 | 120 | 9% | 6.47 | 0.62 |
| orwell | nova-lite | 120 | 0% | 5.29 | 1.54 |
| orwell | nova-pro | 120 | 0% | 5.12 | 1.62 |
| orwell | qwen3-32b | 120 | 0% | 5.12 | 1.40 |
| specific | claude-haiku-5.5 | 120 | 82% | 0.17 | 0.17 |
| specific | claude-opus-5.5 | 120 | 93% | 0.37 | 0.45 |
| specific | claude-sonnet-4.6 | 120 | 71% | 0.92 | 0.60 |
| specific | claude-sonnet-5.5 | 120 | 92% | 0.50 | 0.31 |
| specific | nova-lite | 120 | 5% | 0.00 | 3.61 |
| specific | nova-pro | 120 | 18% | 0.00 | 4.10 |
| specific | qwen3-32b | 120 | 9% | 0.01 | 2.73 |

## Hypothesis tests (scenario-level, paired)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |
|---|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 24 | specific: 0.404 | vague: 0.779 | +0.375 | [+0.164, +0.593] | 0.002 | 19/24 | 0.68 | 20 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 24 | specific: 0.158 | vague: 0.338 | +0.180 | [+0.096, +0.273] | 0.000 | 18/24 | 0.79 | 15 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 24 | specific: 0.039 | vague: 0.052 | +0.013 | [+0.005, +0.021] | 0.006 | 16/24 | 0.60 | 25 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 24 | plain: 0.779 | avoid: 0.162 | -0.617 | [-0.854, -0.394] | 0.000 | 22/24 | -1.02 | 10 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 24 | plain: 0.052 | avoid: 0.044 | -0.008 | [-0.015, -0.002] | 0.029 | 11/24 | -0.47 | 37 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 24 | plain: 1.854 | avoid: 2.523 | +0.670 | [+0.280, +1.077] | 0.002 | 18/24 | 0.66 | 20 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 24 | clearer: 0.102 | specific: 0.529 | +0.426 | [+0.381, +0.469] | 0.000 | 24/24 | 3.78 | 3 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 24 | specific: 0.529 | orwell: 0.029 | -0.500 | [-0.549, -0.451] | 0.000 | 24/24 | -4.00 | 3 |
| L5b Orwell check asks more questions than 'more specific' (B) | 24 | specific: 0.281 | orwell: 5.700 | +5.419 | [+5.263, +5.575] | 0.000 | 24/24 | 13.66 | 3 |

## L6 Sameness (A): word-trigram overlap between outputs for the same prompt
- Same model, repeated: mean Jaccard 0.198 (6720 pairs)
- Different models: mean Jaccard 0.055 (50400 pairs)

## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one
| term | drafts | share |
|---|---|---|
| move the dial | 0 | 0.0% |
| moving the dial | 0 | 0.0% |
| heighten(s|ed|ing)? engagement | 0 | 0.0% |
| optimi[sz](e|es|ed|ing|ation) | 34 | 2.0% |
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
| e g | 18 | 245 |
| feel free | 16 | 101 |
| make sure | 15 | 38 |
| best your name | 14 | 157 |
| next week | 14 | 93 |
| you'd like | 14 | 56 |
| best regards | 13 | 272 |
| let me know | 12 | 270 |
| regards your name | 12 | 254 |
| best regards your name | 12 | 214 |
| thanks your name | 12 | 120 |
| please let | 11 | 125 |
| look forward | 11 | 45 |
| two weeks | 11 | 35 |
| next steps | 10 | 108 |
| work together | 10 | 26 |
| please let me know | 9 | 121 |
| looking forward | 9 | 94 |
| hope you're | 9 | 78 |
| i'd like | 9 | 74 |
| phone number | 9 | 67 |
| doing well | 9 | 39 |
| here's a draft | 9 | 35 |
| specific details | 9 | 22 |
| talk through | 9 | 16 |
| company name | 8 | 105 |
| hi name | 8 | 80 |
| name your position | 8 | 76 |
| i'm happy | 8 | 62 |
| contact information | 8 | 59 |
| finds you well | 8 | 53 |
| don't need | 8 | 39 |
| get back | 8 | 39 |
| team member | 8 | 23 |
| fill in the brackets | 8 | 21 |
| fill in the bracketed | 8 | 19 |
| date please | 8 | 14 |
| name i hope | 7 | 99 |
| reply to this email | 7 | 66 |
| we're excited | 7 | 45 |

## Secondary: response type, coded by LLM judge (2520 of 2520 B outputs coded; validate against human coding)
- **clearer** (840): single_rewrite / invented as none 46%; options / invented as none 40%; options / invented as example 9%; single_rewrite / invented as example 4%; single_rewrite / invented as assertion 0%; options / invented as assertion 0%
- **orwell** (840): questions_first / invented as none 99%; questions_first / invented as example 1%
- **specific** (840): single_rewrite / invented as none 37%; options / invented as example 31%; single_rewrite / invented as assertion 22%; single_rewrite / invented as example 6%; options / invented as none 3%; options / invented as assertion 2%

| instr | model | invented as assertion | as example | none |
|---|---|---|---|---|
| clearer | claude-haiku-5.5 | 0% | 1% | 99% |
| clearer | claude-opus-5.5 | 4% | 53% | 42% |
| clearer | claude-sonnet-4.6 | 0% | 2% | 98% |
| clearer | claude-sonnet-5.5 | 0% | 34% | 66% |
| clearer | nova-lite | 0% | 0% | 100% |
| clearer | nova-pro | 0% | 0% | 100% |
| clearer | qwen3-32b | 0% | 0% | 100% |
| orwell | claude-haiku-5.5 | 0% | 1% | 99% |
| orwell | claude-opus-5.5 | 0% | 5% | 95% |
| orwell | claude-sonnet-4.6 | 0% | 0% | 100% |
| orwell | claude-sonnet-5.5 | 0% | 2% | 98% |
| orwell | nova-lite | 0% | 0% | 100% |
| orwell | nova-pro | 0% | 0% | 100% |
| orwell | qwen3-32b | 0% | 0% | 100% |
| specific | claude-haiku-5.5 | 35% | 55% | 10% |
| specific | claude-opus-5.5 | 31% | 68% | 1% |
| specific | claude-sonnet-4.6 | 33% | 51% | 16% |
| specific | claude-sonnet-5.5 | 12% | 86% | 2% |
| specific | nova-lite | 12% | 0% | 88% |
| specific | nova-pro | 26% | 0% | 74% |
| specific | qwen3-32b | 17% | 0% | 83% |

## Sample of invented specifics (B, 'more specific')
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 00
- S01 / claude-opus-5.5: 45; Thursday; May 15; 2; 00; 45
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 00
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 45
- S01 / claude-opus-5.5: 45; Thursday; March; 14; 2; 00
- S01 / claude-sonnet-5.5: 60; Thursday; May 16; 2; 00; 60
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2
- S01 / claude-sonnet-5.5: 60; Thursday; 2
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2; 00
- S01 / claude-sonnet-5.5: 60; Thursday; May 15; 2; 60; 60
- S01 / claude-haiku-5.5: Tuesday; March; 12; 2; 00; 3
- S01 / claude-haiku-5.5: Tuesday; March; 12; 2; 00; 3
