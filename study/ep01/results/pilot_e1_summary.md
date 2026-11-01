# Ep01 study: pilot_e1 results

168 outputs from 3 models, 4 scenarios. Lexicon 0.1 (frozen).

**Pilot:** these numbers are for checking the procedure and estimating variance only. They are NOT findings, and they must not be quoted in the script. Pilot scenarios are excluded from the main run.

## Experiment A (drafting): by condition
| brief | instr | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| specific | avoid | 24 | 80.04 | 0.09 | 0.09 | 0.02 | 7.86 | 12% | 0.38 |
| specific | plain | 24 | 86.12 | 0.35 | 0.23 | 0.03 | 7.49 | 25% | 0.29 |
| vague | avoid | 24 | 95.62 | 0.17 | 0.14 | 0.05 | 1.31 | 50% | 3.83 |
| vague | plain | 24 | 96.04 | 0.67 | 0.45 | 0.05 | 0.75 | 29% | 3.33 |

## Experiment B (rewriting): by condition
| instr | n | words | lex_per100 | prefab_rate | invented_any | invented | questions | asks |
|---|---|---|---|---|---|---|---|---|
| clearer | 24 | 12.67 | 0.00 | 0.00 | 0% | 0.00 | 0.00 | 0% |
| orwell | 24 | 74.46 | 1.39 | 0.08 | 0% | 0.00 | 4.67 | 100% |
| specific | 24 | 23.75 | 0.49 | 0.01 | 50% | 0.79 | 0.00 | 0% |

## By model
### A, vague brief, plain instruction
| vendor | model | n | words | lex_per100 | lex_core_per100 | prefab_rate | specifics_per100 | invented_any | placeholders |
|---|---|---|---|---|---|---|---|---|---|
| OpenAI | gpt-4o | 8 | 124.62 | 1.45 | 0.80 | 0.05 | 0.49 | 38% | 3.62 |
| OpenAI | gpt-5.5 | 8 | 94.25 | 0.41 | 0.41 | 0.04 | 0.77 | 38% | 0.50 |
| OpenAI | gpt-6-sol | 8 | 69.25 | 0.14 | 0.14 | 0.05 | 0.99 | 12% | 5.88 |

### B, by instruction
| instr | model | n | invented_any | questions | lex_per100 |
|---|---|---|---|---|---|
| clearer | gpt-4o | 8 | 0% | 0.00 | 0.00 |
| clearer | gpt-5.5 | 8 | 0% | 0.00 | 0.00 |
| clearer | gpt-6-sol | 8 | 0% | 0.00 | 0.00 |
| orwell | gpt-4o | 8 | 0% | 8.00 | 1.61 |
| orwell | gpt-5.5 | 8 | 0% | 3.00 | 1.40 |
| orwell | gpt-6-sol | 8 | 0% | 3.00 | 1.16 |
| specific | gpt-4o | 8 | 0% | 0.00 | 1.46 |
| specific | gpt-5.5 | 8 | 88% | 0.00 | 0.00 |
| specific | gpt-6-sol | 8 | 62% | 0.00 | 0.00 |

## E1 pre-registered tests (scenario-level, paired; Holm-adjusted across this table)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p | p (Holm) | same direction |
|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 4 | specific: 0.349 | vague: 0.668 | +0.319 | [-0.018, +0.655] | 0.250 | 1.000 | 3/4 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 4 | specific: 0.232 | vague: 0.450 | +0.218 | [+0.034, +0.510] | 0.250 | 1.000 | 3/4 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 4 | specific: 0.035 | vague: 0.049 | +0.014 | [+0.008, +0.021] | 0.125 | 1.000 | 4/4 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 4 | plain: 0.668 | avoid: 0.168 | -0.500 | [-0.809, -0.147] | 0.250 | 1.000 | 3/4 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 4 | plain: 0.049 | avoid: 0.048 | -0.001 | [-0.012, +0.010] | 1.000 | 1.000 | 2/4 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 4 | plain: 0.749 | avoid: 1.312 | +0.563 | [+0.191, +0.932] | 0.250 | 1.000 | 3/4 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 4 | clearer: 0.000 | specific: 0.500 | +0.500 | [+0.292, +0.667] | 0.125 | 1.000 | 4/4 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 4 | specific: 0.500 | orwell: 0.000 | -0.500 | [-0.667, -0.292] | 0.125 | 1.000 | 4/4 |
| L5b Orwell check asks more questions than 'more specific' (B) | 4 | specific: 0.000 | orwell: 4.667 | +4.667 | [+4.500, +4.875] | 0.125 | 1.000 | 4/4 |
| E1a AI words per 100: GPT-4o vs GPT-6 Sol (A, all conditions) | 4 | gpt-6-sol: 0.000 | gpt-4o: 0.296 | +0.296 | [+0.175, +0.405] | 0.125 | 1.000 | 4/4 |
| E1b Em dash in an output: GPT-4o vs GPT-6 Sol (A, all conditions) | 4 | gpt-6-sol: 0.125 | gpt-4o: 0.156 | +0.031 | [-0.250, +0.344] | 1.000 | 1.000 | 2/4 |

