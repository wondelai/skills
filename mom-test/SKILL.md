---
name: mom-test
description: 'Talk to customers without leading them using Mom Test rules: discuss their life not your idea, ask about specifics in the past, and talk less. Use when the user mentions "customer interviews", "validate my idea", "users say they want it but dont buy", "leading questions", "The Mom Test", "customer feedback bias", "interview script", "how do I interview customers", "am I asking leading questions", or "is my customer feedback reliable". Also trigger when preparing user-research questions, interpreting ambiguous feedback, or designing customer-discovery that avoids false positives. Covers commitment and advancement, avoiding compliments, and extracting signal from noise. For product-market fit, see jobs-to-be-done. For rapid prototype testing, see design-sprint.'
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# The Mom Test Framework

Framework for customer conversations that won't lead you astray, based on a fundamental truth: everyone is lying to you -- not maliciously, but because you're asking the wrong questions. The Mom Test provides rules for asking questions so good that even your mom can't lie to you.

## Core Principle

**Good customer conversations are about their life, not your idea.** The moment you mention what you're building, people switch from sharing truth to performing politeness. Talk about their problems, their lives, and their existing behavior instead of pitching, and ask about specifics in the past, not hypotheticals about the future. Above all, talk less and listen more.

## Scoring

**Goal: 10/10.** Rate customer conversations 0-10 against the principles below: a 10/10 focuses entirely on the customer's life and past behavior, with no leading, no pitching, and clear commitment signals. Always state the current score and the specific improvements needed to reach 10/10.

## Framework Sections

### 1. The Mom Test Rules

**Core concept:** Three rules that make it impossible for even your most supportive loved ones to give you false validation, shifting conversations from opinion-gathering to fact-finding.

**Why it works:** People are unreliable predictors of their own future behavior, so opinions are worthless. Past behavior is the only reliable data and can genuinely inform product decisions.

**Key insights:**
- Rule 1: Talk about their life, not your idea -- never mention your solution until the end, if at all
- Rule 2: Ask about specifics in the past, not generics or hypotheticals about the future
- Rule 3: Talk less, listen more -- aim for them to speak 80% of the time
- A question fails the Mom Test if the answer is always "yes" regardless of whether the business will succeed
- Good questions could potentially destroy your currently imagined business

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Idea validation | Ask about the problem, never the solution | "Tell me about the last time you tried to [problem area]" not "Would you use an app that does X?" |
| Feature prioritization | Discover what people do vs. what they say | "Walk me through how you handled this last week" |
| Pricing research | Anchor to existing spending behavior | "What are you currently paying to solve this?" not "Would you pay $X?" |

**Copy patterns:**
- "Tell me about the last time you..."
- "How are you dealing with that currently?"
- "What else have you tried?"

**Ethical boundary:** Never weaponize someone's honest answers against them -- using vulnerability data to manipulate sales crosses the line.

See: [references/question-patterns.md](references/question-patterns.md) for good vs bad question examples, the three rules in depth, and formulation exercises.

### 2. Good vs Bad Questions

**Core concept:** Most interview questions are broken because they ask people to predict the future, evaluate hypothetical products, or confirm your assumptions. Good questions anchor in observable past behavior and extract concrete facts.

**Why it works:** Asking "would you buy this?" is like asking "will you go to the gym next week?" -- the answer is always yes, the follow-through rarely there. Behavior that already happened can't be rationalized away.

**Key insights:**
- Bad: "Do you think it's a good idea?" -- always gets a yes
- Bad: "Would you buy a product that does X?" / "How much would you pay?" -- hypothetical, anchored to please you
- Good: "How are you dealing with this problem today?" -- reveals actual behavior
- Good: "What have you tried before and why did you stop?" -- reveals past decisions
- Good: "Where does the money come from for solutions like this?" -- reveals real budgets
- The scariest questions -- ones with the power to change what you're building -- produce the most useful data

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Problem validation | Confirm the problem exists and matters | "When did this last come up? What did you do? What didn't work?" |
| Market sizing | Check if enough people share the problem | "Who else in your industry deals with this? How do they handle it?" |
| Competitive analysis | Find real alternatives already in use | "What tools/processes do you currently use for this?" |

**Copy patterns:**
- "What's the hardest part about [doing this thing]?"
- "How often does this come up?"
- "Talk me through the last time this happened"

**Ethical boundary:** Never use leading or loaded questions that anchor the respondent toward your desired answer -- your job is to learn, not to sell.

### 3. Avoiding Compliments and Opinions

**Core concept:** Three types of bad data feel like progress but actively mislead: compliments ("That's a great idea!"), fluff (hypotheticals, maybes, future promises), and ideas (feature requests disconnected from real problems). Deflecting these and digging for truth is the core skill.

