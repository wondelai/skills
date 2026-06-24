---
name: working-with-legacy-code
description: 'Safely change and test untested codebases using Feathers'' "Working Effectively with Legacy Code". Use when the user mentions "legacy code", "no tests", "untested codebase", "how do I test this", "seams", "characterization tests", "sprout method", "afraid to change this code", "monster method", "dependency breaking", "inherited a messy codebase", or "scared to touch this code". Also trigger when changing code without tests safely, getting a class under test when constructors, statics, or singletons block it, adding features to tangled modules, or planning incremental test coverage for an old codebase. Covers the legacy-code change algorithm, seams, characterization tests, sprout/wrap, and dependency-breaking techniques. For refactoring code that already has tests, see refactoring-patterns. For day-to-day code quality, see clean-code.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# Working Effectively with Legacy Code

A field manual for changing code that has no tests, distilled from Michael C. Feathers' *Working Effectively with Legacy Code*. Use it to get untestable classes into a harness, pin down current behavior with characterization tests, and make changes one safe, verifiable step at a time — without resorting to a rewrite.

## Core Principle

**Legacy code is simply code without tests.** Not old code, not ugly code — untested code: without tests you cannot know whether a change preserves behavior, so every edit is a gamble. The craft is breaking dependencies just enough to get tests in place before changing anything — cover and modify, never edit and pray.

## Scoring

**Goal: 10/10.** Rate changes to untested code 0-10 against the principles below. Report the current score and the specific steps needed to reach 10/10.

- **9-10:** Change points covered by characterization tests before any edit; behavior changes and refactoring shipped as separate verified steps; dependencies broken with the least invasive technique
- **7-8:** Tests at most change points, but occasional mixed refactor-plus-behavior commits or heavier dependency surgery than needed
- **5-6:** Some characterization tests, yet key paths still changed on faith; sprouted code accumulating with no payback plan
- **3-4:** Edit-and-pray with manual verification; tests written after the change, asserting whatever the new code happens to do
- **0-2:** Untested edits straight into tangled code, refactoring and behavior change mixed in one commit, rewrite proposed instead of tests

## Framework

### 1. The Legacy Code Dilemma and Change Algorithm

**Core concept:** The dilemma: to change code safely we need tests, but to get tests in place we have to change code. The way out is a fixed sequence — identify change points, find test points, break dependencies, write tests, then make changes and refactor — where the pre-test edits are conservative and mechanical, and the real change happens only inside the safety net.

**Why it works:** Edit-and-pray substitutes care for feedback, and care doesn't scale to code you don't fully understand. Cover-and-modify clamps existing behavior in a vise of tests, so any unintended change announces itself immediately on your machine instead of later in production.

**Key insights:**
- There are two reasons to change code — changing behavior (feature, bug fix) and improving structure (refactoring) — and mixing them in one step makes failures undiagnosable
- Test points are rarely the change points: effects propagate, so you often test where the change's effects surface, not where the edit happens
- Dependency-breaking edits made before tests exist must preserve signatures exactly and lean on the compiler to find every affected site
- Coverage grows along the paths you actually change — that beats any dedicated "testing project" that never gets funded
- "Programming is the art of doing one thing at a time": each step of the algorithm is separately verifiable

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Bug fix in an untested module | Run the five steps before touching the bug | Pin `parseInvoice()` with tests, then fix the rounding error |
| PR mixing cleanup and a feature | Split into structure-only and behavior-only commits | Extract and rename first, tests green, then add the discount rule |
| "It's just a one-line change" | Find the nearest test point first | One pin test at the public method that calls the private one you edit |

See: [references/change-algorithm.md](references/change-algorithm.md)

### 2. Seams: Where to Pry Code Apart

**Core concept:** A seam is a place where you can alter behavior in your program without editing in that place. Every seam has an enabling point — where you decide which behavior runs. Getting legacy code under test is largely a hunt for seams: spots where a test can substitute a slow, global, or external dependency while the production source stays untouched.

