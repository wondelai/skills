---
name: lean-analytics
description: 'Choose and audit startup metrics using Croll and Yoskovitz''s "Lean Analytics". Use when the user mentions "what metrics should we track", "KPIs", "north star metric", "One Metric That Matters", "OMTM", "vanity metrics", "analytics dashboard", "DAU/MAU", "churn benchmark", "measure product-market fit", "are we tracking the right things", or "which number actually matters". Also trigger when choosing metrics for a startup or feature, auditing a dashboard for vanity metrics, setting metric targets and baselines, or instrumenting a product by business model and stage. Covers good-vs-vanity metrics, the One Metric That Matters, metrics by business model, the five startup stages, and benchmarks. For the build-measure-learn loop, see lean-startup. For fixing activation and retention, see improve-retention.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Lean Analytics

A data discipline for startups distilled from Alistair Croll and Benjamin Yoskovitz's *Lean Analytics*: separate metrics that change decisions from numbers that merely flatter, then point the whole company at the One Metric That Matters for your business model and stage. Use it to choose metrics, audit dashboards, set targets, and plan instrumentation.

## Core Principle

**Focus on the one metric that matters right now — everything else is noise that feels like progress.** Startups die from lack of focus more often than lack of data. The discipline is knowing your business model, knowing your stage, and tracking the single number that tells you whether the riskiest part of the business is working. A metric earns attention only if it changes what you do next.

## Scoring

**Goal: 10/10.** Rate metric choices, dashboards, and instrumentation plans 0-10 against these principles. Report the current score and the specific changes needed to reach 10/10.

- **9-10:** One OMTM matched to model and stage, paired counter-metric, a line in the sand with a pre-committed miss response, cohorted and segmented data
- **7-8:** Mostly actionable ratios and a plausible OMTM, but no explicit target, weak cohorting, or too many "key" metrics
- **5-6:** Actionable and vanity metrics mixed; dashboard exists but rarely changes a decision; model and stage never named
- **3-4:** Vanity metrics dominate — totals, cumulative charts, blended averages; metrics copied from other companies
- **0-2:** No instrumentation, or numbers chosen to impress investors rather than drive decisions

## Framework

### 1. Good Metrics vs Vanity Metrics

**Core concept:** A good metric is comparative (versus last week, versus another cohort), understandable (the team can recall and debate it), a ratio or rate (not an ever-growing total), and behavior-changing — if a number won't change what you do, stop measuring it. Vanity metrics — total signups, page views, cumulative anything — only go up and only make you feel good.

**Why it works:** The output of analytics is decisions, not data. Ratios are inherently comparative and operable, while totals hide decay: total registered users rises even while the product bleeds actives. Forcing every metric through the "what will we do differently?" test converts reporting into learning.

**Key insights:**
- Work the lens pairs: qualitative vs quantitative (interviews reveal *why*, numbers reveal *how much*), exploratory vs reporting (exploration finds your unfair advantage; reporting keeps the lights on), leading vs lagging (complaints predict churn before churn happens), correlated vs causal
- Correlation finds the lever; only an experiment proves it — find metrics that move together, then change one for a randomized group to test causality
- Cohorts make time honest: compare users by signup month, or real improvement vanishes inside blended averages
- Segments make comparisons honest: split by channel, plan, and geography — a flat aggregate often hides one segment soaring and another collapsing
- Averages lie under skew: whales and lurkers are different businesses, so read medians and percentiles
- A cumulative up-and-to-the-right chart is the single most reliable vanity tell

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Dashboard audit | Rewrite each total as a ratio | Total signups → % of visitors activating within 7 days |
| Board reporting | Show cohorts, not cumulative curves | Retention by signup month replaces "users over time" |
| Feature decision | Demand a behavior-changing metric | "If D7 retention doesn't rise 10%, the feature comes out" |

**Ethical boundary:** Metrics exist to describe and serve users, not manipulate them — instrument only what you need and respect privacy in what you collect.

See: [references/good-metrics.md](references/good-metrics.md)

### 2. The One Metric That Matters (OMTM)

**Core concept:** At any moment there is one number that matters above all others — the one that tells you whether the current riskiest assumption is working. Pick it, display it everywhere, and let it drive every experiment until you graduate to the next stage.

**Why it works:** The OMTM answers the most important question you have right now, forces you to draw a line in the sand so "good" is defined before results arrive, and focuses the entire company. A dashboard of forty numbers diffuses accountability; one number creates a shared scoreboard and a culture of experimentation.

