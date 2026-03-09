# Can an AI Run a Startup? What TheStartupBench Actually Showed About Codex, Claude, and Gemini

Most AI benchmarks tell you whether a model can code, solve math, retrieve facts, or pass a reasoning test.

They do not tell you whether a model can operate.

That is a different skill.

Operating means making decisions that hold up across time. It means knowing when to cut burn without killing product quality, when to protect trust instead of chasing growth, when to tell the board the truth instead of telling them a cleaner story, and when an org problem is more dangerous than a metric problem.

That is what TheStartupBench is trying to measure.

And after running Codex, Claude, and Gemini across the current full public dev suite, the interesting result is not just who won. The interesting result is that the benchmark is already showing different operating styles and different failure patterns.

That makes it useful not only as benchmark information, but as a practical guide for how to use these models better right now.

## What TheStartupBench Is

TheStartupBench is a stateful startup-operator benchmark.

Instead of asking a model for business advice in one prompt, it drops the model into a simulated company with:

- cash and burn
- pipeline and revenue
- onboarding quality and activation
- customer trust and churn
- support backlog and incident pressure
- team morale and attrition risk
- financing pressure
- a board to report to

The model then acts through tools over weekly turns. It can read metrics, update plans, launch or hold back product, adjust hiring, make org changes, respond to incidents, manage treasury, propose raises, and update the board. Those decisions change the world state. New events then fire on top of those changes.

That matters because startup decision-making is path dependent. A bad launch creates support load. Support load hurts trust. Trust drag hurts renewals. Renewals affect financing pressure. Financing pressure changes which strategic options are still credible.

That is much closer to real operating than "give me a startup strategy."

## What The Benchmark Scores

The current benchmark scores models programmatically across seven outcome dimensions:

- cash efficiency
- revenue quality
- product health
- customer health
- team health
- strategic coherence
- risk management

It also has hard-failure gates for things like bankruptcy, catastrophic trust collapse, and severe financing failure.

That is important because it means the final score is not just "did the output sound smart." It is grounded in what happened to the company.

## What We Ran

We ran three frontier model families on the current 13-scenario public dev suite:

- Codex
- Claude Opus 4.6
- Gemini 3.0

This is the visible public dev suite, not the final hidden hosted lane, and it is still pre-human-calibration. So the right way to read these results is as a serious research comparison, not as a final benchmark-standard leaderboard claim.

Still, the signal is already useful.

## The Topline Result

Across the 13-scenario public dev suite:

| Model | Overall | Passes |
|---|---:|---:|
| Codex | **74.06%** | 13/13 |
| Claude Opus 4.6 | 72.99% | 13/13 |
| Gemini 3.0 | 66.93% | 13/13 |

All three models passed all 13 scenarios.

That is a stronger result than it may look at first glance.

If this were a weak benchmark, one of two things would happen:

- either all the models would collapse into nearly identical results
- or one or more models would fail obvious constraints, and the benchmark would mostly be measuring basic competence

Instead, all three stayed in bounds, and the separation happened on operating quality.

That is exactly where a useful benchmark should separate frontier systems.

## The Most Important Finding

TheStartupBench is already broad enough that these models are not mainly being separated by catastrophic failure.

They are being separated by judgment.

That means the benchmark is starting to test something more valuable than "can the model survive a toy sim." It is testing which model makes better tradeoffs under startup pressure.

## What Each Model Looked Like

### Codex: the best all-around operator

Codex finished first overall and won 9 of the 13 public dev scenarios:

- 0to1
- b2b_saas
- board
- crisis
- scale
- launch_distribution
- finance_fundraise_reset
- people_leadership
- product

Its component averages were:

- cash efficiency: `89.66%`
- risk management: `93.78%`
- product health: `82.48%`
- strategic coherence: `76.37%`
- customer health: `74.07%`
- revenue quality: `58.15%`
- team health: `56.77%`

Its strongest scenarios were:

- finance: `85.90%`
- scale: `80.75%`
- people: `80.64%`

Its weakest scenarios were:

- 0to1: `60.88%`
- people_leadership: `67.81%`
- board: `69.97%`

The shape here is clear. Codex looks like the strongest broad operator when the problem requires disciplined sequencing across product, finance, risk, and execution. It is especially good when the right answer is not flashy, but coherent.

It tends to do well in situations like:

- product-quality tradeoffs
- finance and treasury discipline
- board pressure where the answer needs to remain operationally grounded
- crisis handling where survival and follow-through matter
- startup situations where product, customer, cash, and execution are all entangled

If you want the shortest read: Codex currently looks like the strongest "default operator" model in this benchmark.

### Claude: the strongest challenger, especially on people and GTM-adjacent judgment

Claude finished second overall and won 4 of the 13 visible scenarios:

- people
- growth_experiment
- gtm
- finance was effectively tied at the top

Its component averages were:

- risk management: `93.14%`
- cash efficiency: `86.42%`
- product health: `80.32%`
- strategic coherence: `77.29%`
- customer health: `74.75%`
- team health: `57.99%`
- revenue quality: `56.57%`

Its strongest scenarios were:

- finance: `85.90%`
- people: `83.65%`
- scale: `80.42%`

Its weakest scenarios were:

- 0to1: `58.21%`
- b2b_saas: `66.64%`
- people_leadership: `67.40%`

Claude looks slightly different from Codex. It reads less like the best pure operator and more like the best operator-manager hybrid. It was strongest where people judgment, customer sensitivity, and GTM discipline mattered most.

It tends to look especially good in situations like:

- people and team stabilization
- growth experiment discipline
- GTM adjustments where you need nuance rather than brute optimization
- customer-sensitive operating choices
- contexts where strategic coherence and human-facing judgment matter a lot

If you want the shortest read: Claude currently looks like the best companion when the core problem is not just "what should the company do," but "what should the company do without creating downstream org or customer damage."

### Gemini: capable enough to pass, but clearly weaker on higher-judgment operating tasks

Gemini passed all 13 scenarios, which is not nothing. It means the model is capable enough to stay within the visible benchmark's hard bounds.

But it trailed meaningfully on overall quality.

Its component averages were:

- risk management: `91.91%`
- cash efficiency: `83.19%`
- customer health: `70.41%`
- product health: `70.37%`
- strategic coherence: `69.10%`
- revenue quality: `55.09%`
- team health: `51.85%`

Its strongest scenarios were:

- finance: `81.87%`
- scale: `79.41%`
- gtm: `70.48%`

Its weakest scenarios were:

- 0to1: `56.34%`
- people_leadership: `57.01%`
- board: `60.67%`

The pattern is that Gemini can keep the company alive on the visible suite, but it loses too much quality on leadership, board judgment, product depth, and strategic coherence.

The practical reading is not "Gemini is useless." It is "Gemini looks less reliable when the task requires deeper operator judgment."

## Where the Benchmark Separated Them

The scenario-level pattern is where the story gets interesting.

### Codex beat Claude where broad operating coherence mattered

Codex beat Claude on:

- `0to1`: `60.88%` vs `58.21%`
- `b2b_saas`: `76.12%` vs `66.64%`
- `board`: `69.97%` vs `69.02%`
- `crisis`: `70.62%` vs `70.38%`
- `scale`: `80.75%` vs `80.42%`
- `launch_distribution`: `73.09%` vs `69.73%`
- `finance_fundraise_reset`: `72.77%` vs `71.70%`
- `people_leadership`: `67.81%` vs `67.40%`
- `product`: `78.76%` vs `78.59%`

Many of these are not huge wins. That is the point. Codex is not crushing Claude in every category. It is edging it out repeatedly in situations where operating quality depends on holding multiple constraints together without drifting.

That is what broad operator strength looks like.

### Claude beat Codex where the benchmark rewarded org and GTM sensitivity

Claude beat Codex on:

- `people`: `83.65%` vs `80.64%`
- `growth_experiment`: `74.33%` vs `72.65%`
- `gtm`: `72.96%` vs `72.84%`

And it effectively tied Codex on:

- `finance`: `85.90%` vs `85.90%`

That suggests Claude is especially useful when you want higher-quality thought around:

- growth sequencing
- people systems
- org and customer-sensitive tradeoffs
- GTM moves that can backfire if handled too aggressively

### Gemini mostly stayed in bounds, but trailed hard on the hardest slices

Gemini did not win any visible scenarios.

Its biggest relative weakness showed up in:

- people: `60.86%`
- people_leadership: `57.01%`
- board: `60.67%`
- finance_fundraise_reset: `64.38%`

Those are exactly the kinds of scenarios where startup judgment is least like generic business advice and most like real executive tradeoff work.

## The Difficulty Signature of the Benchmark

The hardest scenario for all three models was `0to1`.

