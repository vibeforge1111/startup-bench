# TheStartupBench RFC v0.1

Status: Draft

Owner: TBD

Last updated: 2026-03-07

## 1. Purpose

TheStartupBench is a benchmark family for evaluating whether AI agents can make strong, durable, realistic startup and business decisions under uncertainty.

It is not a toy management simulator, not a one-shot business case interview, and not a generic "agent benchmark with startup flavor."

TheStartupBench should answer a narrower and more useful question:

Can an agent operate a startup-like company over time across product, go-to-market, finance, people, operations, and crisis scenarios using realistic information, constrained actions, measurable outcomes, and auditable evaluation?

## 2. Why this benchmark should exist

Current widely cited agent benchmarks are strong in coding, browser use, tool use, and general assistance, but none of them directly target startup or business operating judgment as a first-class domain.

What is missing today:

- Long-horizon company operation rather than isolated tasks
- Resource allocation under business constraints
- Strategic tradeoffs across multiple functions
- Decision quality under partial information
- Multi-stakeholder coordination
- Economic outcomes coupled with safety, compliance, and team health

TheStartupBench should fill that gap using the strongest benchmark methodology patterns from the current agent benchmark ecosystem without inheriting their domain assumptions.

## 3. Benchmark charter

### 3.1 Primary objective

Measure an agent's ability to run a startup or startup-like business system under realistic constraints and uncertainty.

### 3.2 Secondary objectives

- Measure robustness, not just upside
- Measure business judgment, not just tool execution
- Measure policy compliance and stakeholder handling
- Measure long-horizon coherence
- Support reproducible and contamination-aware evaluation

### 3.3 Non-goals

- Simulating every nuance of real entrepreneurship
- Predicting actual startup success in the real world
- Replacing expert judgment for investment decisions
- Benchmarking pure coding ability
- Rewarding free-form persuasion without measurable state change

## 4. Product requirements for an industry-standard benchmark

TheStartupBench should only be considered successful if it is:

- Grounded: outcomes are linked to state transitions and explicit rules
- Verifiable: most scoring is programmatic
- Hard to game: hidden tasks, rolling refreshes, contamination controls
- Representative: covers multiple startup modes, not one archetype
- Reproducible: fixed harness, versioning, logs, seeds, and reports
- Interpretable: strong replay, error taxonomy, and subscore visibility
- Human-calibrated: human and expert baselines exist and matter

## 5. Lessons from existing benchmarks

This section extracts methodology patterns from the most relevant benchmarks. It focuses on benchmark design, not on copying task mechanics.

### 5.1 SWE-bench

Reference:

- https://github.com/SWE-bench/SWE-bench

Relevant methodology:

- Real-world tasks derived from naturally occurring artifacts
- Executable evaluation with containerized harnesses
- Objective pass/fail testing

What to adopt:

- Real artifacts, not synthetic "roleplay-only" tasks
- Reproducible harness
- Hard separation between agent action and evaluator logic

What not to copy:

- Over-reliance on a static public benchmark as the main flagship measure

### 5.2 SWE-bench Verified

References:

- https://openai.com/index/introducing-swe-bench-verified/
- https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

Relevant methodology:

- Human verification for task solvability and benchmark quality

What to adopt:

- Human review before promoting tasks into official benchmark splits
- Structured annotation for underspecification and unfair evaluation

Critical warning:

SWE-bench Verified is also a cautionary case. OpenAI said on 2026-02-23 that it no longer reliably measures frontier coding capability because of flawed tests and contamination. TheStartupBench must assume that any open, static, successful benchmark will become contaminated over time.

### 5.3 SWE-rebench

Reference:

- https://swe-rebench.com/about

Relevant methodology:

- Centralized evaluation
- Standardized scaffold
- Repeated runs
- Reporting SEM and pass@k
- Continuous dataset refresh
- Explicit contamination marking tied to model release timing

What to adopt:

- Official evaluation scaffold for leaderboard submissions
- At least 5 runs for stochastic agents
- Confidence intervals and pass@k-style reporting
- Continuous refresh pipeline
- Transparent contamination policy

This is one of the strongest methodology templates for TheStartupBench.

### 5.4 GAIA

Reference:

- https://arxiv.org/abs/2311.12983

Relevant methodology:

- Human-simple but tool-demanding tasks
- Public questions with hidden answers for leaderboard integrity
- Benchmark philosophy focused on robust assistance rather than specialist trick questions

