---
name: team-topologies
description: 'Organize business and technology teams for fast flow using Skelton & Pais''s "Team Topologies". Use when the user mentions "team topologies", "Conway''s law", "platform team", "stream-aligned team", "team boundaries", "cognitive load", "how should we split teams", "org design", "who owns this service", "team dependencies", "reorg", or "teams keep stepping on each other". Also trigger when reorganizing engineering teams, aligning team and service boundaries, splitting a monolith and deciding ownership, reducing cross-team handoffs, or designing an internal platform. Covers the four team types, three interaction modes, the inverse Conway maneuver, and fracture planes. For bounded contexts, see domain-driven-design. For dependency direction in code, see clean-architecture.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Team Topologies

A team-first approach to organization design from Matthew Skelton and Manuel Pais's *Team Topologies*: four fundamental team types, three interaction modes, and deliberate attention to Conway's law and team cognitive load. Use it to structure engineering organizations for fast flow of change — and to keep evolving them as the system, technology, and market shift.

## Core Principle

**The team is the unit of delivery, and organizations ship their communication structure.** Conway's law guarantees that system architecture mirrors how teams actually communicate, so team boundaries and interactions must be designed as deliberately as the software itself. Size each team's responsibilities to its cognitive load, align most teams to streams of business change, declare how teams interact, and treat the resulting topology as a living architecture decision that optimizes for fast flow.

## Scoring

**Goal: 10/10.** Rate org and team designs 0-10 against the principles below. Report the current score and the specific changes needed to reach 10/10.

- **9-10:** Stream-aligned teams own end-to-end slices sized to cognitive load; platform, enabling, and complicated-subsystem teams exist only to reduce that load; interaction modes are explicit and evolve deliberately
- **7-8:** Mostly stream-aligned with a real platform, but some shared ownership, undeclared interaction modes, or one overloaded team
- **5-6:** Team types named but boundaries cut by technology layer; collaboration unbounded; platform adoption mandated
- **3-4:** Component teams everywhere; ticket-driven shared services; every change crosses several teams
- **0-2:** Org ignores Conway's law: project-based staffing churn, "everyone talks to everyone", no notion of cognitive load

## Framework

### 1. Conway's Law and the Inverse Conway Maneuver

**Core concept:** "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure" (Mel Conway). Org communication and system architecture are homomorphic — they mirror each other by force, not by metaphor. The inverse Conway maneuver exploits this: decide the architecture you want, then shape teams and their communication paths so that architecture becomes the natural outcome.

**Why it works:** Teams can only build interfaces they can coordinate, so the space of designs an org can discover is constrained by its communication paths. Reshaping the org reshapes the system; fighting Conway's law instead produces permanent friction and architecture erosion.

**Key insights:**
- Interfaces emerge where teams communicate; seams emerge where they don't — the system records your org's conversations
- The *actual* communication structure (chat, code review, meeting invites) drives architecture, not the org chart
- "Everyone talks to everyone" produces tangled systems: unconstrained communication means unconstrained coupling
- A well-designed org needs *less* inter-team communication, not more — broad cross-team chatter signals wrong boundaries, not healthy collaboration
- Anyone who shapes teams, reporting lines, or hiring is making architecture decisions — architects must co-design the org, and reorgs need architectural review
- When the target architecture and the team structure conflict, the team structure wins

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Target architecture | Shape teams first; expect the architecture to follow | Want decoupled services → small decoupled teams with independent deploys |
| Reorg proposal | Review it as an architecture change | Tech lead/architect signs off on a team merge, not only HR |
| Tangled system | Map actual communication, not the org chart | Chat and review graph reveals hidden coupling between "independent" teams |

### 2. The Four Fundamental Team Types

**Core concept:** Reduce every team to one of four types. Stream-aligned teams own a flow of business change end to end — the primary type, and most teams. Enabling teams grow capabilities in stream-aligned teams and then move on. Complicated-subsystem teams encapsulate deep specialist knowledge (an ML model, a codec, a pricing engine). Platform teams provide a compelling internal product that reduces stream-aligned teams' cognitive load.

