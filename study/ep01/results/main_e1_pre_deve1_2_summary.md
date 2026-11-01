# Ep01 study: main_e1 results

2520 outputs from 3 models, 24 scenarios. Lexicon 0.1 (frozen).

## Experiment A (drafting): by condition
| brief | instr | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| specific | avoid | 360 | 78.53 | 0.12 | 0.07 | 0.02 | 6.55 | 8% | 0.80 |
| specific | plain | 360 | 86.73 | 0.38 | 0.17 | 0.03 | 5.97 | 8% | 0.86 |
| vague | avoid | 360 | 89.94 | 0.13 | 0.10 | 0.04 | 0.91 | 23% | 3.69 |
| vague | plain | 360 | 98.56 | 0.64 | 0.30 | 0.04 | 0.30 | 11% | 3.50 |

## Experiment B (rewriting): by condition
| instr | n | words | lex_per100 | prefab_rate | invented_any | invented | questions | asks |
|---|---|---|---|---|---|---|---|---|
| clearer | 360 | 12.80 | 1.08 | 0.00 | 1% | 0.01 | 0.00 | 0% |
| orwell | 360 | 75.52 | 1.57 | 0.11 | 2% | 0.07 | 4.62 | 100% |
| specific | 360 | 22.14 | 1.26 | 0.00 | 15% | 0.25 | 0.03 | 3% |

## By model
### A, vague brief, plain instruction
| vendor | model | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| OpenAI | gpt-4o | 120 | 125.29 | 1.47 | 0.67 | 0.06 | 0.30 | 18% | 3.88 |
| OpenAI | gpt-5.5 | 120 | 97.99 | 0.33 | 0.16 | 0.03 | 0.23 | 11% | 2.92 |
| OpenAI | gpt-6-sol | 120 | 72.38 | 0.11 | 0.08 | 0.03 | 0.38 | 3% | 3.72 |

### B, by instruction
| instr | model | n | invented_any | questions | lex_per100 |
|---|---|---|---|---|---|
| clearer | gpt-4o | 120 | 0% | 0.00 | 2.28 |
| clearer | gpt-5.5 | 120 | 2% | 0.00 | 0.71 |
| clearer | gpt-6-sol | 120 | 2% | 0.00 | 0.26 |
| orwell | gpt-4o | 120 | 8% | 7.86 | 1.38 |
| orwell | gpt-5.5 | 120 | 0% | 3.02 | 1.72 |
| orwell | gpt-6-sol | 120 | 0% | 3.00 | 1.62 |
| specific | gpt-4o | 120 | 2% | 0.00 | 3.17 |
| specific | gpt-5.5 | 120 | 29% | 0.04 | 0.59 |
| specific | gpt-6-sol | 120 | 14% | 0.05 | 0.03 |

## E1 pre-registered tests (scenario-level, paired; Holm-adjusted across this table)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p | p (Holm) | same direction |
|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 24 | specific: 0.378 | vague: 0.637 | +0.259 | [+0.076, +0.458] | 0.015 | 0.036 | 17/24 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 24 | specific: 0.168 | vague: 0.302 | +0.134 | [+0.039, +0.236] | 0.012 | 0.036 | 15/24 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 24 | specific: 0.026 | vague: 0.039 | +0.012 | [+0.005, +0.020] | 0.002 | 0.014 | 17/24 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 24 | plain: 0.637 | avoid: 0.134 | -0.503 | [-0.695, -0.326] | 0.000 | 0.000 | 22/24 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 24 | plain: 0.039 | avoid: 0.036 | -0.003 | [-0.007, +0.001] | 0.121 | 0.121 | 14/24 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 24 | plain: 0.304 | avoid: 0.908 | +0.605 | [+0.253, +1.058] | 0.001 | 0.005 | 16/24 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 24 | clearer: 0.014 | specific: 0.153 | +0.139 | [+0.078, +0.203] | 0.000 | 0.000 | 14/24 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 24 | specific: 0.153 | orwell: 0.025 | -0.128 | [-0.217, -0.047] | 0.005 | 0.021 | 13/24 |
| L5b Orwell check asks more questions than 'more specific' (B) | 24 | specific: 0.031 | orwell: 4.625 | +4.594 | [+4.475, +4.719] | 0.000 | 0.000 | 24/24 |
| E1a AI words per 100: GPT-4o vs GPT-6 Sol (A, all conditions) | 24 | gpt-6-sol: 0.009 | gpt-4o: 0.421 | +0.412 | [+0.243, +0.596] | 0.000 | 0.000 | 18/24 |
| E1b Em dash in an output: GPT-4o vs GPT-6 Sol (A, all conditions) | 24 | gpt-6-sol: 0.094 | gpt-4o: 0.290 | +0.196 | [+0.083, +0.310] | 0.003 | 0.014 | 16/24 |