What to adopt:

- Hidden-answer or hidden-state official test split
- Preference for tasks humans can understand and audit
- Focus on general operating competence rather than narrow benchmark hacks

### 5.5 WebArena

Reference:

- https://webarena.dev/

Relevant methodology:

- Self-hostable realistic environment
- High-level natural language tasks
- Programmatic validation of functional correctness

What to adopt:

- Realistic multi-application environment
- Programmatic validation of intermediate and final state
- Self-hostable evaluation infrastructure

### 5.6 WorkArena and WorkArena++

Reference:

- https://github.com/ServiceNow/WorkArena

Relevant methodology:

- Knowledge-work focus
- Atomic tasks plus compositional tasks
- Gated instances and unified leaderboard
- Programmatic validation and oracle solutions

What to adopt:

- Split benchmark into atomic subskills and compositional workflows
- Use real enterprise workflows as inspiration
- Keep official infrastructure controlled enough to preserve integrity

This is especially relevant because TheStartupBench is also a knowledge-work benchmark, not just an action benchmark.

### 5.7 MLE-bench

Reference:

- https://github.com/openai/mle-bench

Relevant methodology:

- External score-based evaluation
- Per-task grading scripts
- Rule-violation and plagiarism detectors
- Public known-issues log
- Versioned leaderboard evolution

What to adopt:

- Dedicated exploit detection and rule-violation checks
- Public known-issues ledger
- Versioned leaderboard columns
- Use of externally meaningful scores where possible

This is highly relevant for business benchmarking because agents may exploit simulation loopholes instead of making good decisions.

### 5.8 Terminal-Bench

Reference:

- https://github.com/harbor-framework/terminal-bench

Relevant methodology:

- Each task has instruction, test script, and oracle solution
- Execution harness is separate from task definition
- Dataset and version are explicit leaderboard inputs

What to adopt:

- Every official scenario should have:
  - a scenario specification
  - an evaluator
  - an oracle policy or expert trace
  - a version identifier

### 5.9 tau-bench

References:

- https://github.com/sierra-research/tau-bench
- https://arxiv.org/abs/2406.12045

Relevant methodology:

- Multi-turn tool-agent-user interaction
- Policy-constrained domains
- Final world-state comparison against annotated goal state

What to adopt:

- Stakeholder interaction as part of evaluation
- Policy documents that constrain valid decisions
- State-difference evaluation, not just answer matching

### 5.10 tau2-bench

References:

- https://github.com/sierra-research/tau2-bench
- https://arxiv.org/abs/2506.07982

Relevant methodology:

- Dual-control environment
- Compositional task generator
- User simulator constrained by tools and observable state
- Error decomposition into reasoning versus communication and coordination

What to adopt:

- Shared-control scenarios where the user, customer, employee, or board member also acts on the world
- Compositional scenario generation from atomic business primitives
- Fine-grained error analysis separating planning errors from stakeholder-management errors

This is one of the most directly useful benchmarks for startup settings.

### 5.11 AppWorld

Reference:

- https://github.com/StonyBrookNLP/appworld

Relevant methodology:

- Persistent world of apps, APIs, people, and tasks
- Train/dev with richer ground truth, hidden test details for official evaluation
- Database-state-based evaluation
- Explicit release disclaimer about benchmark contamination risk

What to adopt:

- Persistent world model
- Tool/API documentation embedded in environment
- Train/dev/test split discipline
- State-based evaluation over code/process traces
- Release warnings and contamination awareness

### 5.12 ToolSandbox

References:

- https://github.com/apple/ToolSandbox
- https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark

Relevant methodology:

- Stateful tool execution
- Implicit state dependencies across tools
- Built-in user simulator
- Dynamic evaluation of intermediate and final milestones

What to adopt:

- Stateful business operations where one action changes the feasibility of later actions
- Intermediate milestone evaluation, not only final horizon outcomes

### 5.13 OSWorld

Reference:

- https://os-world.github.io/

Relevant methodology:

- Execution-based evaluation in realistic computer environments
- Reliable setup scripts
- Unified settings for fair comparison
- Benchmark refresh via a "Verified" improvement process

What to adopt:

- Strong environment reproducibility
- Official verified re-releases when benchmark flaws are found
- Consistent evaluation settings across models