**Key insights:**
- The OMTM rotates — it is the metric that matters *now*, not forever; passing a stage gate or pivoting changes it
- Pair it with a counter-metric so it can't be gamed: activation speed paired with 30-day retention, sales velocity paired with refund rate
- A line in the sand has three parts: a target number, a date, and a pre-committed answer to "what do we do if we miss?"
- "Good enough" is a decision made in advance, not a discovery made after — otherwise the goalposts move
- If the team can't agree on the OMTM, you haven't agreed what the riskiest part of the business is — that argument is the valuable part
- Collect many metrics, but *watch* one — the rest live in drill-down reports, not on the wall

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Quarterly planning | One OMTM per stage; experiments ladder up to it | Stickiness stage → all bets target week-4 retention |
| Dashboard design | OMTM big, 4-6 supporting metrics small | Wall display: paid conversion 3.2% huge; CAC, churn, NPS below |
| Team alignment | Pre-commit the miss response | "Under 10% by March 1 → we pivot to the agency segment" |

**Ethical boundary:** The line in the sand disciplines the company's bets, not individuals — turning the OMTM into personal quotas invites gaming and hides truth.

See: [references/omtm.md](references/omtm.md)

### 3. Metrics by Business Model

**Core concept:** Your business model dictates which metrics exist and which matter. Lean Analytics defines six archetypes — e-commerce, SaaS, free mobile app, media site, user-generated content, and two-sided marketplace — each with its own metric tree and its own definition of "working."

**Why it works:** Copying another company's north star fails because metrics encode the mechanics of a model: a marketplace lives or dies on liquidity, a SaaS business on churn, a media site on engaged attention. Naming your model first turns "what should we measure?" from a brainstorm into a lookup.

**Key insights:**
- E-commerce runs on conversion rate, average order value, and repurchase rate — annual repurchase under ~40% means acquisition mode, over ~60% loyalty mode, and each mode has a different playbook
- SaaS runs on MRR, churn, LTV:CAC, expansion, and time-to-value; free mobile apps run on downloads → DAU/MAU, percent paying, and ARPDAU vs ARPPU (whales skew every average)
- Media runs on audience, engaged time (not raw pageviews), CTR, and RPM; UGC runs on the engagement funnel — visitor → voyeur → commenter → creator — plus content per user and spam rate
- Marketplaces run on liquidity: listings, fill/sell-through rate, time-to-transaction, take rate, buyer/seller ratio — GMV is vanity until multiplied by take rate
- Hybrid businesses must pick ONE primary model to own the OMTM; the secondary model contributes counter-metrics, not equal billing
- The model also dictates instrumentation: define each metric's formula and source up front, or every team computes "churn" differently

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New product instrumentation | Name the model, install its metric tree | Subscription box → primary model SaaS; churn tracked before AOV |
| North-star debate | Derive from model mechanics, don't copy | Marketplace adopts fill rate, not a SaaS-style MRR target |
| Investor dashboard | Report the model's canonical ratios | SaaS deck: MRR growth, net churn, LTV:CAC, CAC payback |

See: [references/business-model-metrics.md](references/business-model-metrics.md)

### 4. Metrics by Stage: The Lean Analytics Stages

**Core concept:** Startups move through five stages — Empathy, Stickiness, Virality, Revenue, Scale — and each has a gate. The OMTM is the intersection of business model and current stage; working on a later stage's metric before passing the current gate is the canonical startup mistake.

**Why it works:** Sequencing prevents waste. Virality poured into a product that doesn't retain is a leaky bucket; paid acquisition before unit economics burns runway with precision. Each gate de-risks the next, larger investment of money and time.

**Key insights:**
- Empathy: have 15+ problem interviews shown a painful, frequent problem people will pay to fix? The metric is mostly conversation notes — and that's correct at this stage
- Stickiness: do people use it repeatedly on their own? Track retention cohorts and core-action engagement; don't pour users into a leaky bucket
- Virality: do users bring users? Track viral coefficient AND cycle time — shortening the cycle often grows you faster than raising the coefficient, and inherent virality beats incentivized invites
- Revenue: does a dollar in return more than a dollar out, soon enough? Revenue per customer, CAC payback, gross margin
- Scale: channels, partners, and new markets — metrics shift from product risk to ecosystem and operations
- Gates are evidence, not time: a flattening retention curve exits Stickiness; positive unit economics within payback tolerance exits Revenue

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Growth-spend decision | Check the stickiness gate first | D30 retention at 4% → fix onboarding before buying ads |
| Roadmap prioritization | Stage picks the OMTM; OMTM picks the work | Stickiness stage ships onboarding fixes, not a referral program |
| Fundraising narrative | Pitch the passed gate and its evidence | "Week-4 retention flat at 35% — raising to scale acquisition" |

See: [references/five-stages.md](references/five-stages.md)

### 5. Baselines and Lines in the Sand

**Core concept:** A metric without a target is trivia. Use published baselines as starting heuristics — not laws — to define "good enough," then draw your line in the sand: a number, a date, and a pre-committed action if you miss.

**Why it works:** Baselines convert open-ended measurement into falsifiable bets. Knowing that ~5% monthly churn is the early-SaaS ceiling tells you whether to optimize or rebuild; without a line, every result can be rationalized and no experiment can fail.