**Why it works:** Ambiguous charters ("the API team", "the DevOps team") accumulate work that belongs nowhere and interact unpredictably. Four well-defined types make gaps and overlaps visible, give every team a clear purpose relative to the flow of change, and make the rest of the org's expectations legible.

**Key insights:**
- Stream-aligned is the default; the other three types are justified only by the load they remove from streams
- An enabling team that never disengages has become a dependency — measure it by capabilities transferred, not tickets closed
- Complicated-subsystem teams are justified by genuine specialism, never by managerial convenience — most orgs need zero or one
- A platform is judged by cognitive load removed: if using it is harder than self-hosting, it is a liability with a roadmap
- Anti-patterns: shared-services teams become ticket-queue bottlenecks; a "DevOps team" between dev and ops adds a third silo; component teams everywhere mean every feature crosses many teams

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Ambiguous team charter | Force a choice among the four types | "Core services team" → platform with internal customers and SLAs |
| Deep specialist capability | Complicated-subsystem behind a simple interface | Recommendation-engine team exposes a scoring API to streams |
| New practice rollout | Enabling team, time-boxed | Test-automation specialists coach each stream for 8 weeks, then exit |

See: [references/team-types.md](references/team-types.md)

### 3. The Three Interaction Modes

**Core concept:** Teams interact in exactly three modes: collaboration (two teams work closely together for discovery), X-as-a-Service (one team consumes something another provides over a clear interface), and facilitating (one team helps another learn or improve). For every pair of interacting teams, choose one mode and declare it explicitly.

**Why it works:** Most organizational pain is an undefined interaction: a team expecting a service gets dragged into joint design; a team expecting coaching gets a ticket queue. Declared modes set mutual expectations, bound coordination cost, and turn interpersonal friction into a usable design signal.

**Key insights:**
- Collaboration is for discovery and is expensive — it blurs boundaries and raises both teams' cognitive load; time-box it, and limit each team to one collaboration at a time
- X-as-a-Service trades discovery speed for predictability — right for established interfaces, wrong while the boundary is still unknown
- Modes should evolve deliberately: collaborate to discover an interface, then shift to X-as-a-Service as it stabilizes
- Persistent friction is organizational sensing data: awkward collaboration suggests a wrong boundary; a clunky service suggests the platform needs product work
- A temporary, declared switch back to collaboration is the standard way to adopt a major new platform capability

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| New platform capability | Collaborate first, then X-as-a-Service | Stream and platform pair on a logging API for 6 weeks, then consume it |
| Two teams in endless meetings | Declare the intended mode | Agree it is a service relationship → cut standing syncs, publish the API |
| Capability gap in a stream | Facilitating engagement | Enabling team pairs on observability practices, exits within a quarter |

See: [references/interaction-modes.md](references/interaction-modes.md)

### 4. Team Cognitive Load and Team-Sized Software

**Core concept:** Match responsibilities to the team's cognitive capacity. Three load types apply to teams: intrinsic (the skills and technology the work inherently demands), extraneous (delivery mechanics: tooling, environments, process), and germane (the value-adding domain thinking). Minimize extraneous load, account for intrinsic load, and protect capacity for germane load — and size software to the team, never the reverse.

**Why it works:** When load exceeds capacity, teams thrash: context-switching, shallow ownership, defensive planning, rising lead times, on-call dread. Limiting domains per team keeps ownership deep enough for mastery, and long-lived teams amortize the months it takes a group to gel.

**Key insights:**
- Measure domains, not headcount: one complicated domain per team, never two; a team can hold two or three simple domains; never split one complicated domain across teams
- Bigger teams are not the fix for overload — fewer domains are; if the software exceeds team size, split the software
- A team API makes the team consumable: code, docs, on-call, chat channels, and working agreements that let others interact without meetings
- Long-lived teams beat project staffing — disbanding a gelled team discards months of trust, then pays the gelling cost again
- Respect Dunbar-sized groupings: ~5-9 people per team, then natural limits near 15, 50, and 150 for groupings of teams
- Extraneous load is the cheapest to remove: paved roads, templates, and platform services buy back germane capacity without a reorg

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team reports thrash | Count and classify its domains | 1 complicated + 3 simple domains → shed two simple ones |
| Slow cross-team onboarding | Publish team APIs | Each team lists owners, docs, on-call, channels, request path |
| Project ends | Keep the team, move the work | Re-point the gelled team at the next stream; never disband by default |

