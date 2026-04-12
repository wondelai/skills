# Opinionated Software and Clear Communication

## Table of Contents

- [What Opinionated Software Means](#what-opinionated-software-means)
- [Defaults Over Preferences](#defaults-over-preferences)
- [The Epicycle Trap](#the-epicycle-trap)
- [The Art of Saying No](#the-art-of-saying-no)
- [Clear Copywriting Principles](#clear-copywriting-principles)
- [Focus on What Won't Change](#focus-on-what-wont-change)
- [Out-Teach the Competition](#out-teach-the-competition)
- [Sell Your By-Products](#sell-your-by-products)

## What Opinionated Software Means

Opinionated software makes choices on behalf of the user. Instead of offering 15 configuration options, it picks the best one and ships it as the default — or the only option. Instead of supporting every possible workflow, it supports one workflow well and says "this is how we think it should be done."

This is the opposite of the "platform" mindset, where the goal is maximum flexibility. The 37signals mindset is: flexibility is complexity. Every option you add is a decision the user must make. Every configuration is a potential source of confusion. Opinionated software trades flexibility for clarity.

**Examples of opinionated decisions in Basecamp:**

| Area | Opinionated Choice | What They Did Not Build |
|------|-------------------|----------------------|
| Project structure | All projects have a message board, to-do lists, schedule, docs, and campfire chat | Custom project templates, configurable modules |
| Notifications | Sensible defaults with one toggle (on/off) per project | Per-event notification rules, notification schedules, do-not-disturb windows |
| Permissions | Simple owner/member model | Role-based access control, custom permission levels |
| File organization | Flat list with search | Folder hierarchies, tagging systems, metadata |
| Reporting | Built-in views that answer the most common questions | Custom report builder, query language, data export scheduler |

**The cost of having no opinion:** Software without opinions becomes a configuration puzzle. Users spend more time setting up the tool than using it. Support teams answer the same questions about which settings to use. And the product loses its identity — it becomes a generic platform rather than a tool that stands for something.

## Defaults Over Preferences

Every preference in your software represents a decision your team did not make. Some of these are legitimate — users genuinely have different needs. But most preferences exist because the team could not decide, or because one vocal user requested an option, or because "we'll just make it configurable" felt easier than choosing.

**The preference audit:**

For each preference or setting in your product, ask:

1. **What percentage of users change this from the default?** If it is less than 5%, remove the preference and keep the default.
2. **Is there a single best answer?** If yes, pick it and remove the option. Users do not want to choose — they want it to work.
3. **Does this preference exist because of a vocal minority?** One customer's request is not a mandate. Solve their specific problem differently.
4. **Does this preference create downstream complexity?** If a setting changes behavior in ways that affect other features, the complexity cost is high. Remove it.
5. **Would removing this break a significant use case?** If yes, keep it. If no, remove it.

**How to pick good defaults:**

- **Observe real behavior.** If you already have the preference, look at what most users choose. Make that the default.
- **Choose the safe option.** When in doubt, default to the option that is least likely to cause problems.
- **Choose the simple option.** When both options are safe, choose the one that requires less explanation.
- **Match user expectations.** What would a new user expect this to do without reading documentation? Do that.

**Example: Timezone settings.** Most software asks users to set their timezone. 37signals approach: detect the timezone from the browser. If you are wrong, the user can change it — but you should not make every user manually configure something that can be detected automatically.

## The Epicycle Trap

An epicycle is a feature added to fix a problem caused by an earlier feature. The term comes from Ptolemaic astronomy, where epicycles (circles upon circles) were added to explain planetary motion within a flawed model. In software, epicycles look like this:

1. You add a feature (bulk notifications)
2. Users complain it is noisy (because bulk notifications create too many alerts)
3. You add a preference to control notification frequency (epicycle 1)
4. Some users set it wrong and miss important notifications
5. You add a "priority notification" override (epicycle 2)
6. Users are now confused about the interaction between frequency settings and priority overrides
7. You add a documentation page explaining the notification system (epicycle 3)

Each epicycle makes the original problem worse by adding complexity. The 37signals solution: remove the root cause. If bulk notifications are noisy, fix the notification logic — do not add settings to let users manage the noise themselves.

**How to spot epicycles:**

- You are adding a feature whose primary purpose is to manage or configure another feature
- You are writing documentation to explain feature interactions
- Users need a "getting started guide" for a single feature
- You are adding an "advanced settings" panel
- A feature has more than two preferences

**How to break the cycle:**

1. Identify the root feature that caused the downstream complexity
2. Ask: "Is there a simpler version of this root feature that would not need the epicycles?"
3. Replace the complex version with the simple one
4. Remove all the epicycles

## The Art of Saying No

Saying no is the most important skill in product development. Every feature request, no matter how reasonable, competes with simplicity. The default answer to any request must be no — not because the idea is bad, but because the cost of yes is always higher than it appears.

**The hidden costs of yes:**

| Visible Cost | Hidden Cost |
|-------------|------------|
| Development time | Maintenance forever |
| Design work | Cognitive load for all users |
| Testing effort | Documentation and support burden |
| One-time feature | Ongoing compatibility with future features |
| Satisfying one user | Complicating the product for everyone |

**How to say no effectively:**

- **Be direct.** "We're not going to build this" is clearer and kinder than "We'll add it to the backlog" (which is a lie).
- **Do not apologize.** You are making a product decision, not committing a wrong. "Thanks for the suggestion. We've decided not to include this." is sufficient.
- **Explain your reasoning (briefly).** "We want to keep the notification system simple, and this would add a level of complexity we're not comfortable with." One sentence, not a paragraph.
- **Do not promise a future.** "Not now" implies "later." If you mean no, say no.
- **Acknowledge the need.** "I understand this would be useful for your workflow" shows empathy without creating commitment.

**When to say yes:** Say yes when a request solves a problem that many users share, aligns with the product's opinion, can be built simply, and fits within a cycle's appetite. That combination is rare — which is why no is the default.

**The "few vocal users" problem:** A small number of power users generate a disproportionate amount of feature requests. Their needs are real but not representative. Building for vocal power users at the expense of the quiet majority is a common product mistake. The check: how many users does this actually affect?

## Clear Copywriting Principles

The 37signals approach to copy is an extension of their product philosophy: simple, honest, and opinionated. Every word in the interface is a product decision.

**The rules:**

**1. Write for humans, not for marketers.** If a sentence would sound weird spoken aloud in a conversation, rewrite it. "Your file has been saved" is human. "Your asset has been successfully persisted to our cloud infrastructure" is not.

**2. No buzzwords.** Remove every instance of: "leverage," "synergy," "seamless," "robust," "cutting-edge," "next-generation," "holistic," "ecosystem," and any word that means nothing specific. Replace with plain language.

**3. Be specific.** "Fast" is vague. "Loads in under 2 seconds" is specific. "Easy to use" is vague. "Set up in 3 steps" is specific. Specificity builds trust; vagueness erodes it.

**4. Be honest about limitations.** If your product does not do something, say so. "Basecamp is not for everyone. Here's who it's for." This honesty attracts the right customers and repels the wrong ones — both good outcomes.

**5. Error messages are a product.** Every error message is a conversation with a frustrated user. "An unexpected error occurred" is abandoning that user. "We couldn't send that email. Check the address and try again." is helping them.

**6. Labels matter.** The name you give a feature shapes how users understand it. "Campfire" (Basecamp's chat feature) evokes warmth and informality. "Team Communication Module" does not.

**Copy before/after examples:**

| Before (Generic) | After (37signals Style) |
|------------------|----------------------|
| "Welcome to our platform! Let's get you set up with a seamless onboarding experience." | "Welcome to Basecamp. Let's get your first project started." |
| "An error has occurred. Please contact support." | "That didn't work. Here's what happened and how to fix it:" |
| "Upgrade to our premium tier for enhanced functionality." | "Need more storage? Upgrade for $99/month." |
| "Your notification preferences have been updated successfully." | "Saved." |
| "Leverage our robust integration ecosystem." | "Works with the tools you already use." |

## Focus on What Won't Change

Technology trends come and go. User preferences shift. Competitors add and remove features. But some things never change: people want software that is fast, simple, reliable, and respectful of their time. The 37signals bet is to invest disproportionately in these permanent qualities.

**Permanent qualities worth investing in:**

- **Speed.** A faster product is always better. This will never change.
- **Simplicity.** Easier to understand is always better. This will never change.
- **Reliability.** Always working is always better. This will never change.
- **Clarity.** Clear communication is always better. This will never change.
- **Respect for user time.** Fewer steps, fewer clicks, fewer distractions. Always better.

**Transient qualities to be cautious about:**

- Latest JavaScript framework (will be replaced in 3 years)
- AI features (valuable, but the landscape changes monthly)
- Social features (user expectations shift frequently)
- Integration with trending platforms (platforms rise and fall)

This does not mean ignoring new technology. It means building on a stable foundation and adopting new technology selectively, when it clearly serves a permanent quality. Use a new framework if it makes the product faster. Do not use it because it is trendy.

## Out-Teach the Competition

37signals publishes books, blog posts, conference talks, and free resources about how they work. This is not charity — it is strategy. Teaching your methods openly attracts customers who share your values, establishes authority in your space, and creates a relationship with potential customers long before they buy.

**What teaching looks like:**

- **Books.** Getting Real, Rework, Remote, It Doesn't Have to Be Crazy at Work, Shape Up — all share 37signals' methods openly.
- **Blog posts.** Signal v. Noise (now HEY World) publishes opinions about product development, business, and technology regularly.
- **Open source.** Ruby on Rails is the ultimate "sell your by-products" example — a tool built for internal use, released to the world, creating a massive community that feeds back into 37signals' reputation.
- **Transparent practices.** Open salaries, public positions on remote work, published decision frameworks — transparency builds trust.

**Why teaching works as marketing:**

- People buy from people they trust. Teaching builds trust.
- Your best customers are people who already agree with your philosophy. Teaching finds them.
- Teaching is durable. A blog post generates leads for years. An ad generates leads for a day.
- Teaching differentiates. Competitors can copy your features. They cannot copy your thinking.

## Sell Your By-Products

Every business produces by-products — knowledge, processes, tools, and methods created along the way to the main product. Most companies ignore these. 37signals sells them.

**37signals by-products:**

| Main Product | By-Product | Outcome |
|-------------|-----------|---------|
| Basecamp (project management) | Ruby on Rails (web framework) | World's most popular Ruby framework; massive community |
| Building Basecamp | Getting Real, Rework, Shape Up (books) | Millions of copies; established thought leadership |
| Running a remote company | Remote (book) | Influenced the global remote work movement |
| Product development process | Shape Up methodology | Adopted by thousands of companies |
| Building HEY | Blog posts about email philosophy | Generated massive launch buzz |

**How to identify your by-products:**

1. What processes did you create that others might find useful?
2. What tools did you build internally that could stand alone?
3. What lessons did you learn that others in your industry would value?
4. What opinions do you hold that are different from the mainstream?

**How to sell by-products:**

- Open source internal tools (Rails, Turbo, Stimulus, Hotwire)
- Write about your process (blog posts, books, newsletters)
- Speak about your decisions (conferences, podcasts, interviews)
- Share your templates (pitch templates, hiring processes, team structures)

By-products are already paid for — the cost of creating them was absorbed by the main product. Selling them is nearly pure upside.
