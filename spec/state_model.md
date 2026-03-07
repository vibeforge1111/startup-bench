# State Model Specification

## 1. Purpose

The TSB state model defines the canonical business world representation used by scenarios, tools, evaluators, and traces.

It exists to ensure that:

- scenarios share a common vocabulary
- tools act on well-defined entities
- evaluators can compare world states consistently
- benchmark tasks remain composable

## 2. Design principles

The state model SHOULD be:

- modular
- partially observable
- causal enough to support meaningful transitions
- compact enough for scenario authoring
- extensible across tracks

The state model MUST distinguish:

- visible state
- latent state
- derived metrics
- policy state

## 3. Top-level state partitions

Every scenario world state SHOULD contain:

- `company`
- `finance`
- `product`
- `customers`
- `market`
- `team`
- `growth`
- `sales`
- `operations`
- `governance`
- `policy`
- `risk`
- `sim`

## 4. Company partition

Purpose:

- stable company identity and high-level strategic posture

Core fields:

- company id
- name
- stage
- sector
- business model
- target segments
- declared strategy

## 5. Finance partition

Purpose:

- track capital position and financial obligations

Core fields:

- cash
- restricted cash if applicable
- revenue
- gross margin
- burn
- payroll
- accounts receivable
- accounts payable
- debt or credit obligations
- runway
- financing options

Recommended sub-objects:

- `cash_flow`
- `budget`
- `fundraising`
- `unit_economics`

## 6. Product partition

Purpose:

- represent product state, roadmap, reliability, and delivery pressure

Core fields:

- active products or SKUs
- roadmap items
- quality and reliability indicators
- technical debt
- launch calendar
- incidents
- feature flags or experiment gates

## 7. Customers partition

Purpose:

- track customer health, adoption, and trust

Core fields:

- active accounts
- segments
- retention
- churn
- expansion potential
- NPS or trust proxy
- support load
- onboarding progress

The customer model SHOULD support both aggregate and account-level representations.

## 8. Market partition

Purpose:

- encode external conditions

Core fields:

- market growth
- demand by segment
- competitor posture
- platform dependencies
- regulatory climate
- macro conditions

## 9. Team partition

Purpose:

- represent people capacity and organizational constraints

Core fields:

- headcount by function
- open roles
- hiring funnel
- skill coverage
- morale
- attrition risk
- management load
- bandwidth allocation

## 10. Growth partition

Purpose:

- represent acquisition, activation, retention, and experimentation

Core fields:

- acquisition channels
- funnel metrics
- experiment backlog
- experiment results
- CAC
- payback
- growth constraints

## 11. Sales partition

Purpose:

- represent pipeline and commercial operations

Core fields:

- opportunities
- stage distribution
- forecast
- quota or target
- pricing plans
- procurement friction
- renewal schedule

## 12. Operations partition

Purpose:

- represent service health and execution operations

Core fields:

- incident queue
- reliability metrics
- support queue
- vendor dependencies
- operational bottlenecks

## 13. Governance partition

Purpose:

- represent board, investors, and milestone obligations

Core fields:

- board expectations
- covenant or milestone obligations
- reporting schedule
- stakeholder sentiment
- decision approvals required

## 14. Policy partition

Purpose:

- represent binding rules on action space

Core fields:

- spending rules
- approval policies
- legal constraints
- security constraints
- customer contractual obligations

## 15. Risk partition

Purpose:

- collect known and latent risks in a structured form

Core fields:

- risk register
- severity
- likelihood
- mitigation status

## 16. Sim partition

Purpose:

- represent simulation clock and execution metadata

Core fields:

- current time
- current turn
- horizon end
- pending event count
- budget counters

## 17. Entity granularity

The state model SHOULD support mixed granularity:

- aggregate metrics when individual entities are unnecessary
- entity-level rows where decisions act on specific accounts, hires, incidents, or roadmap items

Use entity-level records for:

- enterprise deals
- critical customers
- incidents
- board requests
- open roles
- major roadmap initiatives

## 18. Derived metrics

Derived metrics SHOULD be recomputable from base state where possible.

Examples:

- runway
- net revenue retention
- weighted pipeline
- coverage ratio
- incident severity score

Derived metrics SHOULD NOT be treated as independent hidden truth.

## 19. Visibility model

Every state field SHOULD be assigned a visibility class:

- `visible`
- `delayed_visible`
- `partially_visible`
- `latent`
- `evaluator_only`

This visibility class is critical for preventing agent leakage.

## 20. Mutation model

State transitions SHOULD be categorized as:

- deterministic mutations
- seeded stochastic mutations
- stakeholder-mediated mutations
- evaluator-only derived updates

## 21. Track extensions

Tracks MAY extend the state model with track-specific fields.

Examples:

- deeptech: technical milestone uncertainty
- marketplace: supply liquidity and fraud state
- board: financing and governance sensitivity

Core partitions SHOULD remain stable across tracks.

## 22. Implementation guidance

For implementation, maintain:

- a canonical internal state object
- a visible projection for the agent
- a derived metrics layer
- a diff engine for evaluators and traces