**Why it works:** If you must edit code to test it, you risk changing the very behavior you are trying to pin down. Seams move the substitution to a distance — a subclass, an import, a build flag — so the code under test runs exactly as in production while the test controls its dependencies from the enabling point.

**Key insights:**
- Object seams are the default in OO code: every overridable call is a seam, and its enabling point is wherever the object is created or passed in
- Link and import seams swap implementations at build or load time — `jest.mock` and `unittest.mock.patch` are link seams in modern clothing
- Preprocessing seams (C/C++ macros) are the bluntest instrument; reach for them last
- `new Database()` inside a method body is a seam that never got built — constructors doing real work, globals, statics, and hard-wired I/O are where seams die
- A seam without a reachable enabling point is useless: if the test can't make the decision, keep hunting
- Dynamic languages make nearly every name lookup a seam — cheap, but patching internals couples tests to file layout

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Class constructs its own DB client | Object seam via constructor parameter | `constructor(db: Db = new ProdDb())` — tests pass a fake |
| Module calls a top-level `send_email()` | Import/link seam | `mocker.patch("billing.send_email")` or `jest.mock("./mailer")` |
| Logic reads the wall clock directly | Seam at the clock | Inject a `now()` provider; tests freeze time |

See: [references/seams.md](references/seams.md)

### 3. Characterization Tests

**Core concept:** A characterization test documents what the code actually does right now — not what the spec, the comments, or anyone's memory says it should do. Write a probe you know will fail, let the failure message reveal the real behavior, then change the assertion to pin that behavior in place.

**Why it works:** In legacy systems the actual behavior is the de facto spec: callers, reports, and customers may depend on it, quirks included. Tests written from imagined requirements fail for reasons that tell you nothing, while characterization tests fail during refactoring precisely when — and where — you changed existing behavior.

**Key insights:**
- The recipe: call the code in a harness, assert something absurd (`expect(total).toBe(-1)`), read the failure, pin the observed value
- Sensing and separation are the two reasons to break dependencies: separation gets code into a harness, sensing lets assertions see what it computed
- For complex output (reports, generated files, large JSON) use a golden master: capture the full output once, diff against it forever
- Snapshot tests are golden masters — review the first snapshot like code and normalize volatile data, or you are pinning noise
- Found a bug while characterizing? Pin it with a comment and a ticket — downstream code may depend on the wrong behavior; fix it later as a deliberate, separate change
- Characterize the branches your change will touch, not the whole system — coverage follows change

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Refactoring a tax calculator | Pin outputs for representative inputs | Run 20 cases through, assert each recorded result |
| Legacy report generator | Golden master diff | Generate the report, compare to a checked-in master file |
| Off-by-one found while pinning | Pin the wrong value, document it | `assert days == 30  # BUG? expected 31 — TICKET-482` |

See: [references/characterization-tests.md](references/characterization-tests.md)

### 4. Sprout and Wrap: Changing Without Tests First

**Core concept:** When you genuinely cannot get the area under test today, don't weave new logic into the untested mass. Sprout Method or Sprout Class: write the new behavior as fresh, fully tested code and call it from a single line in the legacy spot. Wrap Method or Wrap Class: rename the old code aside and add behavior before or after the call to it, decorator-style.

**Why it works:** New code in a fresh method or class can be test-driven even when its host can't be instantiated in a harness. The untested host changes by one call site — old behavior remains byte-for-byte intact, new behavior arrives fully verified, and the risk stays contained to a single line.

**Key insights:**
- Sprout Method when new logic plugs in at one point; Sprout Class when the host class won't even instantiate in a test harness
- Wrap Method suits behavior that surrounds the old code (logging, notification, metering) rather than mixes with it: rename `pay()` to `rawPay()`, recreate `pay()` as the wrapper
- Wrap Class is the Decorator pattern — use it when several call sites need the added behavior or the class is already bloated
- Be honest about the trade-off: the host stays untested; you have added good code to a bad neighborhood
- Track sprouts as debt and pay them back — cover the host the next time a change lands there
- Sprouting is a tactical move inside the change algorithm, not a permanent substitute for getting code under test

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Late-fee rule in a 400-line `process()` | Sprout Method, one call line | `total += lateFee(order)` — `lateFee()` written test-first |
| Audit logging around legacy `pay()` | Wrap Method | New `pay()` logs, calls `rawPay()`, logs again |
| New validation, class won't instantiate | Sprout Class | `new OrderValidator().validate(data)` called from legacy code |