### 5.14 LiveCodeBench

Reference:

- https://github.com/LiveCodeBench/LiveCodeBench

Relevant methodology:

- Continuous collection of fresh tasks
- Time-window-based contamination mitigation
- Multiple capability slices instead of one narrow score
- Errata tracking

What to adopt:

- Rolling task windows for startup scenarios
- Benchmark slices by capability
- Public errata and release notes

### 5.15 SWE-Lancer

References:

- https://arxiv.org/abs/2502.12115
- https://github.com/openai/SWELancer-Benchmark

Relevant methodology:

- Mapping benchmark performance to economic value
- Separate independent execution tasks from managerial decision tasks
- Different evaluators for implementation and managerial choices

What to adopt:

- Tie performance to economic outcomes when possible
- Include both operator tasks and managerial decision tasks
- Use different evaluation mechanisms for different task classes

This is directly relevant for a startup benchmark because business work is partly operational and partly managerial.

## 6. Synthesis: methodology patterns TheStartupBench should adopt

TheStartupBench should explicitly adopt the following methodology stack:

- Executable evaluation
- Hidden official test split
- Rolling scenario refresh
- Fixed official scaffold
- Repeated runs with uncertainty reporting
- State-based evaluation
- Atomic plus compositional task structure
- Multi-stakeholder interaction
- Policy-constrained action spaces
- Fine-grained error taxonomy
- Public errata and versioning
- Contamination and exploit monitoring

## 7. Methodology patterns TheStartupBench should reject

TheStartupBench should explicitly avoid:

- Static public benchmark as the sole flagship metric
- Single-scenario or single-seed claims
- Single scalar score with no subscores
- Heavy dependence on LLM judges for outcome scoring
- Overly gameable reward shaping
- Exposing privileged simulator internals to the agent
- Rewarding benchmark-specific heuristics that do not transfer to real operations

## 8. TheStartupBench benchmark philosophy

The benchmark should model startup operation as a partially observed, dynamic control problem with multiple stakeholders and delayed consequences.

It should measure whether the agent can:

- infer what matters
- choose what to do next
- allocate scarce resources
- communicate effectively
- adapt when the world changes
- preserve strategic coherence over time

TheStartupBench should reward outcomes that are good for a real operator, not outcomes that are merely good for a simulator exploit.

## 9. Core benchmark entities

The benchmark world should include:

- Company
- Market
- Customers
- Prospects
- Competitors
- Team
- Capital providers
- Regulators and compliance constraints
- Product and roadmap
- Revenue model
- Operating systems and internal tools
- Event engine

Each entity should expose only the information a real operator would plausibly have.

## 10. Core company state

At minimum, each scenario state should include:

### 10.1 Finance

- Cash balance
- Burn
- Revenue and gross margin
- Accounts receivable and payable
- Runway
- Budget commitments
- Financing options
- Cap table state where relevant

### 10.2 Product

- Features
- Roadmap items
- Bugs and incidents
- Technical debt
- Product quality
- Launch state

### 10.3 Growth and GTM

- Activation funnel
- Retention and churn
- Sales pipeline
- Win/loss history
- CAC and payback
- Pricing plans
- Expansion opportunities

### 10.4 Team and organization

- Headcount
- Roles and skills
- Hiring funnel
- Morale
- Manager load
- Attrition risk
- Execution bandwidth

### 10.5 Market and competitors

- Segment demand
- Market growth
- Competitor launches
- Platform dependencies
- Regulatory or macro shifts

### 10.6 Governance

- Board expectations
- Milestones
- Reporting cadence
- Investor sentiment

## 11. World model design

The simulation should be hybrid:

### 11.1 Structural model

Deterministic or seeded-stochastic equations for:

- retention and churn
- lead flow
- pipeline conversion
- pricing response
- burn and payroll
- hiring throughput
- incident probability
- productivity and delay

### 11.2 Event engine

Discrete or semi-discrete event system for:

- competitor launches
- outages
- enterprise procurement delays
- key employee departures
- PR crises
- pricing changes in infra dependencies
- board pressure events
- legal or compliance escalations

### 11.3 Semantic judgment layer

Used only when unavoidable, such as:

- board memo quality
- customer escalation response quality
- pricing rationale quality
- hiring rubric quality

Rules:

- semantic judging should be rubric-bound
- use multi-judge or calibrated judge ensembles
- never let semantic judging dominate total score
- preserve evaluator prompts and version them

