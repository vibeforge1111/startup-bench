# Real-World Startup Crisis Scenarios For TheStartupBench

Last updated: 2026-03-07

## Purpose

This document maps real startup and scale-up crises into benchmark-ready scenario archetypes for TheStartupBench.

The first executable pack derived from this catalog now lives in:

- [real_world_crisis_scenario_suite.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_crisis_scenario_suite.json)

The point is not to copy any one company’s exact incident. The point is to identify repeatable patterns:

- sudden demand collapse
- treasury/liquidity shock
- security compromise
- infrastructure outage
- scale bottleneck
- legal or policy backlash
- trust erosion
- board and stakeholder communication stress

## Selection Method

Each case below was selected because it has all or most of the following:

- the company is a successful startup or startup-origin company
- the event was materially hard, existential, or trust-threatening
- the company or a credible public source published a retrospective, statement, or postmortem
- the response included concrete actions, not just narrative
- the pattern can be abstracted into a reusable benchmark scenario

## The 20 Scenario Archetypes

| # | Company | Real event | What happened | How they navigated it | What TheStartupBench should test | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Airbnb | Pandemic demand collapse (2020) | Travel demand collapsed almost overnight, forcing a major reset of cost structure, priorities, and staffing. | Airbnb cut headcount, refocused the company, communicated the logic publicly, and reorganized around a changed market. | Whether an agent cuts burn fast enough, preserves trust, and reorients strategy instead of assuming a quick rebound. | https://news.airbnb.com/a-message-from-co-founder-and-ceo-brian-chesky/ |
| 2 | Buffer | Cash-flow crisis and layoffs (2016) | Buffer ran into a near-term cash crisis that required immediate expense reduction. | Buffer made layoffs, published the financial reality, and tied the change to a concrete recovery plan. | Whether an agent notices runway risk early, acts before insolvency, and communicates transparently to the team. | https://buffer.com/resources/layoffs-and-moving-forward/ |
| 3 | Brex | SVB treasury shock (2023) | The SVB failure created acute liquidity and payroll risk across the startup ecosystem. | Brex publicly diversified its own funds and moved fast to support customers facing treasury disruption. | Whether an agent diversifies counterparty risk, preserves payroll continuity, and reacts over a weekend without waiting for certainty. | https://www.brex.com/journal/press/brex-diversifies-its-own-corporate-funds-into-silicon-valley-bank |
| 4 | Zoom | Security and privacy backlash (2020) | Hypergrowth exposed security and privacy weaknesses, creating a trust crisis. | Zoom froze non-security feature work, launched a 90-day security plan, changed defaults, and communicated progress repeatedly. | Whether an agent trades short-term feature velocity for trust recovery when the product’s core legitimacy is under threat. | https://www.zoom.com/en/blog/update-on-zoom-90-day-plan-to-bolster-key-privacy-and-security-initiatives/ |
| 5 | Robinhood | Market-volatility outage (2020) | Unprecedented market activity stressed infrastructure during a critical customer moment. | Robinhood acknowledged the outage, attributed it to infrastructure stress, and committed to remediation. | Whether an agent prioritizes reliability under peak load, customer communication, and remediation after a high-visibility failure. | https://robinhood.com/newsroom/an-update-from-robinhoods-founders/ |
| 6 | Slack | Job queue scaling bottleneck (2017) | Slack’s asynchronous job system risked write unavailability when queue buildup exhausted Redis memory. | Slack introduced Kafka in front of Redis, rolled out incrementally, used double writes, and monitored heartbeat canaries. | Whether an agent chooses incremental de-risking over a heroic rewrite when a core system is near its limit. | https://slack.engineering/scaling-slacks-job-queue/ |
| 7 | Slack | Major product outage on 2-22-22 | A major outage disrupted the core product for a large user base. | Slack published a detailed incident analysis and focused on response coordination, diagnosis, and follow-up remediation. | Whether an agent can run incident command, prioritize recovery, and produce a credible post-incident improvement plan. | https://slack.engineering/slacks-incident-on-2-22-22/ |
| 8 | Notion | Database capacity crisis and live re-sharding (2023) | Core Postgres shards were at risk because of sustained traffic growth. | Notion horizontally re-sharded the fleet with no downtime, added capacity headroom, and staged the migration carefully. | Whether an agent invests ahead of failure, chooses scalable architecture, and plans zero-downtime migration work. | https://www.notion.com/blog/the-great-re-shard |
| 9 | Dropbox | Maintenance-script outage (2014) | A subtle bug in a maintenance script reinstalled active machines and caused a prolonged outage. | Dropbox restored service, published a postmortem, and explained the failure mode and lessons learned. | Whether an agent protects destructive operations with stronger safeguards, rollback planning, and blast-radius controls. | https://dropbox.tech/infrastructure/outage-post-mortem |
| 10 | Dropbox | Phishing-led source code compromise (2022) | Attackers impersonated CircleCI, captured GitHub credentials, and copied repositories. | Dropbox investigated quickly, disclosed the event, scoped impact, notified affected parties, and tightened controls. | Whether an agent treats internal-tool compromise as a real production crisis and responds with containment plus transparency. | https://dropbox.tech/security/a-recent-phishing-campaign-targeting-dropbox |
| 11 | Segment | Privileged-account security incident (2019) | An unauthorized party used a compromised employee account with privileged access to access customer-usage-related data. | Segment disclosed the incident, scoped the impact, and issued customer notices. | Whether an agent handles incident disclosure, customer notification, and privilege-boundary redesign under pressure. | https://segment.com/blog/bulletins-incident090519/ |
| 12 | Figma | Multi-incident service disruption (2022) | Repeated service disruptions blocked file opening and collaboration during a long instability window. | Figma diagnosed AWS ElastiCache behavior, redirected traffic, isolated workloads, and published a detailed postmortem. | Whether an agent avoids cargo-cult capacity fixes, isolates suspect workloads, and communicates progress during recurring failures. | https://www.figma.com/blog/postmortem-service-disruptions-on-june-6-and-7-2022/ |
| 13 | Linear | Largest outage in company history (2024) | A production incident led to platform downtime and partial data unavailability. | Linear restored data, published impact numbers, and removed dangerous privileges as part of remediation. | Whether an agent treats recovery design and privilege minimization as core follow-up work after a severe outage. | https://linear.app/blog/linear-incident-on-jan-24th-2024 |
| 14 | GitHub | Database and replication outage (2018) | A data-center failover triggered replication lag and a long restoration process. | GitHub favored data integrity over fast but risky failover and published a detailed incident report. | Whether an agent can choose the slower but safer recovery path when correctness and speed conflict. | https://github.blog/news-insights/company-news/october21-incident-report/ |
| 15 | GitHub | youtube-dl legal and policy backlash (2020) | A DMCA takedown created developer backlash and trust risk around platform neutrality and open source support. | GitHub reversed the removal, changed policy/process, and created a defense fund for developers. | Whether an agent can respond to a legal-policy crisis without treating it as only a PR issue. | https://github.blog/news-insights/policy-news-and-insights/standing-up-for-developers-youtube-dl-is-back/ |
| 16 | Atlassian | Accidental customer-site deletion outage (2022) | A script deleted hundreds of customer sites, creating a complex restoration effort lasting days. | Atlassian built large-scale restoration workstreams, mobilized support, improved communication, and committed to soft-delete protections. | Whether an agent can manage multi-day restoration, customer communications, and process redesign after an operator-caused disaster. | https://www.atlassian.com/blog/atlassian-engineering/post-incident-review-april-2022-outage |
| 17 | Coinbase | Internal SSL certificate outage (2021) | An expired internal certificate caused widespread production unavailability. | Coinbase published a postmortem, traced the dependency chain, and detailed prevention steps. | Whether an agent catches operational hygiene failures and improves certificate, dependency, and monitoring discipline. | https://www.coinbase.com/blog/incident-post-mortem-november-23-2021 |
| 18 | Shopify | BFCM traffic-tsunami readiness | Black Friday/Cyber Monday creates recurring extreme load that can function like a planned disaster test. | Shopify simulated traffic well above prior peaks, found bottlenecks early, and treated readiness as a year-round engineering program. | Whether an agent invests in readiness before the revenue-critical event instead of gambling on peak weekend survival. | https://shopify.engineering/bfcm-readiness-2025 |
| 19 | Stripe | Card-testing attack wave (2022) | Fraudsters launched large-scale card-testing attacks that could overwhelm merchants and increase disputes. | Stripe adapted Radar defenses, blocked large attack volumes, and documented mitigation guidance. | Whether an agent can distinguish abuse prevention from normal growth and deploy controls without crushing legitimate conversion. | https://stripe.com/en-mx/newsroom/news/card-testing-surge |
| 20 | Asana | Major product outage (2018) | Asana experienced hours of unavailability in a major incident. | Asana published a detailed incident write-up and traced both failure and response learnings. | Whether an agent can coordinate recovery, stakeholder updates, and hardening after a broad SaaS outage. | https://asana.com/pl/inside-asana/april-9-2018-asana-outage |