See: [references/cognitive-load.md](references/cognitive-load.md)

### 5. Fracture Planes: Splitting Software for Team Ownership

**Core concept:** Split software along natural seams — fracture planes — so each piece can be fully owned by one team. Business domain (a DDD bounded context) is the default plane; the others are regulatory compliance, change cadence, team location/timezone, risk, performance isolation, technology, and user personas.

**Why it works:** Software larger than one team's cognitive load forces shared ownership, and arbitrary or layer-based splits recreate cross-team coupling. Splitting along seams that change together keeps most changes inside one team — and when service boundaries match team boundaries, Conway's law works for you instead of against you.

**Key insights:**
- Default to business-domain splits; reach for another plane only with a concrete forcing reason (PCI scope, 10x performance hot spot, clashing change cadences)
- Technology is usually the worst plane — frontend/backend/DBA splits guarantee every feature needs three teams
- Litmus test for any proposed split: could this piece be offered as an independent service or SaaS? If not, the boundary leaks
- "Monolith" is more than code: monolithic databases, coupled release trains, and mandatory org-wide standardization all fight team independence
- Code owned by three teams is owned by no one — give every artifact one owner, extract it to a platform, or run it as inner source with a steward
- Different parts of one system can split along different planes; one plane need not rule the whole system

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Monolith decomposition | Map bounded contexts first | Orders, payments, catalog → three team-owned services |
| Compliance burden everywhere | Split by regulatory scope | PCI flows isolated in one audited service and team |
| Mixed change rates | Split by cadence | Weekly-changing pricing separated from yearly-changing ledger |

See: [references/fracture-planes.md](references/fracture-planes.md)

### 6. Platform as a Product and Sensing/Evolving

**Core concept:** Run the platform as an internal product whose customers are the stream-aligned teams, starting from the Thinnest Viable Platform — the smallest thing that accelerates streams, which can be a wiki page curating vetted services. Then treat the whole topology as dynamic: use friction, wait times, and on-call signals to sense when team boundaries and interaction modes must change.

**Why it works:** Mandated platforms with captive users decay into bureaucracy because failure has no feedback channel; optional adoption forces the platform to stay compelling, and product discipline keeps it solving real needs. Orgs that treat topology as a one-time reorg drift back into Conway misalignment as products and markets shift.