## 12. Benchmark tracks

TheStartupBench should launch as a benchmark family with separate tracks.

### 12.1 TSB-0to1

Early wedge selection, PMF search, initial monetization, constrained runway.

### 12.2 TSB-B2B-SaaS

Pipeline management, enterprise sales, onboarding, renewals, pricing, support.

### 12.3 TSB-Consumer

Activation, retention, virality, content/product loops, growth efficiency.

### 12.4 TSB-DeepTech

Long R&D cycles, uncertain technical milestones, fundraising dependency.

### 12.5 TSB-Marketplace

Supply-demand balancing, trust and safety, liquidity, incentives.

### 12.6 TSB-Crisis

Incidents, security, regulatory pressure, PR management, customer trust preservation.

### 12.7 TSB-Scale

Org design, delegation, planning, cross-functional coordination.

### 12.8 TSB-Board

Investor communication, reforecasting, prioritization, strategic tradeoffs.

## 13. Atomic skills and compositional scenarios

Like WorkArena plus WorkArena++, TheStartupBench should separate atomic business skills from full operating scenarios.

### 13.1 Atomic tasks

Examples:

- calculate runway
- prioritize features under a budget
- choose a pricing plan
- respond to a churn-risk customer
- write a hiring plan
- evaluate a sales pipeline
- decide whether to ship or delay

### 13.2 Compositional scenarios

Examples:

- navigate a 16-week PMF search with shrinking runway
- survive a competitor launch while retaining top customers
- re-forecast the company after missed revenue and rising infra costs
- decide whether to fundraise, cut burn, or pivot

Atomic tasks are good for diagnostics.

Compositional scenarios are what should matter most on the flagship leaderboard.

## 14. Time structure

The benchmark should support multiple cadences:

- single decision
- daily operations
- weekly planning
- monthly board cycle
- quarterly strategic horizon

Recommended default for v1:

- weekly turns
- 24 to 52 simulated weeks

Why:

- enough delay for consequences to matter
- not so granular that evaluation becomes dominated by busywork

## 15. Agent interface design

The agent should operate through explicit business tools, not unrestricted "god mode."

### 15.1 Core tool families

- `metrics.query`
- `product.roadmap`
- `product.launch`
- `growth.experiment`
- `sales.pipeline`
- `sales.pricing`
- `finance.plan`
- `finance.raise`
- `people.hire`
- `people.reorg`
- `ops.incident`
- `board.update`
- `research.market`
- `notes.write`

### 15.2 Input surfaces

- dashboards
- customer inbox
- CRM
- support queue
- engineering issue tracker
- board requests
- financial reports
- market research reports
- legal/compliance memos

### 15.3 Information constraints

The agent should not see:

- hidden latent variables
- full causal equations
- official grading criteria
- unreleased scenario metadata
- oracle policies

## 16. Shared-control design

Borrowing from tau2-bench, some benchmark scenarios should require other actors to take actions in the world.

Examples:

- customer must approve procurement
- candidate must accept offer
- employee must execute assigned work
- board must approve financing
- legal counsel must review a response

The agent's job is then partly:

- reasoning
- sequencing
- communication
- instruction quality
- coordination

This is important because real startup work is often not single-control.

## 17. Scenario design primitives

Every scenario should be generated or authored from reusable primitives:

- market segment
- business model
- customer profile
- channel mix
- team composition
- tech maturity
- cash state
- stakeholder pressure
- shock types
- policy constraints
- time horizon

This supports diversity, controlled difficulty, and future scenario generation.

## 18. Difficulty model

Difficulty should be defined along independent axes:

- information ambiguity
- action branching factor
- time pressure
- capital pressure
- stakeholder conflict
- coupling across functions
- delay between action and consequence
- number of active constraints

This should be stored as metadata and used for analysis, not shown to agents on hidden tests.

## 19. Scoring model

The benchmark should never use one simplistic score such as final cash or survival alone.

### 19.1 Proposed top-level score

Use a constrained weighted score:

`TSB Score = Outcome Score x Constraint Satisfaction Multiplier`

Where:

- Outcome Score reflects economic and operational performance
- Constraint Satisfaction Multiplier penalizes violations such as bankruptcy, compliance breaches, severe trust loss, or severe morale collapse

### 19.2 Outcome components