E1a and E1b are written as (GPT-4o minus GPT-6 Sol), so a positive difference means GPT-4o uses more.

## E1 descriptive: dashes and named words by model, all outputs (v1.0 rows were seen before E1; DESC-2)
| arm | model | outputs | em dash: share of outputs | spaced en dash: share | delve | tapestry | pivotal | game-changer | low-hanging fruit | in today's fast-paced world |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | gpt-4o | 56 | 7 (12%) | 9% | 0 | 0 | 1 | 0 | 0 | 0 |
| E1 | gpt-5.5 | 56 | 9 (16%) | 0% | 0 | 0 | 0 | 0 | 0 | 0 |
| E1 | gpt-6-sol | 56 | 10 (18%) | 0% | 0 | 0 | 0 | 0 | 0 | 0 |
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
| gpt-4o | 32 | 16% | 0.16 | 12% | 0.30 | 0.75 |
| gpt-5.5 | 32 | 6% | 0.06 | 0% | 0.00 | 0.17 |
| gpt-6-sol | 32 | 12% | 0.36 | 0% | 0.00 | 0.04 |
| model | n | em_any | em_per100 | en_spaced_any | ai_words_per100 | lex_per100 |
|---|---|---|---|---|---|---|
| gpt-4o | 24 | 8% | 0.12 | 4% | 0.31 | 1.02 |
| gpt-5.5 | 24 | 29% | 0.93 | 0% | 0.00 | 0.47 |
| gpt-6-sol | 24 | 25% | 0.66 | 0% | 0.00 | 0.39 |

## Hypothesis tests (scenario-level, paired)
| Test | scenarios | cond A | cond B | B - A | 95% CI | p (sign-flip) | same direction | dz | scenarios for 80% power |
|---|---|---|---|---|---|---|---|---|---|
| L2 Stock phrases: vague vs specific brief (A, plain) | 4 | specific: 0.349 | vague: 0.668 | +0.319 | [-0.018, +0.655] | 0.250 | 3/4 | 0.83 | 14 |
| L2b Core stock phrases (excl. practitioner list): vague vs specific (A, plain) | 4 | specific: 0.232 | vague: 0.450 | +0.218 | [+0.034, +0.510] | 0.250 | 3/4 | 0.74 | 17 |
| L2c Prefabricated wording: vague vs specific brief (A, plain) | 4 | specific: 0.035 | vague: 0.049 | +0.014 | [+0.008, +0.021] | 0.125 | 4/4 | 1.68 | 5 |
| L4a 'Avoid clichés' cuts stock phrases (A, vague brief) | 4 | plain: 0.668 | avoid: 0.168 | -0.500 | [-0.809, -0.147] | 0.250 | 3/4 | -1.33 | 7 |
| L4c 'Avoid clichés' cuts prefabricated wording? (A, vague brief) | 4 | plain: 0.049 | avoid: 0.048 | -0.001 | [-0.012, +0.010] | 1.000 | 2/4 | -0.09 | 960 |
| L4b 'Avoid clichés' adds concrete detail? (A, vague brief) | 4 | plain: 0.749 | avoid: 1.312 | +0.563 | [+0.191, +0.932] | 0.250 | 3/4 | 1.20 | 8 |
| L3a 'More specific' invents facts vs 'clearer' (B) | 4 | clearer: 0.000 | specific: 0.500 | +0.500 | [+0.292, +0.667] | 0.125 | 4/4 | 2.12 | 4 |
| L5a Orwell check invents fewer facts than 'more specific' (B) | 4 | specific: 0.500 | orwell: 0.000 | -0.500 | [-0.667, -0.292] | 0.125 | 4/4 | -2.12 | 4 |
| L5b Orwell check asks more questions than 'more specific' (B) | 4 | specific: 0.000 | orwell: 4.667 | +4.667 | [+4.500, +4.875] | 0.125 | 4/4 | 19.80 | 3 |