E1a and E1b are written as (GPT-4o minus GPT-6 Sol), so a positive difference means GPT-4o uses more.

## E1 descriptive: dashes and named words by model, all outputs (v1.0 rows were seen before E1; DESC-2)
| arm | model | outputs | em dash: share of outputs | spaced en dash: share | delve | tapestry | pivotal | game-changer | low-hanging fruit | in today's fast-paced world |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | gpt-4o | 840 | 160 (19%) | 4% | 0 | 0 | 0 | 0 | 0 | 0 |
| E1 | gpt-5.5 | 840 | 111 (13%) | 2% | 0 | 0 | 0 | 0 | 0 | 0 |
| E1 | gpt-6-sol | 840 | 89 (11%) | 0% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | claude-haiku-5.5 | 840 | 0 (0%) | 1% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | claude-opus-5.5 | 840 | 2 (0%) | 4% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | claude-sonnet-4.6 | 840 | 316 (38%) | 25% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | claude-sonnet-5.5 | 840 | 0 (0%) | 3% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | nova-lite | 840 | 8 (1%) | 1% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | nova-pro | 840 | 6 (1%) | 1% | 0 | 0 | 0 | 0 | 0 | 0 |
| v1.0 | qwen3-32b | 840 | 304 (36%) | 8% | 0 | 0 | 0 | 0 | 0 | 0 |

### E1 by model and experiment
| model | n | em_any | em_per100 | en_spaced_any | ai_words_per100 | lex_per100 |
|---|---|---|---|---|---|---|
| gpt-4o | 480 | 29% | 0.31 | 7% | 0.42 | 0.80 |
| gpt-5.5 | 480 | 6% | 0.07 | 3% | 0.05 | 0.12 |
| gpt-6-sol | 480 | 9% | 0.19 | 0% | 0.01 | 0.03 |
| model | n | em_any | em_per100 | en_spaced_any | ai_words_per100 | lex_per100 |
|---|---|---|---|---|---|---|
| gpt-4o | 360 | 6% | 0.14 | 0% | 1.48 | 2.27 |
| gpt-5.5 | 360 | 22% | 0.75 | 0% | 0.26 | 1.01 |
| gpt-6-sol | 360 | 12% | 0.44 | 0% | 0.12 | 0.64 |

## Hypothesis tests (scenario-level, paired)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |
|---|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 24 | specific: 0.378 | vague: 0.637 | +0.259 | [+0.073, +0.459] | 0.013 | 17/24 | 0.53 | 31 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 24 | specific: 0.168 | vague: 0.302 | +0.134 | [+0.037, +0.235] | 0.013 | 15/24 | 0.54 | 30 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 24 | specific: 0.026 | vague: 0.039 | +0.012 | [+0.005, +0.020] | 0.003 | 17/24 | 0.67 | 20 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 24 | plain: 0.637 | avoid: 0.134 | -0.503 | [-0.694, -0.329] | 0.000 | 22/24 | -1.06 | 9 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 24 | plain: 0.039 | avoid: 0.036 | -0.003 | [-0.007, +0.001] | 0.122 | 14/24 | -0.33 | 75 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 24 | plain: 0.304 | avoid: 0.908 | +0.605 | [+0.259, +1.067] | 0.001 | 16/24 | 0.58 | 26 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 24 | clearer: 0.014 | specific: 0.153 | +0.139 | [+0.081, +0.206] | 0.000 | 14/24 | 0.86 | 13 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 24 | specific: 0.153 | orwell: 0.025 | -0.128 | [-0.217, -0.050] | 0.005 | 13/24 | -0.59 | 25 |
| L5b Orwell check asks more questions than 'more specific' (B) | 24 | specific: 0.031 | orwell: 4.625 | +4.594 | [+4.472, +4.717] | 0.000 | 24/24 | 14.50 | 3 |