**Key insights:**
- Early SaaS: ~5% monthly customer churn is the upper bound of viable; healthy companies push toward ~2% or lower
- Habitual and social apps: DAU/MAU around 20%+ signals real engagement; casual mobile apps average roughly 14% day-30 retention, so plan for steep decay
- Conversion: e-commerce typically converts ~1-3% of visitors; landing pages on good paid traffic usually convert low single digits — 25-30% is exceptional, not a planning number
- A viral coefficient above 1 is rare and fleeting; treat virality as CAC reduction and optimize cycle time before coefficient
- No benchmark for your case? Measure your current value, improve relative to it, and watch the derivative — 5% weekly improvement compounds into category-leading numbers
- Benchmarks shift by market, channel, price point, and era — always re-derive against your own cohorts before adopting someone else's number

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Target setting | Baseline → line in the sand → pre-commitment | "Churn under 4% by Q3 or we rebuild onboarding" |
| Anomaly triage | Compare to your own baseline before benchmarks | Conversion fell 2.4% → 1.9% in a week — investigate the release |
| Channel evaluation | Re-derive benchmarks per channel | Paid social converts 0.8%, search 4% — budget follows the line |

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| A dashboard with 40 metrics | Diffuses focus; nobody owns anything | One OMTM big, 4-6 supporting metrics, archive the rest |
| Celebrating cumulative charts | Totals can't go down, so they hide decay | Plot rates, conversions, and cohort retention instead |
| Copying another company's north star | Metrics encode model mechanics you don't share | Derive the OMTM from your model × stage |
| Skipping cohorts | Blended averages mask whether the product improves | Track each signup cohort separately over time |
| Optimizing virality before stickiness | Growth multiplies churn — the leaky bucket | Pass the retention gate, then build invite loops |
| Measuring what's easy, not what's risky | Decisions still get made on gut | Instrument the riskiest assumption first |
| No line in the sand | Every result gets rationalized; experiments can't fail | Pre-commit target, date, and miss response |
| Confusing correlation with causation | You pump a metric that doesn't drive the outcome | Run a controlled experiment before investing |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you name your OMTM right now? | Focus is diffused across a dashboard | Pick one metric from current model × stage |
| Would this metric change what you do next? | You're reporting, not deciding | Drop it, or define the decision it gates |
| Is it a ratio or rate, not a total? | Vanity risk — totals only go up | Rewrite as a conversion, retention, or per-user rate |
| Do you know your business model archetype? | Wrong metric tree installed | Name one of the six models; adopt its metrics |
| Do you know your stage (Empathy → Scale)? | Probably optimizing a later stage too early | Find the first unpassed gate; that's your stage |
| Is there a target with a date and a miss plan? | Goalposts will move after results | Draw the line in the sand in writing |
| Is the data cohorted and segmented? | Averages are hiding the truth | Build cohort tables; split by channel and segment |
| Is a counter-metric guarding the OMTM? | The OMTM will be gamed | Pair it, e.g. signup growth × 30-day retention |

## Reference Files

- [references/good-metrics.md](references/good-metrics.md) — Four tests of a good metric, vanity-metric rewrite table, cohort analysis how-to, segmentation discipline, correlation-to-causation loop, metric definition template
- [references/omtm.md](references/omtm.md) — Choosing the OMTM step by step, stage × model matrix, counter-metric pairing, lines in the sand, dashboard design, rotation triggers, worked examples
- [references/business-model-metrics.md](references/business-model-metrics.md) — Metric trees for all six business models with formulas, instrumentation notes, measurement failure modes, hybrid-model guidance
- [references/five-stages.md](references/five-stages.md) — Stage-by-stage playbook: gating metrics, exit-criteria checklists, premature-scaling symptoms, funding and runway interactions
- [references/case-studies.md](references/case-studies.md) — Three scenarios: SaaS dashboard to OMTM, marketplace liquidity discovery, mobile app fixing stickiness before growth

## Further Reading

- [*"Lean Analytics: Use Data to Build a Better Startup Faster"*](https://www.amazon.com/Lean-Analytics-Better-Startup-Faster/dp/1449335675?tag=wondelai00-20) by Alistair Croll & Benjamin Yoskovitz
- [*"The Lean Startup"*](https://www.amazon.com/Lean-Startup-Entrepreneurs-Continuous-Innovation/dp/0307887898?tag=wondelai00-20) by Eric Ries
- [*"Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing"*](https://www.amazon.com/Trustworthy-Online-Controlled-Experiments-Practical/dp/1108724264?tag=wondelai00-20) by Ron Kohavi, Diane Tang & Ya Xu

## About the Authors

**Alistair Croll** is an entrepreneur and analyst who co-founded web performance company Coradiant, founded Solve For Interesting, and chairs Startupfest among other technology conferences. **Benjamin Yoskovitz** is a founding partner at venture studio Highline Beta and a serial founder and startup investor. They wrote *Lean Analytics* for Eric Ries's Lean Series.