## L6 Sameness (A): word-trigram overlap between outputs for the same prompt
- Same model, repeated: mean Jaccard 0.229 (48 pairs)
- Different models: mean Jaccard 0.068 (192 pairs)

## L1 the author's terms in AI drafts (A, vague briefs): share of drafts containing each one
| term | drafts | share |
|---|---|---|
| move the dial | 0 | 0.0% |
| moving the dial | 0 | 0.0% |
| heighten(s|ed|ing)? engagement | 0 | 0.0% |
| optimi[sz](e|es|ed|ing|ation) | 3 | 6.2% |
| at scale | 0 | 0.0% |
| scal(e|es|ed|ing) up | 0 | 0.0% |
| scalab(le|ility) | 0 | 0.0% |
| at a high level | 0 | 0.0% |
| unified approach | 0 | 0.0% |
| leverag(e|es|ed|ing) | 1 | 2.1% |
| unlock(s|ed|ing)? (the |our |your |its )?(full )?potential | 0 | 0.0% |

## L1 Most common phrases in AI drafts (A, vague briefs), excluding words copied from the prompt
Ranked by the number of different scenarios a phrase appears in (topic-independent wording), then by drafts.
| phrase | scenarios | drafts |
|---|---|---|
| e g | 4 | 7 |
| let me know | 3 | 7 |
| best regards | 3 | 5 |
| best regards your name | 3 | 5 |
| regards your name | 3 | 5 |
| insert date | 3 | 5 |
| focus areas | 3 | 3 |
| hi team | 2 | 19 |
| thanks your name | 2 | 9 |
| day-to-day work | 2 | 9 |
| hi team we’re | 2 | 9 |
| team we’re | 2 | 9 |
| key milestones | 2 | 6 |
| completed key | 2 | 6 |
| launching a new | 2 | 5 |
| team i’m | 2 | 4 |
| let you know | 2 | 4 |
| best your name | 2 | 4 |
| together best | 2 | 4 |
| you’d like | 2 | 4 |
| time for questions | 2 | 4 |
| progress against | 2 | 4 |
| hi team i’m | 2 | 3 |
| questions or ideas | 2 | 3 |
| details soon | 2 | 3 |
| next month | 2 | 3 |
| please let | 2 | 3 |
| looking ahead | 2 | 3 |
| team completed | 2 | 3 |
| milestone and made | 2 | 3 |
| milestone and made progress | 2 | 3 |
| made progress | 2 | 3 |
| current work | 2 | 3 |
| brief reason | 2 | 3 |
| because brief | 2 | 3 |
| because brief reason | 2 | 3 |
| moving forward | 2 | 3 |
| briefly describe | 2 | 3 |
| brief description | 2 | 2 |
| dear team | 2 | 2 |

## Sample of invented specifics (B, 'more specific')
- P1 / gpt-5.5: 25%; next quarter
- P1 / gpt-5.5: 25%; next quarter
- P1 / gpt-6-sol: next quarter
- P1 / gpt-6-sol: 70%; 80%; next quarter
- P2 / gpt-5.5: June; 30
- P2 / gpt-5.5: March; 15
- P2 / gpt-6-sol: June; 30
- P3 / gpt-5.5: next quarter
- P4 / gpt-5.5: Q4
- P4 / gpt-6-sol: Q4
- P4 / gpt-5.5: Q4
- P4 / gpt-6-sol: Q4