That is a strong sign that the benchmark is testing something real.

The hardest startup problems are often the least structured:

- when to push growth before product is ready
- when a signal is real versus vanity
- how to sequence proof, distribution, and onboarding
- when to reset the story rather than stretch it

`people_leadership` was also hard for all three models.

That also makes sense. Leadership-gap scenarios force the model to reason about ownership, confidence, manager load, onboarding, morale, and execution quality all at the same time.

By contrast, `finance` was comparatively strong for all three.

That tells you something useful about current models: finance problems are often more legible to them than org and ambiguity problems. People and leadership remain much harder.

## The Practical Guide: Where to Use Codex vs Claude Right Now

This is the most useful part if you are actually choosing models.

### Use Codex when the job is operating the system

Codex looks best when you need a model to reason through a multi-variable operating problem and not lose the thread.

Use Codex for:

- product and roadmap tradeoffs
- finance, treasury, and fundraising sequencing
- board-facing operating synthesis
- crisis response and recovery planning
- startup situations where product, customer, cash, and execution are all entangled

In plain language: use Codex when you need the most reliable operator brain.

### Use Claude when the job is managing people, GTM nuance, or sensitive tradeoffs

Claude looks best when the answer has to be strategically sound and socially intelligent at the same time.

Use Claude for:

- people and org questions
- growth experiment design and review
- GTM and customer-sensitive decisions
- messaging or operational plans that can fail if they are too blunt
- cases where you want the model to notice downstream trust and team effects

In plain language: use Claude when the problem is not only "what is the right move," but "what is the right move with the least organizational damage."

### Use both together when the cost of being wrong is high

The most practical workflow may not be picking one winner. It may be using both differently.

A strong current workflow looks like this:

1. Use Codex to generate the core operating plan.
2. Use Claude to pressure-test that plan for people, GTM, and stakeholder risk.
3. Have a human make the final call on the irreversible parts.

That is especially useful for:

- layoffs or reorgs
- fundraising narrative resets
- board updates after misses
- launch decisions under thin readiness
- customer-trust incidents

Codex gives you the stronger operating backbone. Claude gives you the better human-risk review.

### Where not to overtrust any of them yet

Even the best result here should not be overread.

All three models were weakest on:

- 0-to-1 ambiguity
- leadership gaps
- org-heavy judgment

That means these are still not "give it the keys and walk away" systems.

You should still keep a human tightly involved when:

- the company is pre-PMF
- the model is making people decisions
- the model is shaping board truth under pressure
- the answer depends on subtle founder judgment rather than clear metrics

## Why This Matters Beyond the Benchmark

A lot of AI discussion still treats "business use" as a generic category.

But the benchmark results suggest something more useful:

- current frontier models are not interchangeable as startup operators
- the differences show up in practical, high-leverage slices
- one model can be better at broad operator reasoning while another is better at people and GTM sensitivity

That is exactly the kind of information practitioners need.

If you are a founder, operator, chief of staff, PM, or investor, the useful question is not "which model is smartest." The useful question is "which model is strongest for this type of startup decision."

The current results suggest:

- Codex is the better default for broad startup operating problems
- Claude is the better specialist for people and GTM-adjacent judgment
- Gemini is usable, but currently less reliable on the hardest operator questions

## What TheStartupBench Is Not Yet

This part matters.

TheStartupBench should not yet be presented as a final benchmark-standard v1 or a finished hosted leaderboard. The repo is explicit that this is still pre-human-calibration. The hidden corpus still needs to grow. Governance and contamination workflows still need to mature further.

So the right conclusion is not "startup benchmarking is solved."

The right conclusion is that there is now a real executable startup benchmark here, and even before the final human calibration phase it is already producing actionable signal.

That is a meaningful step.

## The Bottom Line

The interesting result is not that Codex, Claude, and Gemini all passed the public dev suite.

The interesting result is how they passed.

Codex looked like the strongest broad operator. Claude looked like the strongest challenger on people, GTM, and customer-sensitive judgment. Gemini stayed in bounds, but trailed on leadership, product depth, and strategic coherence.

That is what a useful benchmark should reveal.

And for anyone actually using these models, that is already enough to change behavior:

- use Codex to operate
- use Claude to pressure-test people and GTM judgment
- keep humans tightly in the loop on 0-to-1, leadership, and board-truth decisions

That is a much more useful conclusion than "model A beat model B."
