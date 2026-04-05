# Refactoring Workflow

Detailed reference for when and how to refactor safely. The discipline of refactoring is as important as knowing the individual transformations. This reference covers the refactoring cycle, timing, safety techniques, and strategies for large-scale refactoring in production systems.

## Table of Contents
1. [The Refactoring Cycle](#the-refactoring-cycle)
2. [When to Refactor](#when-to-refactor)
3. [When NOT to Refactor](#when-not-to-refactor)
4. [Testing and Refactoring](#testing-and-refactoring)
5. [Refactoring and Performance](#refactoring-and-performance)
6. [Branch by Abstraction](#branch-by-abstraction)
7. [Parallel Change (Expand-Migrate-Contract)](#parallel-change-expand-migrate-contract)
8. [Large-Scale Refactoring Strategies](#large-scale-refactoring-strategies)
9. [Refactoring Checklist](#refactoring-checklist)

---

## The Refactoring Cycle

Every refactoring follows the same four-step loop:

```
1. Run tests → GREEN
2. Apply one small structural change
3. Run tests → GREEN
4. Commit
```

**Then repeat.**

### Why Small Steps Matter

| Approach | Risk | Recovery Time |
|----------|------|---------------|
| One refactoring at a time | Minimal -- if tests fail, the cause is obvious | Seconds (revert one change) |
| Several refactorings between tests | Medium -- must debug to find which one broke | Minutes |
| Big-bang rewrite | Maximum -- structural and behavioral changes mixed | Hours to days (or never) |

**Rule:** If a test fails after a refactoring step, **revert immediately**. Don't debug. The step was too big or wrong. Revert, think, try a smaller step.

### The Two Hats

Martin Fowler describes two distinct modes of work. You wear only one "hat" at a time:

| Hat | What You Do | What You Don't Do |
|-----|-------------|-------------------|
| **Refactoring** | Change structure, keep behavior identical | Add features, fix bugs, change tests |
| **Adding Function** | Add new behavior, write new tests | Change existing code structure |

**Switching hats:** You may alternate frequently, but never wear both at once. A typical sequence:

1. Refactoring hat: restructure to make the new feature easy to add. Commit.
2. Adding-function hat: add the feature and its tests. Commit.
3. Refactoring hat: clean up any mess the new feature introduced. Commit.

---

## When to Refactor

### Preparatory Refactoring (Refactor to Make the Change Easy)

**Trigger:** You're about to add a feature, and the code isn't structured to accommodate it easily.

**Example:** You need to add a new payment method. The payment logic is in a long if/else chain. Before adding the new branch, refactor to Replace Conditional with Polymorphism. Now adding the new payment method means creating one new class.

**Kent Beck's quote:** "Make the change easy (warning: this may be hard), then make the easy change."

**The payoff:** The feature is faster to add, less likely to contain bugs, and the refactoring improves the code for all future changes, not just this one.

### Comprehension Refactoring (Refactor to Understand)

**Trigger:** You're reading code and struggling to understand it. Rename variables, extract methods, and reorganize to make the code express its intent.

**Example:** You encounter a function called `calc` with variables named `a`, `b`, and `temp`. As you figure out what each does, rename them: `calculateMonthlyPayment`, `principal`, `interestRate`, `monthlyAmount`. The understanding you gain is encoded in the code itself.

**Ward Cunningham's insight:** "By refactoring, I move the understanding from my head into the code itself."

### Litter-Pickup Refactoring (Boy Scout Rule)

**Trigger:** You touch a file for any reason and notice a small improvement you can make. Do it.

**Examples:**
- Rename a misleading variable name
- Extract a method from a long function
- Remove dead code
- Add a missing guard clause

**The rule:** Leave the code cleaner than you found it. Each small improvement compounds over time. A codebase that is consistently cleaned by every developer who touches it stays healthy.

### Rule of Three

**Trigger:** The third time you see duplicated code or a repeated pattern.

**The progression:**
1. First time: Write it
2. Second time: Wince at the duplication but tolerate it
3. Third time: Refactor -- extract the common pattern

**Why three, not two:** Premature abstraction is as dangerous as duplication. Two occurrences might be coincidental. Three confirms the pattern.

### Long-Term Refactoring

**Trigger:** A large structural problem that can't be fixed in one session.

**Examples:**
- Replacing a library or framework
- Splitting a monolith into modules
- Changing a pervasive data representation

**Approach:** The team agrees on a target architecture. Everyone makes small changes toward it during regular work. No one stops feature development for a "refactoring sprint."

---

## When NOT to Refactor

Not every piece of code deserves refactoring. Save your effort for code that justifies it.

### Code You Should Leave Alone

| Situation | Why |
|-----------|-----|
| The code works and nobody needs to modify it | If it's behind a clean interface, its internal messiness costs nothing |
| It's easier to rewrite from scratch | If the code is small and the rewrite is straightforward, don't polish what you'll replace |
| There are no tests and adding them is impractical | Refactoring without tests is too risky; consider characterization tests first |
| The code will be deleted soon | Don't beautify code with a known end-of-life |
| You're exploring or prototyping | Throwaway code benefits from speed, not structure |

### The "Messy Middle" Trap

Some teams swing between two extremes:
- **Never refactor:** Technical debt accumulates until development grinds to a halt
- **Always refactor:** Gold-plating code that doesn't need it, shipping features slowly

The right balance: **Refactor code that you're about to change, or code that's actively hurting velocity.** Don't refactor code just because it's not beautiful.

---

## Testing and Refactoring

### The Safety Net

Tests are not optional for refactoring. Without them, you cannot verify that behavior is preserved.

| Test Type | Role in Refactoring |
|-----------|-------------------|
| Unit tests | Fast feedback on individual method behavior |
| Integration tests | Verify behavior across collaborating objects |
| Characterization tests | Capture existing behavior of legacy code (the starting point) |
| Regression tests | Ensure the entire system still works after changes |

### Characterization Tests

When you encounter code without tests that you need to refactor:

1. Run the code with known inputs
2. Observe the actual outputs (even if you think they're "wrong")
3. Write tests that assert the actual current behavior
4. Now you have a safety net -- refactor freely

**Example:**
```python
def test_weird_edge_case():
    # This behavior may be "wrong" but it's what exists.
    # Capture it so refactoring doesn't accidentally change it.
    result = calculate_shipping(weight=0, distance=100)
    assert result == 5.99  # Captures existing behavior
```

### Test-Driven Refactoring Steps

1. **Before starting:** Run all tests. If any fail, fix them first.
2. **After each refactoring step:** Run tests. All must pass.
3. **If a test fails:** Revert immediately. Don't debug.
4. **After completing a logical group of refactorings:** Commit.
5. **If you discover a bug during refactoring:** Stop refactoring. Fix the bug (adding-function hat). Then resume refactoring.

---

## Refactoring and Performance

### The Common Fear

"Won't all these small methods and indirection make the code slower?"

### The Reality

1. Most performance concerns about refactored code are unfounded. Modern compilers and runtimes inline small methods.
2. Performance bottlenecks are almost never where you think they are. Profile first.
3. Well-structured code is **easier** to optimize because the hot path is isolated.

### The Three-Step Performance Strategy

1. **Write clear code first.** Don't optimize during refactoring.
2. **Profile the running system.** Find the actual bottleneck (usually 10% of the code causes 90% of the performance issue).
3. **Optimize only the measured hot path.** Well-refactored code makes this easy because the hot path is in a small, isolated method.

### When Refactoring Genuinely Hurts Performance

| Refactoring | Potential Cost | Mitigation |
|-------------|---------------|------------|
| Replace Temp with Query | Method called multiple times instead of cached once | Cache if profiling shows impact |
| Extract Method | Additional method call overhead | Usually inlined by the compiler/JIT |
| Replace Conditional with Polymorphism | Virtual dispatch instead of branch | Negligible in most cases; profile if in doubt |
| Introduce Parameter Object | Object allocation for each call | Often optimized away; pool if necessary |

**Key insight:** Optimization and refactoring are separate concerns. Refactor first for clarity, then optimize the measured bottleneck.

---

## Branch by Abstraction

A technique for making large-scale changes to a widely-used component without creating a long-lived feature branch.

### When to Use

- Replacing a framework, library, or major internal component
- The replacement will take weeks or months
- You need to keep shipping features during the transition
- Feature branches would become stale and cause merge conflicts

### How It Works

```
Step 1: Identify the component to replace (OldComponent)
Step 2: Create an abstraction layer (interface) that wraps OldComponent
Step 3: Change all callers to use the abstraction (deploy incrementally)
Step 4: Create NewComponent that implements the same abstraction
Step 5: Switch the abstraction to point to NewComponent (one change, deploy)
Step 6: Remove OldComponent and the abstraction layer (clean up)
```

### Example

**Step 1-2:** Introduce the abstraction
```python
# Before: callers use OldPaymentGateway directly
class OldPaymentGateway:
    def charge(self, amount, card): ...

# After: introduce abstraction
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount, card): ...

class OldPaymentGateway(PaymentGateway):
    def charge(self, amount, card): ...  # existing implementation
```

**Step 3:** Migrate callers to use `PaymentGateway` (the abstraction). Deploy.

**Step 4:** Build `NewPaymentGateway(PaymentGateway)`. Test thoroughly.

**Step 5:** Switch the wiring:
```python
# In configuration:
# gateway = OldPaymentGateway()  # old
gateway = NewPaymentGateway()    # new
```

**Step 6:** Delete `OldPaymentGateway`. Optionally inline the abstraction if only one implementation remains.

---

## Parallel Change (Expand-Migrate-Contract)

A technique for making breaking API changes safely by running old and new versions side by side.

### When to Use

- Renaming a widely-used method or changing its signature
- Changing a data format while consumers still read the old format
- Migrating from one API to another when you can't update all consumers at once

### The Three Phases

**1. Expand:** Add the new version alongside the old one.
```python
class User:
    def get_full_name(self):     # new name
        return f"{self.first} {self.last}"

    def getFullName(self):       # old name, still works
        return self.get_full_name()  # delegates to new
```

**2. Migrate:** Update all callers to use the new version. This can happen incrementally across multiple deployments.

**3. Contract:** Remove the old version once all callers have migrated.
```python
class User:
    def get_full_name(self):     # only the new version remains
        return f"{self.first} {self.last}"
```

### Parallel Change for Data

```
1. Expand: Write to both old and new columns/formats
2. Migrate: Update all readers to use the new format
3. Contract: Stop writing the old format, remove old column
```

---

## Large-Scale Refactoring Strategies

### The Strangler Fig Pattern

Gradually replace a legacy system by building new functionality around it, routing more and more traffic to the new system until the old one can be decommissioned.

| Phase | Action |
|-------|--------|
| 1. Intercept | Place a routing layer in front of the legacy system |
| 2. Build new | Implement new components behind the router |
| 3. Redirect | Route requests to new components as they're ready |
| 4. Retire | Decommission old components once no traffic reaches them |

### Mikado Method

For complex refactorings with many interdependencies:

1. Try the refactoring you want to make
2. If it breaks, note what needs to change first (the prerequisites)
3. Revert your change
4. Recursively fix the prerequisites (each may have its own prerequisites)
5. Build a dependency graph (the "Mikado Graph")
6. Solve the graph from the leaves (no-dependency tasks) toward the root

### Feature Toggles During Refactoring

Use feature flags to gradually roll out a refactored component:

```python
if feature_flag('new_pricing_engine'):
    return new_pricing_engine.calculate(order)
else:
    return old_pricing_engine.calculate(order)
```

This allows:
- Incremental rollout (10% of traffic, then 50%, then 100%)
- Instant rollback by toggling the flag
- A/B comparison of old vs. new behavior

---

## Refactoring Checklist

Use this checklist before, during, and after refactoring sessions:

### Before Starting

- [ ] All existing tests pass (green)
- [ ] You've identified the specific smell or improvement target
- [ ] You can name the refactoring(s) you'll apply
- [ ] The code has test coverage for the area you'll change (add characterization tests if not)

### During Refactoring

- [ ] Each step is the smallest possible transformation
- [ ] Tests run after every step
- [ ] You revert immediately if tests fail (don't debug)
- [ ] You're wearing only the refactoring hat (no new features)
- [ ] You commit after each logical group of steps

### After Completing

- [ ] All tests still pass
- [ ] The code is easier to read than before
- [ ] Variable and method names reveal intent
- [ ] No unnecessary comments remain (the code explains itself)
- [ ] No new smells were introduced
- [ ] Changes are committed with a clear message describing the refactoring