**Key insights:**
- A platform is judged by cognitive load removed, not features shipped — bigger platform is not better platform
- Thinnest Viable Platform discipline: start with curation and docs ("use these services, this way"); build software only where curation stops being enough
- Internal developers are customers: do user research, publish a roadmap and SLAs, track adoption and developer experience like product metrics
- If streams can leave, the platform must compete on value — mandates hide platform failure until it is catastrophic
- Shadow platforms, growing wait times, recurring cross-team friction, and on-call pain are sensing signals that the topology needs to evolve
- No topology is final — revisit team boundaries and interaction modes every few quarters, on signals rather than ceremony

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Forming a platform team | Adopt product practices | Roadmap, internal user research, office hours, versioned APIs with SLAs |
| Platform sprawl | Re-anchor on the TVP | Cut to the six services streams actually use; curate the rest |
| Org feels "off" again | Run a sensing review | Friction log and wait-time data drive one deliberate boundary change |

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Creating a "DevOps team" between dev and ops | Adds a third silo and another handoff queue | Platform team for self-service tooling, or enabling team to grow capability |
| Permanent enabling teams | Capability never transfers; streams stay dependent | Time-box engagements with explicit exit criteria |
| Mandating platform adoption | Captive users hide failure; platform decays into bureaucracy | Keep adoption optional; make the platform compete on value |
| Splitting teams by technology layer | Every feature crosses several teams; handoffs dominate lead time | Split along business-domain fracture planes; stream-aligned ownership |
| Disbanding teams when projects end | Discards gelled trust; re-pays forming-storming cost every time | Long-lived teams; flow work to teams, not people to projects |
| Shared-services team as a ticket queue | Serializes every stream's work through one bottleneck | Convert to platform-as-product (self-service) or enabling team |
| Sizing teams by headcount, not cognitive load | Large teams still thrash when domains are too many or too complex | Count and classify domains; max one complicated domain per team |
| Leaving interaction modes implicit | Mismatched expectations; coordination meetings metastasize | Declare a mode per team pair; review and evolve it deliberately |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can each stream-aligned team deliver its typical change without handoffs? | Flow is blocked by queues between teams | Realign teams to end-to-end slices of business change |
| Is every team identifiable as one of the four types? | Ambiguous charters accumulate orphaned work | Classify each team; convert or dissolve the misfits |
| Is the interaction mode declared for each pair of dependent teams? | Friction from mismatched expectations | Declare collaboration, X-as-a-Service, or facilitating per pair |
| Is each team's domain count within cognitive-load heuristics? | Thrash, shallow ownership, slow delivery | Reassign domains; max one complicated domain per team |
| Do service and repo boundaries match team boundaries? | Conway misalignment; shared ownership creeps in | Re-split along fracture planes; one owner per artifact |
| Is platform adoption optional and measured by load removed? | Mandate is masking a failing platform | Run the platform as a product; track voluntary adoption and DevEx |
| Are enabling engagements time-boxed with exit criteria? | Permanent dependency replaces learning | Set end dates and capability-transfer goals up front |
| Is there a recurring mechanism to sense and evolve the topology? | Design rots as system and market shift | Quarterly review of friction, wait times, and on-call signals |

## Reference Files

- [team-types.md](references/team-types.md): Each team type in depth — responsibilities, staffing, success metrics, failure modes, converting existing teams, and a "which type is this team really?" decision guide
- [interaction-modes.md](references/interaction-modes.md): Mode-by-mode mechanics, team interaction contracts, time-boxing collaboration, designing X-as-a-Service interfaces, the facilitation playbook, and mode-evolution triggers
- [cognitive-load.md](references/cognitive-load.md): Assessing team cognitive load (survey, domain counting, on-call and tooling proxies), the full team API template, domain-allocation heuristics, and overload warning signs
- [fracture-planes.md](references/fracture-planes.md): The fracture-plane catalog with selection criteria, a monolith-to-team-ownership mapping exercise, DDD alignment, shared-code options, and sequencing an inverse Conway reorg
- [case-studies.md](references/case-studies.md): Three scenarios — a scale-up redesigned into stream-aligned plus platform teams, an ops team converted to platform-as-product, and a monolith split with explicit interaction modes

## Further Reading

- [*"Team Topologies: Organizing Business and Technology Teams for Fast Flow"*](https://www.amazon.com/Team-Topologies-Organizing-Business-Technology/dp/1942788819?tag=wondelai00-20) by Matthew Skelton & Manuel Pais
- [*"Accelerate: The Science of Lean Software and DevOps"*](https://www.amazon.com/Accelerate-Software-Performing-Technology-Organizations/dp/1942788339?tag=wondelai00-20) by Nicole Forsgren, Jez Humble & Gene Kim
- [*"The Mythical Man-Month: Essays on Software Engineering"*](https://www.amazon.com/Mythical-Man-Month-Software-Engineering-Anniversary/dp/0201835959?tag=wondelai00-20) by Frederick P. Brooks Jr.

## About the Authors

**Matthew Skelton** is the founder of Conflux, a consultancy for fast flow in software organizations, and co-author of *Team Topologies*. **Manuel Pais** is an independent IT organizational consultant and trainer specializing in team interactions and delivery practices. Both focus on team-first organization design that optimizes for fast, sustainable flow of change.