**Why it works:** Compliments are the fool's gold of customer development -- they feel amazing but contain zero information about whether anyone will pay or use the product. Only specifics about real past behavior and genuine commitments provide signal.

**Key insights:**
- Compliments: deflect immediately and return to concrete facts about how they handle the problem today
- Fluff: generic claims ("I usually," "I always," "I would never") are worthless without a specific instance
- Ideas: dig into the motivation behind every feature request -- what's driving it, when they last needed it
- Fishing for compliments ("Don't you think this would be useful?") is unconscious validation-seeking
- Symptom of a bad conversation: you walk away feeling great but with no concrete facts or commitments

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Post-demo feedback | Deflect "this looks awesome" | "Thanks! What part of your current workflow would this replace?" |
| Feature requests | Dig for the underlying job | "Why do you want that? Can you show me the last time you needed it?" |
| Investor conversations | Separate encouragement from interest | Ask for customer intros, not "great idea" feedback |

**Copy patterns:**
- "Thanks, but to make sure I'm not wasting your time -- what does your current process look like?"
- "When you say you'd 'definitely' use this, what would you stop using?"
- "That's a great feature idea -- what problem would it solve for you specifically?"

**Ethical boundary:** Deflecting compliments is about getting to truth, not pressuring someone into a sale.

See: [references/avoiding-bad-data.md](references/avoiding-bad-data.md) for the three bad-data types and deflection scripts.

### 4. Commitment and Advancement

**Core concept:** The currency of a customer conversation is commitment, not compliments. End every conversation with a clear advance toward adoption or a clear rejection -- the worst outcome is a "zombie lead" who is polite but never commits.

**Why it works:** Saying "I'd definitely buy that" costs nothing; offering an intro, a deposit, or a pilot invests something real. Commitment closes the dangerous gap between what people say and what they do.

**Key insights:**
- Commitment currencies: time (meeting, trial), reputation (intro, testimonial), money (deposit, pre-order, letter of intent)
- Advancing moves the relationship toward a sale; spinning wheels produces pleasant, useless meetings
- Know your "ask" before the meeting -- the minimum commitment that proves this is real
- A "no" is more valuable than a "maybe" -- you can learn from it and move on
- If they won't give you their time, they definitely won't give you their money

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Early validation | Request a commitment that tests interest | "Can I follow up with a prototype next week for 15 minutes of your time?" |
| B2B sales | Advance toward the decision-maker | "Could you introduce me to the person who handles the budget for this?" |
| Pre-launch | Collect pre-orders or letters of intent | "Launching in 8 weeks -- want to join the first cohort at 40% off?" |

**Copy patterns:**
- "Who else should I talk to about this?"
- "Would you be willing to try a prototype next week?"
- "If I built this, would you be willing to pilot it for 30 days?"

**Ethical boundary:** Separate real interest from politeness -- never pressure people into commitments they'll regret.

See: [references/commitment-advancement.md](references/commitment-advancement.md) for commitment currencies and pushing for advancement.

### 5. Finding Conversations

**Core concept:** The best customer conversations happen casually -- warm intros, industry events, online communities, coffee. Formal "customer interview" framing triggers performance mode; casual framing produces honest data.

**Why it works:** "Can I interview you about your problems?" makes people polished and guarded; "I'm trying to learn about the industry -- can I buy you coffee?" makes them open up. The framing determines the quality of the data.

**Key insights:**
- Cold outreach: keep it short, lead with their expertise, don't pitch
- Warm intros are the best source -- one well-connected advisor can open dozens of doors
- Go where customers already gather: industry events, meetups, online communities (participate genuinely first)
- "I'm trying to learn" beats "I'm doing customer research"
- Use the five-part structure for getting meetings: vision / framing / weakness / pedestal / ask

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Pre-idea exploration | Immerse in the target community | 3 industry events and 20 casual conversations before writing code |
| B2B prospecting | Warm intros through advisors | "Our advisor [Name] suggested I ask how you handle [problem area]" |
| Consumer research | Intercept at the point of behavior | Talk to people in line at the store, the gym, the coworking space |

**Copy patterns:**
- "I'm researching how [industry] handles [problem] -- could I learn from your experience over a 15-minute coffee?"
- "[Mutual contact] suggested I talk to you because you know a lot about [area]"
- "I'm not trying to sell anything -- I'm just trying to understand the space"

**Ethical boundary:** Never disguise a sales call as a learning conversation -- if you already have a product and are selling, be transparent.

See: [references/finding-conversations.md](references/finding-conversations.md) for cold vs warm approaches and keeping it casual.

### 6. Processing and Learning