### 5. Dependency-Breaking Techniques

**Core concept:** A catalog of mechanical, low-risk moves that sever whatever blocks instantiation or sensing: Extract Interface, Parameterize Constructor, Parameterize Method, Extract and Override Factory Method or Getter, Introduce Instance Delegator, Adapt Parameter, Break Out Method Object, Subclass and Override Method. Because they run before tests exist, always pick the least invasive technique that unblocks you.

**Why it works:** Code resists testing for a small set of recurring reasons — constructors doing real work, statics and singletons, parameters you can't construct, monster methods. Each blocker has a named, practiced counter-move, so you execute a known maneuver instead of improvising surgery on code that has no safety net.

**Key insights:**
- Parameterize Constructor with a production default is the workhorse: existing callers compile untouched while tests inject fakes
- Extract Interface is the safest move in the book — introducing an interface can't change behavior, only loosen a type
- Subclass and Override Method underlies half the catalog: a testing subclass that stubs the dangerous parts is a legitimate tool, not a hack
- For statics and singletons, Introduce Instance Delegator hands callers an instance they can swap; a static setter can supersede a singleton in tests
- Adapt Parameter beats fighting unfakeable framework types — wrap `HttpServletRequest` in your own narrow interface and test against that
- Dynamic languages have cheaper seams: `unittest.mock.patch` or `jest.mock` can stand in for several techniques, but parameterizing leaves better design behind

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Constructor opens a DB connection | Parameterize Constructor | `def __init__(self, conn=None): self.conn = conn or connect()` |
| Static `Billing.charge()` called everywhere | Introduce Instance Delegator | Instance `charge()` delegates to the static; tests override it |
| 900-line method hoarding locals | Break Out Method Object | `new RateCalculation(order, rates).run()` — locals become fields |

See: [references/dependency-breaking.md](references/dependency-breaking.md)

### 6. Untangling and Understanding

**Core concept:** Before changing code you don't understand, invest in cheap comprehension: effect sketches trace what a change can affect, feature sketches show how methods and fields cluster inside a god class, scratch refactoring means refactoring recklessly to learn and then throwing the edits away, and telling the story of the system forces a simplifying summary. The payoff is finding pinch points — narrow places where a few tests cover wide behavior.

**Why it works:** In legacy code the bottleneck is comprehension, not typing. An effect sketch turns "what could this break?" from anxiety into a finite list, and a pinch point lets a handful of tests act as a vise over an entire cluster of methods — often revealing where a hidden class boundary wants to be drawn.

**Key insights:**
- Effect sketch: a bubble per variable or method, an arrow per "affects" — trace forward from your change point to every place behavior can leak out
- A pinch point is a narrowing in the effect sketch; test there and everything upstream of it is covered
- Scratch refactoring is refactoring as a reading technique: extract, rename, and simplify for an hour, then revert — the insight survives the checkout
- Monster method strategy: golden-master it at a pinch point, Break Out Method Object, then refactor inside the new class
- God class strategy: feature-sketch the clusters, then extract along the natural boundaries between them
- Triage when there's no time: a spot changing once gets a sprout or wrap; the same spot changing again has earned its tests

**Applications:**

| Context | Application | Example |
|---------|-------------|---------|
| "What breaks if I change this field?" | Effect sketch from the field outward | Three readers found; two pinch-point tests cover them |
| Feature due in a 5,000-line class | Pinch-point tests, then sprout | Cover `postInvoice()`, sprout the new rule as a class |
| Code nobody on the team understands | Scratch refactor on a branch | Extract and rename to learn, revert, plan the real moves |

