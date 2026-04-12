# Build Less: The Philosophy of Deliberate Omission

## Table of Contents

- [The Core Argument](#the-core-argument)
- [Underdo the Competition](#underdo-the-competition)
- [Solve Your Own Problem](#solve-your-own-problem)
- [Embrace Constraints](#embrace-constraints)
- [Be a Curator](#be-a-curator)
- [Half a Product, Not a Half-Assed Product](#half-a-product-not-a-half-assed-product)
- [Focus on What Won't Change](#focus-on-what-wont-change)
- [The Feature Audit](#the-feature-audit)
- [Practical Application](#practical-application)

## The Core Argument

Most software fails not because it does too little, but because it does too much. Every feature added to a product carries hidden costs: maintenance burden, cognitive load for users, increased testing surface, documentation overhead, and opportunity cost. The 37signals philosophy inverts the default: instead of asking "What should we add?", ask "What can we leave out?"

This is not minimalism for its own sake. It is a strategic choice rooted in the reality of building products with small teams and limited resources. When you build less, you can build better. When you maintain less, you can move faster. When users have fewer choices, they make decisions more confidently.

Getting Real calls this "less software." Rework calls it "underdoing the competition." Both mean the same thing: the constraint of less is not a limitation — it is the competitive advantage.

## Underdo the Competition

The instinct when facing a competitor with more features is to match them. This is a trap. Feature parity is an arms race that favors incumbents with bigger teams and deeper pockets. The 37signals alternative: do less, but do it so well that the simplicity itself becomes the selling point.

**How underdoing works:**

- Competitor has 50 integrations? You ship 3 that work flawlessly and require zero configuration.
- Competitor has a full project management suite? You ship task lists with clear deadlines and nothing else.
- Competitor has 20 report types? You ship one report that answers the question 80% of users actually have.

Underdoing is not laziness. It requires harder decisions than overdoing. You must understand which 20% of functionality delivers 80% of the value, and have the discipline to ship only that.

**The psychology of underdoing:** Users experience feature overload as anxiety. A product with fewer, better features feels more trustworthy than one with dozens of half-implemented ones. Simplicity signals confidence — it says "we know what matters."

**When underdoing fails:** Underdoing fails when you cut core functionality, not peripheral features. The key is understanding the essential job your product does. A project management tool can skip Gantt charts but cannot skip task assignment. Know the job, then strip everything that does not directly serve it.

## Solve Your Own Problem

The surest way to build something valuable is to build something you need yourself. When you are your own user, you understand the problem intimately. You do not need extensive user research to know if a feature works — you use it every day. You do not need a PM to prioritize — your own frustration tells you what matters.

**Why self-use matters:**

- **Faster feedback loops.** You notice problems immediately because you experience them.
- **Authentic understanding.** You know the difference between nice-to-have and must-have because you feel it.
- **Reduced research overhead.** User interviews supplement your understanding rather than being your only source.
- **Better taste.** You develop strong opinions about how things should work because you live with the consequences.

Basecamp was built because 37signals needed a project management tool for their own client work. Ruby on Rails was extracted from Basecamp's codebase. HEY was built because they were frustrated with existing email clients. In each case, the product existed to solve a real problem the team experienced daily.

**The limitation:** Solving your own problem works best when your problem is shared by many others. It fails when your use case is too niche or idiosyncratic. The check: would at least a few thousand other people recognize this problem as their own?

## Embrace Constraints

Constraints — limited time, limited budget, limited people — are typically viewed as obstacles. The 37signals philosophy treats them as creative fuel. When you cannot do everything, you must find the essential version. When you have three people instead of thirty, you cannot afford unnecessary complexity. When you have six weeks instead of six months, you must cut to what matters.

**Types of constraints and their creative benefits:**

| Constraint | What It Forces | Creative Benefit |
|-----------|----------------|-----------------|
| Small team (2-3 people) | No specialization overhead, direct communication | Every person understands the whole; decisions happen fast |
| Fixed time (6 weeks) | Cannot build everything | Must find the simplest version that delivers value |
| No outside funding | Must be profitable early | Forces focus on features users will pay for, not vanity metrics |
| No dedicated PM role | Team owns decisions | No telephone game between decision-makers and builders |
| Simple technology stack | Cannot over-engineer | Solutions are maintainable and debuggable by the whole team |

**The paradox of constraints:** Teams with unlimited resources often ship slower and worse than teams with tight constraints. Abundance breeds indecision — when you can do anything, you debate endlessly about what to do. Scarcity breeds action — when you can only do one thing, you pick it and move.

## Be a Curator

Building software requires a curator — someone who decides what stays and what goes. Like a museum curator who selects which pieces belong in an exhibit, a product curator decides which features belong in the product. The curator's most important tool is the word "no."

**What curators do:**

- **Say no by default.** The default response to any feature request, any idea, any suggestion is no. Only the ideas that keep coming back, that solve real problems, that fit the product's opinion get through.
- **Remove, not just add.** Curators periodically audit the product and remove features that no longer earn their place. If a feature is rarely used and adds maintenance cost, it goes.
- **Maintain coherence.** A product with 100 well-curated features feels simple. A product with 20 random features feels complex. Coherence comes from having a clear opinion about what the product is for.
- **Resist epicycles.** An epicycle is a feature added to fix a problem caused by an earlier feature. Epicycles compound complexity. When you notice an epicycle forming, remove the root cause rather than adding another layer.

**The feature request trap:** Users request features that solve their immediate problem without considering the systemic cost. "Just add an option for X" sounds simple but adds one more preference, one more test path, one more thing to document. The curator's job is to understand the underlying need and find a solution that serves it without adding complexity.

## Half a Product, Not a Half-Assed Product

This is the most frequently quoted 37signals principle, and the most frequently misunderstood. It does not mean "ship something broken." It means: deliberately choose to build a complete, polished version of half the features rather than a half-finished version of all the features.

**What "half a product" looks like:**

- Every feature that ships works correctly, is well-designed, and is properly documented
- The product does fewer things but does each one with care and attention
- Users can accomplish the core job without workarounds or missing pieces
- The product feels finished, not like a beta

**What "half-assed" looks like:**

- Many features exist but most are partially implemented or buggy
- The product technically has a feature checklist but users hit walls constantly
- Edge cases are unhandled, error states are unhelpful, and flows are inconsistent
- The product feels unfinished despite being feature-rich on paper

**The decision framework:** Before adding a feature, ask: "If we add this, can we do it completely and well within our constraints?" If the answer is no, do not add it. A missing feature is invisible. A broken feature is visible and damaging.

## Focus on What Won't Change

Rework makes a sharp distinction between what changes (trends, technologies, competitors' features) and what does not change (speed, simplicity, reliability, ease of use, quality). The 37signals bet: invest in what will not change, because those investments compound forever.

**What does not change:**

- Users want software that is fast
- Users want software that is simple to understand
- Users want software that works reliably
- Users want clear communication (no jargon, no hidden surprises)
- Users want to accomplish their task with minimum friction

**What changes constantly:**

- Technology stacks and frameworks
- Design trends and visual styles
- Competitor feature sets
- Market narratives and buzzwords

Building on what does not change means your investment appreciates. Building on what changes means your investment depreciates.

## The Feature Audit

Periodically audit your product to identify features that no longer earn their place. Use this decision matrix:

| Feature State | Usage | Maintenance Cost | Action |
|--------------|-------|-----------------|--------|
| Core — defines the product | High | Any | Keep and invest |
| Useful — supports the core job | Moderate | Low | Keep |
| Useful — supports the core job | Moderate | High | Simplify or rebuild |
| Marginal — nice-to-have | Low | Low | Keep for now, monitor |
| Marginal — nice-to-have | Low | High | Remove |
| Legacy — served a past need | Minimal | Any | Remove |
| Epicycle — fixes problems from other features | Any | Any | Remove root cause instead |

**How to run the audit:**

1. List every feature in the product
2. Classify each by usage level and maintenance cost
3. Identify epicycles — features that exist only because of other features
4. Propose removals and simplifications
5. Ship the leaner version and measure impact

## Practical Application

**For product managers:** When prioritizing, start by asking "What can we remove?" before "What should we add?" Every removal simplifies the product for all users. Every addition complicates it for all users.

**For designers:** Design the simplest possible version first. Add elements only when their absence causes a real problem, not a theoretical one. If you are designing preferences, stop and ask which default would work for 80% of users.

**For engineers:** Resist the urge to build for hypothetical future requirements. Build what is needed now, build it well, and trust that you can extend it later if the need materializes. The best code is code you do not write.

**For founders:** Your competitive advantage is not features — it is focus. The company with fewer features and a clearer opinion will always out-execute the company trying to be everything to everyone.