**Core concept:** Conversations are only useful if processed: distill raw notes into beliefs, update them regularly, and share with your team. Without a system you'll cherry-pick quotes that confirm your biases.

**Why it works:** Memory is biased toward recent and emotionally charged information, so teams selectively remember confirming data. Processing as a team prevents any one person's bias from dominating the narrative.

**Key insights:**
- Take notes during or immediately after -- never rely on memory
- Separate facts (what they said and did) from interpretations (what you think it means)
- Share raw notes with your team, not filtered summaries
- Update your three key beliefs after each batch: the problem, the customer segment, the solution
- Stop talking and start building when conversations start repeating
- Use a simple spreadsheet: who, date, key quotes, facts, commitments, belief changes

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| Team alignment | Review notes together weekly | 5 conversations per week reviewed as a team; belief board updated |
| Pivot decisions | Track evidence against core beliefs | 8 of 10 conversations reveal a different problem than expected -- pivot |
| Feature validation | Count unprompted mentions | A problem named by 7 of 10 people is real; 1 of 10 might not be |

**Copy patterns:**
- "Our current belief is X -- here's what confirms it and what challenges it"
- "We've heard this from N of M people -- is that enough signal?"
- "Time to stop talking and build -- conversations are repeating"

**Ethical boundary:** Never selectively quote conversations to justify a predetermined conclusion -- honest processing means accepting uncomfortable truths.

See: [references/processing-learning.md](references/processing-learning.md) for note-taking systems and knowing when to stop talking.

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Pitching your idea instead of asking about their life | Triggers politeness; produces compliments, not facts | Don't mention your idea until the very end, if at all |
| Asking "would you buy this?" | Hypothetical yeses cost nothing | Ask what they've already done: "How much are you spending on this now?" |
| Accepting compliments as validation | "Great idea!" carries zero information about behavior | Deflect immediately: "Thanks -- but what are you doing about this today?" |
| Talking too much | You learn while listening, not talking | They should talk 80%+ of the time |
| No clear ask at the end | Produces zombie leads that go nowhere | Know your advance before the meeting: trial, intro, pre-order |
| Running formal "interview" sessions | Triggers performance mode and filtered answers | Keep it casual: coffee, hallway conversations, Slack DMs |
| Not processing notes as a team | Individual bias filters data into confirmation | Share raw notes weekly; update shared beliefs together |

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Did the conversation focus on their life and past behavior, not your idea? | You ran a pitch, not a Mom Test conversation | Redo with zero mention of your solution |
| Did you get concrete facts about what they've already done? | You collected opinions and hypotheticals | Ask about the last time the problem occurred and what they did |
| Did they give a commitment (time, reputation, or money)? | Likely a zombie lead -- polite but not interested | Ask for a specific next step: trial, intro, or pre-order |
| Did they do most of the talking? | You talked too much and learned too little | Practice silence; let awkward pauses work for you |
| Did you learn something that could change what you're building? | You asked safe, confirming questions | Ask the scary questions you've been avoiding |
| Did you update your beliefs based on the conversation? | You're collecting data but not learning | Review notes with the team; update problem/segment/solution beliefs |
| Can you summarize the key facts (not opinions)? | Poor notes, or opinions confused with facts | Separate facts from interpretations immediately after |

## Reference Files

- [question-patterns.md](references/question-patterns.md): Good vs bad question examples, the three rules in depth, question formulation exercises
- [commitment-advancement.md](references/commitment-advancement.md): Commitment currencies, advancing vs spinning wheels, how to push for commitment
- [avoiding-bad-data.md](references/avoiding-bad-data.md): Compliments, fluff, ideas -- the three types of bad data and how to deflect them
- [finding-conversations.md](references/finding-conversations.md): Where to find people, cold vs warm approaches, keeping conversations casual
- [processing-learning.md](references/processing-learning.md): Note-taking, team sharing, updating beliefs, knowing when to stop talking
- [case-studies.md](references/case-studies.md): Realistic scenarios showing Mom Test principles applied to SaaS, consumer, B2B, and marketplace contexts

## Further Reading

This skill is based on Rob Fitzpatrick's Mom Test methodology:

- [*"The Mom Test: How to Talk to Customers & Learn if Your Business is a Good Idea When Everyone is Lying to You"*](https://www.amazon.com/Mom-Test-customers-business-everyone/dp/1492180742?tag=wondelai00-20) by Rob Fitzpatrick

## About the Author

**Rob Fitzpatrick** is an entrepreneur and educator who founded multiple venture-backed startups and learned the hard way that most customer conversations produce misleading feedback. *The Mom Test* (2013) distills his evidence-based approach, has been translated into 20+ languages, and is required reading at accelerators including Y Combinator and Techstars. He also wrote *The Workshop Survival Guide* and *Write Useful Books*.
