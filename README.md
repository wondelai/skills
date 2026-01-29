# Wondel.ai Skills

Agent skills for Claude Code and agentskills.io-compatible agents.

## Installation

Install via [skills.sh](https://skills.sh):

```bash
# Install all skills
npx skills add wondelai/skills

# Or install individual skills
npx skills add wondelai/skills/jobs-to-be-done
npx skills add wondelai/skills/cro-methodology
npx skills add wondelai/skills/refactoring-ui
npx skills add wondelai/skills/ios-hig-design
npx skills add wondelai/skills/scorecard-marketing
```

## Available Skills

| Skill | Description | Based On |
|-------|-------------|----------|
| jobs-to-be-done | JTBD framework for product innovation | [Clayton Christensen](https://x.com/claychristensen)'s [*"Competing Against Luck"*](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612) |
| cro-methodology | Conversion rate optimization methodology | [Karl Blanks](https://www.karlblanks.com/) & [Ben Jesson](https://www.ben-jesson.co.uk/)'s [*"Making Websites Win"*](https://www.amazon.com/Making-Websites-Win-Customer-Centric-Methodology/dp/1544500513) |
| refactoring-ui | Practical UI design system | [Adam Wathan](https://x.com/adamwathan) & [Steve Schoger](https://x.com/steveschoger)'s [*"Refactoring UI"*](https://www.refactoringui.com/) |
| ios-hig-design | Native iOS app design guidelines | [Apple](https://x.com/Apple)'s [*Human Interface Guidelines*](https://developer.apple.com/design/human-interface-guidelines/) |
| scorecard-marketing | Quiz/assessment funnel lead generation | [Daniel Priestley](https://x.com/DanielPriestley)'s [*"Scorecard Marketing"*](https://www.amazon.com/Scorecard-Marketing-four-step-playbook-getting/dp/1781337195) |

---

## Skill Details

### jobs-to-be-done

Strategic framework for discovering and designing product innovations. Customers don't buy products—they "hire" them to make progress in specific circumstances.

**Use when you need to:**
- Understand why customers really buy (or don't buy) your product
- Design a new product or feature from scratch
- Write customer discovery interview questions
- Analyze competition beyond obvious product categories
- Diagnose why a product isn't selling or customers are churning
- Create positioning and messaging strategy
- Reframe product metrics around customer progress

**Example prompts:**
- *"Help me write interview questions to discover the job our customers hire our app for"*
- *"Our signup-to-active rate is 20%. Use JTBD to diagnose why users aren't completing the Little Hire"*
- *"What jobs might compete with our meditation app that aren't other meditation apps?"*
- *"Write a job statement for someone buying a $3000 online course"*

---

### cro-methodology

Scientific, customer-centric approach to conversion rate optimization. Rejects "best practices" in favor of evidence-based testing—understand WHY visitors don't convert before changing anything.

**Use when you need to:**
- Audit a landing page or website for conversion issues
- Identify why visitors aren't converting (objections vs. UX problems)
- Write persuasive copy that addresses customer objections
- Design A/B tests with bold hypotheses (not button color tests)
- Find hidden "persuasion assets" you're not using
- Map and optimize a conversion funnel
- Create an objection/counter-objection framework

**Example prompts:**
- *"Audit this landing page and list the top 5 objections a visitor might have"*
- *"Create an O/CO (objection/counter-objection) table for our SaaS pricing page"*
- *"What persuasion assets are we missing on this page? (testimonials, guarantees, credentials)"*
- *"Rewrite this headline to address the 'is this worth my time?' objection"*

---

### refactoring-ui

Practical, opinionated UI design system for developers. Design in grayscale first, add color last. Start with too much white space, then remove.

**Use when you need to:**
- Make a UI "look less amateur" without a designer
- Fix visual hierarchy problems (everything looks the same importance)
- Choose a consistent spacing and typography scale
- Build a color palette with proper shades and contrast
- Add depth with shadows and layering
- Review UI code for common design mistakes
- Style components in Tailwind CSS

**Example prompts:**
- *"This dashboard looks cluttered. Apply Refactoring UI principles to fix the hierarchy"*
- *"Generate a color palette with 9 shades for a warm, friendly SaaS app"*
- *"Review this card component and suggest spacing/typography improvements"*
- *"The text is hard to read. What's wrong with the contrast and line height?"*
- *"Convert this design to Tailwind classes following Refactoring UI spacing scale"*

---

### ios-hig-design

Design native iOS apps that feel intuitive and aligned with Apple's platform conventions. Covers layout, typography, navigation, gestures, colors, and accessibility.

**Use when you need to:**
- Design iPhone or iPad app interfaces
- Build SwiftUI or UIKit components that feel native
- Validate if a design follows iOS conventions
- Implement proper navigation patterns (tab bar, nav bar, modals)
- Ensure accessibility (VoiceOver, Dynamic Type, contrast)
- Handle safe areas, notch, and Dynamic Island correctly
- Choose correct touch target sizes and spacing

**Example prompts:**
- *"Review this SwiftUI view and check if it follows HIG guidelines"*
- *"What's the correct navigation pattern for a settings screen with sub-pages?"*
- *"Add proper accessibility labels to these interactive elements"*
- *"This design uses a hamburger menu. What's the iOS-native alternative?"*
- *"Generate the correct icon sizes for App Store submission"*

---

### scorecard-marketing

Lead generation system using interactive quiz/assessment funnels. Converts 30-50% vs 3-10% for traditional PDF lead magnets by creating psychological tension and self-qualification.

**Use when you need to:**
- Create a lead magnet that actually converts
- Build a quiz funnel landing page
- Design assessment questions that qualify leads
- Write dynamic results content based on score tiers
- Set up automated follow-up sequences by segment
- Generate scorecard concepts for any industry

**Example prompts:**
- *"Create a scorecard concept for a B2B accounting software company"*
- *"Write 15 assessment questions for a 'Marketing Maturity' scorecard with 5 categories"*
- *"Generate landing page copy for a 'Are You Ready to Scale?' quiz using the 3 Cs formula"*
- *"Write dynamic results page content for Low/Medium/High scoring tiers"*
- *"What follow-up email sequence should we send based on scorecard results?"*