## L6 Sameness (A): word-trigram overlap between outputs for the same prompt
- Same model, repeated: mean Jaccard 0.239 (2880 pairs)
- Different models: mean Jaccard 0.080 (7200 pairs)

## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one
| term | drafts | share |
|---|---|---|
| move the dial | 0 | 0.0% |
| moving the dial | 0 | 0.0% |
| heighten(s|ed|ing)? engagement | 0 | 0.0% |
| optimi[sz](e|es|ed|ing|ation) | 22 | 3.1% |
| at scale | 0 | 0.0% |
| scal(e|es|ed|ing) up | 0 | 0.0% |
| scalab(le|ility) | 5 | 0.7% |
| at a high level | 0 | 0.0% |
| unified approach | 0 | 0.0% |
| leverag(e|es|ed|ing) | 11 | 1.5% |
| unlock(s|ed|ing)? (the |our |your |its )?(full )?potential | 0 | 0.0% |

## L1 Most common phrases in AI drafts (A, vague briefs), excluding words copied from the prompt
Ranked by the number of different scenarios a phrase appears in (topic-independent wording), then by drafts.
| phrase | scenarios | drafts |
|---|---|---|
| e g | 16 | 88 |
| best regards | 15 | 81 |
| regards your name | 15 | 71 |
| best regards your name | 15 | 64 |
| feel free | 14 | 65 |
| best your name | 13 | 98 |
| let me know | 11 | 154 |
| next steps | 11 | 58 |
| make sure | 11 | 20 |
| thanks your name | 10 | 66 |
| you’d like | 10 | 49 |
| finds you well | 9 | 55 |
| contact information | 9 | 45 |
| free to reach | 9 | 20 |
| feel free to reach | 9 | 20 |
| brief description | 9 | 16 |
| please let | 8 | 88 |
| message finds | 8 | 31 |
| hope this message | 8 | 31 |
| hope this message finds | 8 | 31 |
| message finds you well | 8 | 31 |
| don’t hesitate | 8 | 20 |
| there’s anything | 8 | 12 |
| please feel | 8 | 10 |
| please feel free | 8 | 10 |
| please let me know | 7 | 86 |
| please contact | 7 | 38 |
| date please | 7 | 25 |
| doing well | 7 | 22 |
| contact info | 7 | 21 |
| clear communication | 7 | 18 |
| work together | 7 | 18 |
| look forward | 7 | 17 |
| need help | 7 | 12 |
| hi name | 6 | 74 |
| name i hope | 6 | 63 |
| let you know | 6 | 41 |
| name your position | 6 | 38 |
| we’d love | 6 | 37 |
| well i wanted | 6 | 32 |

## Secondary: response type, coded by LLM judge (1080 of 1080 B outputs coded; validate against human coding)
- **clearer** (360): single_rewrite / invented as none 99%; single_rewrite / invented as assertion 1%
- **orwell** (360): questions_first / invented as none 100%
- **specific** (360): single_rewrite / invented as none 71%; single_rewrite / invented as assertion 29%

| instr | model | invented as assertion | as example | none |
|---|---|---|---|---|
| clearer | gpt-4o | 0% | 0% | 100% |
| clearer | gpt-5.5 | 2% | 0% | 98% |
| clearer | gpt-6-sol | 2% | 0% | 98% |
| orwell | gpt-4o | 0% | 0% | 100% |
| orwell | gpt-5.5 | 0% | 0% | 100% |
| orwell | gpt-6-sol | 0% | 0% | 100% |
| specific | gpt-4o | 8% | 0% | 92% |
| specific | gpt-5.5 | 42% | 0% | 58% |
| specific | gpt-6-sol | 37% | 0% | 63% |

## Sample of invented specifics (B, 'more specific')
- S01 / gpt-5.5: Tuesday; 2
- S01 / gpt-5.5: Thursday; 2
- S01 / gpt-5.5: 60
- S01 / gpt-5.5: 60
- S04 / gpt-5.5: £50,000
- S04 / gpt-6-sol: $50,000; 15%
- S04 / gpt-6-sol: $50,000; 15%
- S04 / gpt-6-sol: 15%
- S05 / gpt-5.5: next week
- S05 / gpt-5.5: Friday; 30; next week
- S05 / gpt-6-sol: Friday; next week
- S05 / gpt-6-sol: Friday; next week
