# Can an AI Run a Startup? What We Learned from TheStartupBench

Most AI benchmarks tell you whether a model can code, solve math problems, retrieve facts, or follow instructions. They do not tell you whether a model can operate under the kind of messy, compounding pressure that defines an actual startup.

That is the gap TheStartupBench is trying to close.

The idea is simple: instead of asking a model for business advice in a single prompt, drop it into a simulated company with real operating pressure. Give it cash balance, burn, pipeline, onboarding quality, customer trust, support backlog, org stress, financing pressure, and a board to answer to. Let events fire over time. Then see whether the model can make coherent decisions week after week.

This is not a "write a strategy memo" benchmark. It is a stateful operating benchmark.

## What TheStartupBench Actually Measures

In TheStartupBench, the model does not just explain what it would do. It has to act through tools.

It can read metrics, adjust product roadmap tradeoffs, launch or hold back releases, change financial plans, rebalance treasury exposure, propose financing, update hiring, make org adjustments, handle incidents, resolve support pressure, update the board, and advance the simulation forward in time. Its decisions then change the world state, and later events compound on top of those changes.

That matters because startup judgment is almost never about a single clever answer. It is about sequencing. If you push growth too early, support breaks. If you protect cash without protecting trust, renewals slip. If you tell the board a prettier story than the one the operating system can support, you buy short-term calm at the cost of long-term credibility.

The current benchmark scoring is programmatic across seven outcome dimensions:

- cash efficiency
- revenue quality
- product health
- customer health
- team health
- strategic coherence
- risk management

On top of that, hard-failure gates penalize or fail runs for outcomes like bankruptcy, catastrophic trust collapse, or serious financing breakdown.

That is the right shape for the problem. It means the benchmark is trying to reward durable operating quality, not just polished language.

## What Exists Today

As of the current pre-human-calibration freeze, TheStartupBench is no longer just an RFC. It now has a reference Python package and CLI, executable scenario/runtime machinery, built-in baselines, public and hidden suite packaging, run-manifest support, calibration-study workflows, synthetic reviewer import/export, governance artifacts, and CI.

The public dev suite now contains 13 scenarios across:

- 0-to-1
- B2B SaaS
- board
- crisis
- scale
- GTM
- finance
- people
- product

There are also hidden operator, strategy, canary, and real-world-derived packs in the repo for integrity, exploit detection, and calibration work.

That said, the benchmark is still in an important intermediate state. The honest framing is not "this is a final leaderboard benchmark." The honest framing is: this is now a serious executable benchmark with meaningful separation signal, but it is still pre-human-calibration and still expanding its hidden corpus and governance maturity.

## We Ran Codex, Claude, and Gemini on the Full Public Dev Suite

To test whether the benchmark is already producing useful signal, we ran three frontier model families across the full 13-scenario public dev suite:

- Codex
- Claude Opus 4.6
- Gemini 3.0

The topline results were:

| Model | Overall | Passes |
|---|---:|---:|
| Codex | **74.06%** | 13/13 |
| Claude Opus 4.6 | 72.99% | 13/13 |
| Gemini 3.0 | 66.93% | 13/13 |

That result is more interesting than it looks.

If this were still a weak benchmark surface, you would expect one of two outcomes: either all the models would cluster tightly with no meaningful pattern, or one or more would fail obvious constraints and the benchmark would mainly be measuring basic competence.

Instead, all three models passed all 13 scenarios.

That means the benchmark is already broad enough that these systems can stay structurally in bounds. The separation is happening somewhere more interesting: on the quality of startup judgment.

## What Separated the Models

Codex finished first overall and won 9 of the 13 public dev scenarios. It looked like the strongest all-around operator. Its profile was strongest on cash efficiency, product depth, and risk profile. It handled finance and scale especially well, and it also came out ahead on a wide set of judgment-heavy scenarios including board, crisis, launch distribution, finance fundraise reset, people leadership, and product.

Claude finished a close second and won 4 of the 13 visible scenarios. It looked strongest on people-heavy and GTM-adjacent cases, especially people, growth experiment discipline, and GTM. Its component profile suggested slightly better customer, team, and strategic-coherence behavior than the other models, even though it trailed Codex narrowly overall.

Gemini passed the whole suite, which is important, but it trailed materially on overall operating quality. It looked competent enough to stay alive in the visible benchmark, but it gave up ground on leadership judgment, product depth, board quality, and strategic coherence.

That is exactly the kind of signal a useful startup benchmark should produce.

The benchmark is not saying "one model is good and the others are broken." It is saying: these models are all capable enough to survive the visible suite, but they do not survive in the same way. The differences show up in sequencing, prioritization, communication quality, and ability to handle ambiguous operator tradeoffs.

## The Difficulty Signature Matters

One of the most telling things in the results is which scenarios were hard.

Across all three models, `0to1` was consistently one of the hardest slices. `people_leadership` was also difficult. `finance` was comparatively strong for all three.

That pattern makes sense. The hardest startup problems are usually not bookkeeping. They are ambiguity-heavy judgment problems:

- When is there enough product truth to scale?
- When should you reset the fundraising narrative instead of stretching it?
- How do you handle an org gap without creating deeper ownership drift?
- What do you tell the board when the company needs a real re-forecast, not a cosmetic story?

If a benchmark claims to measure startup operation and its hardest cases are not ambiguity, sequencing, and leadership, it is probably measuring the wrong thing. TheStartupBench appears to be getting that part right.

## Why This Is Different from Generic Business Prompting

There are plenty of ways to get a language model to sound smart about startups. Ask it about pricing, fundraising, org design, or growth loops and it will often produce plausible advice.

That is not the same as operating.

Operating means one decision changes the feasible set of the next decision. It means quality debt becomes support drag, support drag becomes trust drag, trust drag becomes renewal risk, and renewal risk changes what financing options remain credible. It means a board update is not judged only as nice prose, but by whether it fits the underlying state of the company.

That is the core promise of TheStartupBench. It turns startup reasoning into something more executable and therefore more falsifiable.

## What The Benchmark Is Not Yet

This part matters just as much as the promising result.

TheStartupBench should not yet be presented as a benchmark-complete v1 or as a final hosted leaderboard. The repo itself is clear about that. Human and operator calibration are still in progress. The hidden corpus still needs to grow. Governance, contamination policy, refresh cadence, and broader benchmark-scale coverage still need more work.

So the right conclusion is not "we have solved startup benchmarking."

The right conclusion is: there is now a real executable startup benchmark here, and even before the final human calibration phase it is already producing nontrivial signal on frontier models.

That is a meaningful step forward.

## The Current Takeaway

If you want the shortest possible summary, it is this:

The interesting result is not that Codex, Claude, and Gemini all passed the public dev suite. The interesting result is how they passed.

Codex looked like the strongest broad operator. Claude looked like the strongest challenger on people and GTM-heavy judgment. Gemini stayed in bounds, but trailed on leadership, product depth, and strategic coherence.

That is what a serious benchmark should reveal.

TheStartupBench is still early. But it is already doing something most AI evaluation work does not: forcing models to behave like operators instead of commentators.
