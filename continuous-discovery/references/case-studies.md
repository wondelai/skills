# Case Studies: Continuous Discovery in Practice

Four realistic scenarios showing how product teams apply continuous discovery habits across different contexts. Each case study follows a team from establishing the practice through making evidence-based decisions.

## Table of Contents
1. [Case Study 1: B2B SaaS -- Project Management Tool](#case-study-1-b2b-saas-project-management-tool)
2. [Case Study 2: Consumer Mobile -- Fitness App](#case-study-2-consumer-mobile-fitness-app)
3. [Case Study 3: Platform Team -- Internal Developer Platform](#case-study-3-platform-team-internal-developer-platform)
4. [Case Study 4: Growth Team -- E-Commerce Marketplace](#case-study-4-growth-team-e-commerce-marketplace)
5. [Patterns Across Case Studies](#patterns-across-case-studies)

---

## Case Study 1: B2B SaaS -- Project Management Tool

### Context

**Company:** Mid-stage B2B SaaS company (200 employees) building a project management tool for marketing teams. 15,000 paying customers, $20M ARR.

**Team:** Product trio -- Priya (PM), Jake (designer), and Lena (engineer). They've been a team for 4 months.

**Assigned outcome:** Increase 90-day retention for new accounts from 62% to 75%.

### Establishing the Practice

**Week 1-2: Setting up the cadence**

Priya's first step was automating interview recruitment. The team added an in-app banner for users in their first 30 days: "Help us make [Product] better for your team. Chat for 25 minutes and get a $25 gift card." This fed into a Calendly link with two weekly slots -- Tuesday at 2pm and Thursday at 10am.

The team created a shared Miro board for their Opportunity Solution Tree, with the outcome ("Increase 90-day retention from 62% to 75%") at the top and empty space below for opportunities.

**Week 3-4: First interviews and experience mapping**

In the first two weeks, the trio conducted 4 interviews with users who were 2-3 weeks into their accounts. They asked each user: "Tell me about the last time you tried to set up a project in [Product]. Start from the very beginning."

The stories revealed a consistent pattern: users understood how to create projects, but they struggled to get their team members to adopt the tool. One user said: "I spent an hour setting it up perfectly, then sent the link to my team, and nobody logged in. I felt like an idiot."

The team built an experience map of "Getting your team onto a new project tool" and identified five distinct steps, with the biggest pain point at "getting team members to log in and start using it."

### The Opportunity Solution Tree Takes Shape

After 6 interviews, the team's OST looked like this:

```
Outcome: Increase 90-day retention from 62% to 75%
│
├── "Account creator can't get team members to adopt the tool"
│   ├── "Team members don't understand why they should switch"
│   ├── "First login experience is confusing for invited members"
│   └── "No accountability -- nobody knows if team is using it"
│
├── "Users can't figure out which features are relevant to their workflow"
│   └── "Marketing teams have different workflows than the default templates"
│
└── "Users lose momentum after initial setup"
    ├── "No reason to come back daily"
    └── "Progress isn't visible to the person who advocated for the tool"
```

### Assumption Testing

The team decided to focus on "Account creator can't get team members to adopt the tool" because 5 of 6 interviews mentioned this struggle. They brainstormed three solutions:

1. **Onboarding buddy system:** Pair the account creator with a CS rep for the first 2 weeks
2. **Team adoption dashboard:** Show the creator which team members have logged in, completed tasks, etc.
3. **Magic invite link:** Pre-populate the invited member's view with their first assigned task so they immediately see why they need to log in

For the "magic invite link" solution, the riskiest assumption was: "Team members will engage if they see an assigned task rather than an empty dashboard." They designed a painted-door test: existing invite emails were A/B tested. Version A was the current generic invite. Version B said "You have a task waiting for you in [Product]" (the task was the standard onboarding tutorial, reframed).

**Result:** Version B had 34% higher click-through and 22% higher day-1 activation. The assumption was validated.

### Outcome

Over 8 weeks, the team shipped an improved invite flow based on validated assumptions. After one quarter of continuous discovery, 90-day retention moved from 62% to 71%. Not yet at the 75% target, but the team had clear evidence pointing to the next opportunities to pursue.

---

## Case Study 2: Consumer Mobile -- Fitness App

### Context

**Company:** Early-stage startup (20 employees) with a mobile fitness app targeting busy professionals who want to exercise but struggle to maintain a routine. 50,000 MAU, freemium model.

**Team:** Product trio -- Marcus (PM), Ava (designer), and Chen (engineer). This is their first time practicing continuous discovery.

**Assigned outcome:** Increase 7-day retention (users active on day 1 and day 7) from 25% to 40%.

### Getting Started with Limited Resources

Marcus had no budget for a research platform, so they started scrappy. Ava added a single screen after the user's third workout: "We're building this app for people like you. Got 20 minutes for a quick call? We'll give you a free month of premium." This generated 3-4 willing participants per week.

The trio blocked Thursday at 3pm as their standing interview slot. They created a simple Google Doc template for their interview snapshots.

### Key Discovery: The Motivation Gap

The first 5 interviews revealed something the team hadn't expected. Users weren't leaving because the workouts were bad -- they left because they couldn't figure out which workout to do on any given day.

One user described it: "I open the app on Monday feeling motivated. I see 200 workouts. I spend 5 minutes scrolling, can't decide, and close the app. By Wednesday my motivation is gone."

Another user: "The app has great content, but it feels like a library, not a coach. I don't need more options -- I need someone to tell me 'do this today.'"

The team mapped the experience of "deciding what workout to do today" and found that the decision point was where most users dropped off. The experience map showed:

1. Open app with intention to work out
2. Browse workout library (feeling: overwhelmed)
3. Try to filter or search (feeling: frustrated -- too many options)
4. Either pick something random or give up (feeling: defeated or unsatisfied)
5. If they picked something, do the workout (feeling: good during, but uncertain if it was the "right" choice)

### Opportunity Solution Tree

```
Outcome: Increase 7-day retention from 25% to 40%
│
├── "I can't decide which workout to do today" ← FOCUS
│   ├── "I don't know what's appropriate for my fitness level"
│   ├── "I don't have a plan -- every day feels like starting over"
│   └── "There are too many options and I'm overwhelmed"
│
├── "I lose motivation when I don't see progress"
│   └── "I can't tell if I'm getting stronger or fitter"
│
└── "Life gets in the way and I fall off the routine"
    └── "Once I miss a day, I feel guilty and avoid the app"
```

### Testing Assumptions

The team focused on "I don't have a plan -- every day feels like starting over" because it appeared in 4 of 5 interviews and was connected to the strongest emotional language.

**Solution idea:** A simple daily plan that tells users exactly which workout to do today based on their stated goals, available time, and equipment.

**Riskiest assumption:** "Users will follow a prescribed daily plan instead of browsing on their own."

**Test:** They created a Wizard of Oz test. For 20 users who opted in, Ava manually selected a daily workout based on their profile and sent a push notification each morning: "Today's workout: [name] (25 min, upper body). Tap to start." Marcus tracked how many tapped the notification and completed the workout.

**Result:** 14 of 20 users (70%) completed the recommended workout on day 1. By day 7, 11 of 20 (55%) were still following the daily plan. Compared to the 25% baseline retention, this was a dramatic improvement.

### Outcome

The team built a lightweight recommendation engine based on what they learned from the Wizard of Oz test. Day-7 retention climbed to 38% within 6 weeks. The continuous interview cadence continued to reveal refinements -- users wanted to swap workouts without losing their plan, and they wanted a "rest day" option that didn't feel like failure.

---

## Case Study 3: Platform Team -- Internal Developer Platform

### Context

**Company:** Large enterprise (5,000 employees) with an internal platform team that builds tools for the company's 300 software engineers.

**Team:** Product trio -- Sam (PM), Robin (designer), and Alex (engineer). Their "customers" are internal developers.

**Assigned outcome:** Reduce average deployment time from 45 minutes to under 15 minutes.

### Adapting Discovery for Internal Customers

Sam's advantage was direct access to customers -- they sat in the same Slack channels. The challenge was that internal developers had strong opinions about solutions ("just give us better CI/CD pipelines") but rarely articulated the underlying needs.

The team set up a weekly "Deploy Stories" interview. Every Thursday, they invited one developer to walk through their most recent deployment step by step. The framing was crucial: "We're not asking what tools you want -- we want to understand your actual experience of deploying code last week."

### Surprising Findings

The team assumed the slow deployment was a CI/CD pipeline problem. The experience map told a different story:

1. **Write code and get it reviewed** (15 min, well-understood)
2. **Merge to main** (2 min, no pain)
3. **Wait for CI to run** (8 min -- the part the team expected to be the bottleneck)
4. **Manually check 3 dashboards to verify the deploy is healthy** (12 min -- unexpected)
5. **Write a deploy summary in Slack for the on-call engineer** (5 min -- unknown to the platform team)
6. **Wait for the on-call engineer to acknowledge** (variable: 3-20 min -- the actual bottleneck)

Steps 4, 5, and 6 accounted for more time than CI (step 3) and were entirely manual. The platform team had been investing in CI speed while the real time sinks were elsewhere.

### The OST Reframed

```
Outcome: Reduce deployment time from 45 min to under 15 min
│
├── "I have to manually check multiple dashboards to verify deploy health"
│   ├── "I don't trust that the deploy is healthy without checking myself"
│   └── "Each dashboard shows different metrics and I'm not sure what to look for"
│
├── "I have to write a manual deploy summary and wait for acknowledgment"
│   ├── "The summary format isn't standardized so I spend time figuring out what to include"
│   └── "The on-call person doesn't always see my message quickly"
│
└── "CI takes 8 minutes and I context-switch during the wait"
    └── "By the time CI finishes, I've started something else and don't come back for 10+ min"
```

### Evidence-Driven Solutions

Instead of optimizing CI (which would have saved 2-3 minutes at best), the team focused on the deploy verification and handoff steps. They tested a simple assumption: "Developers will trust an automated health check if it shows the same metrics they currently check manually."

They built a prototype that aggregated the three dashboards into a single deploy health summary posted automatically in Slack. Seven developers tested it for one week. Six of seven said they no longer needed to check the dashboards separately. The seventh wanted one additional metric included.

### Outcome

By automating health verification and deploy summaries, the team reduced average deployment time from 45 minutes to 18 minutes -- without touching the CI pipeline at all. Continuous interviews continued to reveal further optimizations, and the team estimated they could reach the 15-minute target within another quarter.

---

## Case Study 4: Growth Team -- E-Commerce Marketplace

### Context

**Company:** Series B e-commerce marketplace connecting independent artisans with buyers. 200,000 registered buyers, 8,000 sellers.

**Team:** Product trio -- Dana (PM), Leo (designer), and Nia (engineer). They sit on the growth team focused on buyer-side metrics.

**Assigned outcome:** Increase first-purchase conversion from 12% to 20% (percentage of registered users who make a purchase within 30 days).

### Two-Sided Discovery

The team's challenge was that their outcome depended on both sides of the marketplace. They needed to understand why buyers registered but didn't purchase. They split their interview cadence:

- **Tuesdays:** Interview a registered buyer who hadn't purchased yet (recruited via email: "We noticed you signed up but haven't found anything yet -- can we learn why?")
- **Thursdays:** Interview a buyer who did make their first purchase within 30 days (recruited via post-purchase email)

This contrast was powerful. By interviewing both converters and non-converters, the team could identify what was different about their experiences.

### The Discovery

Non-converter interviews revealed three dominant patterns:

**Pattern 1 (mentioned in 7 of 10 non-converter interviews):** "I browsed for a while but couldn't tell if the products were actually good quality. The photos looked nice but I wasn't sure about sizing, materials, or durability."

**Pattern 2 (mentioned in 5 of 10):** "I found something I liked but the shipping cost surprised me at checkout. I thought 'I'll come back later' and never did."

**Pattern 3 (mentioned in 4 of 10):** "I signed up because someone shared a link to a specific product, but when I looked at the rest of the site, nothing else caught my eye."

Converter interviews showed a contrasting pattern: buyers who purchased often mentioned reading reviews, seeing detailed product descriptions, or having a friend recommend a specific seller.

### Opportunity Solution Tree

```
Outcome: Increase first-purchase conversion from 12% to 20%
│
├── "I can't assess product quality from the listing" ← PRIMARY FOCUS
│   ├── "Photos don't show scale, materials, or details"
│   ├── "I don't trust reviews -- are they real?"
│   └── "I can't find information about the seller's craftsmanship"
│
├── "Shipping costs surprise me and kill my motivation to buy"
│   ├── "I don't see shipping costs until checkout"
│   └── "Shipping feels too expensive relative to the product"
│
└── "After seeing the product I came for, I don't discover anything else"
    └── "The 'recommended for you' section isn't relevant to my interests"
```

### Assumption Testing

For the primary focus opportunity, the team generated three solutions:

1. **Enhanced listing requirements:** Require sellers to include size reference photos and material close-ups
2. **Verified review badges:** Show which reviews come from verified purchases
3. **Seller story cards:** Short profiles showing the artisan's workshop and process

The riskiest assumption for seller story cards was: "Seeing the artisan's story will increase buyer confidence in product quality." They tested this with a simple experiment: for 500 product views, they added a one-line artisan bio with a workshop photo at the top of the listing. For another 500 views (control), the listing was unchanged.

**Result:** Listings with artisan context had 18% higher add-to-cart rates and 11% higher checkout completion. Buyers spent an average of 8 seconds longer on the listing -- suggesting they were reading the context and it influenced their decision.

For the shipping cost opportunity, they tested upfront shipping display. The assumption: "Showing shipping costs on the product listing page (instead of at checkout) will reduce cart abandonment without significantly reducing add-to-cart rates." They ran an A/B test on 2,000 product views.

**Result:** Showing shipping costs upfront reduced add-to-cart by 5% but increased checkout completion by 23%. Net effect: more completed purchases. The transparency removed the unpleasant surprise.

### Outcome

Over 10 weeks, the team shipped artisan context cards, verified review badges, and upfront shipping display. First-purchase conversion moved from 12% to 17.5%. The continuous interview cadence revealed that the next biggest opportunity was in the post-first-purchase experience -- buyers who had a good first experience but didn't come back for a second purchase.

---

## Patterns Across Case Studies

### 1. The Real Problem Is Rarely Where You Expect It

- The B2B team thought retention was a feature problem; it was a team adoption problem
- The fitness team thought content quality was the issue; it was decision fatigue
- The platform team thought CI speed was the bottleneck; it was manual verification
- The growth team thought conversion was about product appeal; it was about trust signals

**Lesson:** Continuous discovery's greatest value is correcting the team's initial assumptions about where the problem lies.

### 2. Interviews Reveal What Data Cannot

Analytics showed the platform team that deployments took 45 minutes. Only interviews revealed that 25 of those minutes were spent on manual steps invisible to the deployment pipeline.

**Lesson:** Quantitative data tells you what is happening. Qualitative interviews tell you why.

### 3. Small Tests Prevent Big Mistakes

Every team ran cheap tests before committing to building. The fitness team's Wizard of Oz test cost zero engineering effort. The marketplace team's artisan story card test was a simple content addition.

**Lesson:** The cheapest test that generates evidence is always the right first step.

### 4. The Cadence Compounds

In each case study, the team's understanding deepened over weeks. Early interviews revealed surface-level problems. Later interviews, informed by earlier learning, probed deeper and uncovered root causes.

**Lesson:** Individual interviews are informative. A sustained cadence of interviews is transformative.

### 5. The Trio Makes Better Decisions Together

When PM, designer, and engineer all hear the same customer stories, alignment happens naturally. There's no need for lengthy requirements documents or persuasion -- everyone saw the user struggle with the same pain point.

**Lesson:** Shared evidence creates shared conviction. The product trio interviewing together is not a luxury; it's a prerequisite for good decisions.