See: [references/case-studies.md](references/case-studies.md)

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Refactoring and changing behavior in one step | When something breaks, you can't tell which edit did it | Separate commits; tests green between each step |
| Writing "should" tests on legacy code | Imagined specs fail noisily and you "fix" load-bearing behavior | Characterize what the code does; file bugs separately |
| Mocking everything in sight | Tests pin the implementation, so every refactor breaks them | Fake only what blocks instantiation or sensing |
| Big-bang rewrite instead of incremental coverage | The old system keeps moving; rewrites ship late and miss years of edge cases | Cover and modify piece by piece |
| Silently fixing bugs found while characterizing | Callers and reports may depend on the wrong behavior | Pin it, document it, fix it as a separate deliberate change |
| Invasive cleanup before any tests exist | Every manual edit risks behavior with no net underneath | Least invasive technique; preserve signatures; lean on the compiler |
| Sprouting forever without payback | The host stays untested and sprouts ossify into the next legacy layer | Track sprout debt; cover hot spots on the next touch |
| Waiting for a dedicated "testing project" | That project never gets funded; coverage never appears | Grow coverage along every change you ship |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Do tests cover the code you're about to change? | You're editing and praying | Run the change algorithm; pin behavior before editing |
| Can you construct the class in a test harness? | Dependencies block separation | Parameterize Constructor, Extract Interface, or Sprout Class |
| Can a test sense the effect of your change? | Effects are invisible to assertions | Find a sensing point; Extract and Override Getter |
| Is this commit behavior-only or structure-only? | Mixed changes are unverifiable | Split it; run the tests between the two |
| Do you know everything this change can affect? | Unknown blast radius | Draw an effect sketch; test at the pinch points |
| Do your assertions state observed behavior? | You're testing wishes, not code | Probe, read the failure, pin the actual value |
| Is the seam you chose the cheapest one available? | Needless surgery risks behavior | Prefer constructor parameters and import seams first |
| Will the code be better covered after this change? | The next change costs as much as this one | Leave at least one pin test at the nearest test point |

## Reference Files

- [change-algorithm.md](references/change-algorithm.md): The five-step algorithm as a working procedure — change points, test points, safety checklists, triage for "no time" situations, behavior-vs-structure discipline
- [seams.md](references/seams.md): Seam catalog with code — object, link/import, and preprocessing seams, enabling points, seams in modern stacks (DI containers, jest.mock, pytest monkeypatch, clock and config seams)
- [characterization-tests.md](references/characterization-tests.md): From first failing probe to a pinned suite — golden masters, snapshot tests done right, and a worked before/after refactor
- [dependency-breaking.md](references/dependency-breaking.md): Before/after code for each major technique plus a decision table mapping blockers to techniques
- [case-studies.md](references/case-studies.md): Three scenarios — a feature in an untested 800-line service, a singleton-ridden module brought under test, a monster method tamed before a bug fix

## Further Reading

- [*"Working Effectively with Legacy Code"*](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052?tag=wondelai00-20) by Michael C. Feathers
- [*"Refactoring: Improving the Design of Existing Code"*](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesley-Signature/dp/0134757599?tag=wondelai00-20) by Martin Fowler
- [*"Tidy First?: A Personal Exercise in Empirical Software Design"*](https://www.amazon.com/Tidy-First-Personal-Exercise-Empirical/dp/1098151240?tag=wondelai00-20) by Kent Beck
- [*"Kill It with Fire: Manage Aging Computer Systems (and Future Proof Modern Ones)"*](https://www.amazon.com/Kill-Fire-Manage-Computer-Systems/dp/1718501188?tag=wondelai00-20) by Marianne Bellotti

## About the Author

**Michael C. Feathers** is the founder of R7K Research & Conveyance, a consultancy focused on software design and the rehabilitation of aging systems. A long-time consultant and conference speaker on legacy code, he wrote *Working Effectively with Legacy Code* (2004) and gave the field its working definition: legacy code is simply code without tests.