## How To Turn These Into Benchmark Tracks

These cases suggest at least six high-value scenario families:

1. Liquidity and runway shock
2. Trust and security crisis
3. Core infrastructure outage
4. Hypergrowth capacity bottleneck
5. Legal-policy backlash
6. Planned peak-event readiness

## Recommended Scenario Fields

Each benchmark scenario derived from these cases should encode:

- public facts the agent can observe
- hidden latent causes
- time pressure
- stakeholder pressure
- irreversible tradeoffs
- response costs
- recovery windows
- trust/compliance constraints

## Recommended Evaluation Dimensions

For crisis scenarios in particular, score the agent on:

- time to acknowledge
- time to stabilize
- correctness of the first mitigation
- avoidance of harmful “fixes”
- customer and board communication quality
- cash and trust preservation
- follow-up hardening quality
- whether the agent recognized when to pause growth or feature work

## Design Warning

These scenarios should be abstracted, not copied literally. A benchmark should borrow the structure of the crisis, not become a trivia test about a specific company’s history.

The right pattern is:

- keep the causal structure
- change company identity and surface details
- preserve the operational tradeoff
- preserve the hidden failure mode
- preserve the success and failure criteria

## Bottom Line

TheStartupBench should include real crisis patterns because startup quality is most visible under stress. The 20 cases above are strong raw material for a serious startup benchmark because they force tradeoffs across finance, trust, reliability, governance, and communication instead of rewarding shallow growth heuristics.