- enterprise value proxy
- revenue quality
- cash efficiency
- product health
- customer health
- organizational health
- strategic coherence

### 19.3 Constraint components

- no bankruptcy or controlled distressed operation only
- no severe compliance violation
- no severe customer trust breach
- no catastrophic people collapse

### 19.4 Track-specific subscores

Per track, publish:

- survival or completion rate
- median score
- pass@k
- variance across scenarios
- cost efficiency
- decision latency

## 20. Economic realism

Economic realism should be explicit, but the benchmark should avoid overclaiming.

Recommended design:

- map some scenario outcomes to dollarized or utility-like proxies
- include downside asymmetry
- include delayed compounding
- include model-cost accounting

Possible reported metrics:

- expected enterprise value delta
- avoided loss
- cash generated or preserved
- score per dollar of API spend

The benchmark should use economics for interpretability, not as fake startup valuation theater.

## 21. Evaluation modes

TheStartupBench should support three official evaluation modes.

### 21.1 Dev mode

- public scenarios
- full reproducibility
- rich diagnostics

### 21.2 Hidden test mode

- official leaderboard
- hidden scenarios or hidden evaluator internals
- centralized runs preferred

### 21.3 Fresh mode

- periodically refreshed scenarios
- release-date contamination gating
- "live" leaderboard slice

## 22. Reproducibility requirements

Every official run should log:

- model identifier
- provider
- system prompt hash
- tool schema version
- benchmark version
- scenario version
- seed
- runtime settings
- action trace
- state trajectory snapshots
- costs
- final evaluator outputs

Without this, benchmark claims should not be accepted as leaderboard-grade.

## 23. Leaderboard policy

Official leaderboard entries should require:

- same official scaffold
- same tool contract
- same benchmark version
- minimum repeated runs
- declared cost
- declared model date/version
- contamination declaration
- exploit declaration

Recommended leaderboard columns:

- overall TSB score
- track scores
- survival/completion rate
- pass@k
- SEM / confidence intervals
- cost
- wall-clock time
- benchmark version
- contamination flag
- source code availability
- trace availability

## 24. Anti-gaming design

The benchmark should be designed under the assumption that strong labs will optimize against it directly.

### 24.1 Required controls

- hidden official test scenarios
- private evaluator details where needed
- canary scenarios
- exploit detectors
- policy-violation detectors
- rolling scenario refresh
- release-date contamination filters
- periodic benchmark audits

### 24.2 Exploit classes to defend against

- simulator loopholes
- privileged-state inference via metadata leaks
- overfitting to public dev templates
- semantic judge prompt exploitation
- reward hacking via narrow score optimization
- scripted benchmark-specific heuristics

## 25. Human baselines

TheStartupBench should not launch without human baselines.

At minimum:

- random baseline
- trivial heuristic baseline
- strong scripted baseline
- non-expert human baseline
- startup operator baseline
- expert functional baseline for selected tracks

These baselines should be used to validate:

- task solvability
- difficulty ordering
- benchmark signal quality
- model-versus-human interpretation

## 26. Error taxonomy

Every failed or low-quality run should be classifiable.

Recommended top-level error taxonomy:

- perception error
- data interpretation error
- strategic reasoning error
- sequencing error
- coordination error
- communication error
- policy violation
- financial discipline failure
- local optimization at global cost
- failure to adapt after feedback
- exploit attempt

This is critical for research usefulness.

## 27. Data and scenario lifecycle

TheStartupBench should have an explicit scenario promotion pipeline.

### 27.1 Scenario sources

- expert-authored business cases
- procedurally generated cases from validated primitives
- synthetic but audited event trees
- carefully transformed real-world business archetypes

### 27.2 Promotion stages

- draft
- internally tested
- human solvability reviewed
- dev split
- hidden test split
- retired

### 27.3 Retirement criteria

- contamination risk too high
- exploit identified
- evaluator unfairness
- state model bug
- scenario saturation

## 28. Governance and versioning

There should be a benchmark governance process from the start.

Recommended:

- semantic versioning for benchmark releases
- scenario-level versioning
- public changelog
- errata log
- leaderboard version columns
- benchmark review board with domain experts and eval experts

## 29. Concrete differentiation from current benchmarks

TheStartupBench differs from major existing benchmarks in the following way:

### 29.1 Versus SWE-bench family

SWE benchmarks test issue resolution in software repositories. TheStartupBench tests business operation across multiple functions and delayed feedback loops.

### 29.2 Versus GAIA

GAIA tests general assistance on human-simple, tool-heavy problems. TheStartupBench tests persistent operating judgment inside a business system.

### 29.3 Versus WebArena and WorkArena

WebArena and WorkArena test browser workflows and knowledge-work automation. TheStartupBench tests cross-functional decision quality in a simulated company where browser-like tools are only one component.

### 29.4 Versus tau-bench and tau2-bench

tau benchmarks test conversational agents in tool/policy environments. TheStartupBench extends that idea into company management with broader state, longer horizon, and richer business objectives.

### 29.5 Versus AppWorld

AppWorld is a persistent app-and-API world for interactive coding and tool use. TheStartupBench should borrow its world-model rigor while centering business strategy and operations instead of app orchestration.

### 29.6 Versus MLE-bench

MLE-bench measures ML engineering work with external score functions. TheStartupBench similarly needs externalized business score functions where possible, but in a richer multi-objective environment.

## 30. TheStartupBench v1 proposal

V1 should be deliberately scoped.

### 30.1 V1 tracks

- TSB-B2B-SaaS
- TSB-Consumer
- TSB-Crisis

### 30.2 V1 scenario count

- 60 public dev scenarios
- 150 hidden official test scenarios
- 30 fresh rolling scenarios added quarterly

### 30.3 V1 horizon

- 24 weeks default

### 30.4 V1 tools

- metrics
- CRM
- finance
- roadmap
- hiring
- board updates
- experiments
- incident response

### 30.5 V1 evaluation

- 5 repeated runs per model setting
- centralized leaderboard runs preferred
- public trace format
- official score plus track subscores

## 31. Suggested implementation architecture

### 31.1 Core packages

- `tsb_core`
- `tsb_env`
- `tsb_scenarios`
- `tsb_eval`
- `tsb_leaderboard`
- `tsb_baselines`

### 31.2 Scenario file structure

Each scenario should define:

- metadata
- initial state
- latent variables
- event schedule or generator
- available tools
- evaluator configuration
- oracle metadata

### 31.3 Runtime loop

1. Load scenario and seed
2. Initialize visible state and hidden latent state
3. Provide tool interface and context surfaces
4. Accept agent actions
5. Apply business state transitions
6. Advance event engine
7. Evaluate milestones
8. Repeat until horizon or terminal condition
9. Produce final scorecard and trace

## 32. Recommended evaluation report format

Every official report should contain:

- executive summary
- benchmark version and date
- model and settings
- cost and runtime
- overall score
- track scores
- variance measures
- failure taxonomy summary
- benchmark caveats
- scenario coverage summary

## 33. Open design questions

These should be resolved before implementation:

- How much of the world should be deterministic versus stochastic?
- What percentage of score should come from semantic judging?
- Should fundraising be included in v1 or delayed to v2?
- How much free-form communication should agents be allowed?
- Should there be a separate benchmark for investor-facing versus operator-facing agents?
- What is the right week-to-turn ratio for balancing realism and tractability?
- What is the minimum viable hidden test set size for robust leaderboard use?

## 34. Immediate next steps

### Phase 1: benchmark specification

- freeze benchmark charter
- define track taxonomy
- define scorecard
- define trace schema

### Phase 2: scenario system

- implement scenario primitive library
- author 20 pilot scenarios
- create human baseline protocol

### Phase 3: evaluator and harness

- build official scaffold
- implement programmatic evaluators
- add exploit and policy detectors

### Phase 4: validation

- run scripted and human baselines
- audit solvability and fairness
- revise difficulty calibration

### Phase 5: public launch

- release dev split
- reserve hidden test split
- publish leaderboard protocol
- publish errata and governance policy

## 35. Final recommendation

TheStartupBench should be built as:

- a benchmark family, not a single simulator
- a stateful operating benchmark, not a roleplay benchmark
- a reproducible evaluation system, not a collection of anecdotes
- a contamination-aware live benchmark, not a static public test

If done correctly, TheStartupBench could become for startup and business decision agents what the strongest modern benchmarks are for coding, browser use, and tool use:

- not just a demo
- not just a leaderboard
- a durable measurement system

Implementation-ready follow-on documents now live under `spec/`, with machine-readable schemas under `schemas/` and an example scenario under `examples/`.
