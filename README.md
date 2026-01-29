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
| jobs-to-be-done | JTBD framework for product innovation | [Clayton Christensen](https://x.com/claychristensen)'s [*"Competing Against Luck"*](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612?tag=wondelai00-20) |
| cro-methodology | Conversion rate optimization methodology | [Karl Blanks](https://www.karlblanks.com/) & [Ben Jesson](https://www.ben-jesson.co.uk/)'s [*"Making Websites Win"*](https://www.amazon.com/Making-Websites-Win-Customer-Centric-Methodology/dp/1544500513?tag=wondelai00-20) |
| refactoring-ui | Practical UI design system | [Adam Wathan](https://x.com/adamwathan) & [Steve Schoger](https://x.com/steveschoger)'s [*"Refactoring UI"*](https://www.refactoringui.com/) |
| ios-hig-design | Native iOS app design guidelines | [Apple](https://x.com/Apple)'s [*Human Interface Guidelines*](https://developer.apple.com/design/human-interface-guidelines/) |
| scorecard-marketing | Quiz/assessment funnel lead generation | [Daniel Priestley](https://x.com/DanielPriestley)'s [*"Scorecard Marketing"*](https://www.amazon.com/Scorecard-Marketing-four-step-playbook-getting/dp/1781337195?tag=wondelai00-20) |

---

## Skill Details

### jobs-to-be-done

Strategic framework for discovering and designing product innovations. Customers don't buy products—they "hire" them to make progress in specific circumstances.

**About the author:** [Clayton M. Christensen](https://x.com/claychristensen) (1952–2020) was a Harvard Business School professor widely regarded as one of the most influential business thinkers of our time. Named the world's most influential business thinker by Thinkers50 in 2011 and 2013, he developed the theory of "disruptive innovation" and authored nine books including *The Innovator's Dilemma*. Christensen co-founded Innosight (growth strategy consultancy), Rose Park Advisors (investment firm), and the Christensen Institute (non-profit think tank). His JTBD framework, detailed in [*"Competing Against Luck"*](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612?tag=wondelai00-20), has been adopted by companies like Netflix, Intuit, and countless startups worldwide.

**Use when you need to:**
- Understand why customers really buy (or don't buy) your product
- Design a new product or feature from scratch
- Write customer discovery interview questions
- Analyze competition beyond obvious product categories
- Diagnose why a product isn't selling or customers are churning
- Create positioning and messaging strategy
- Reframe product metrics around customer progress

**Example prompts:**
- *"Help me write interview questions to discover the job our customers hire our app for. Use jobs-to-be-done skill."*
- *"Our signup-to-active rate is 20%. Diagnose why users aren't completing the Little Hire. Use jobs-to-be-done skill."*
- *"What jobs might compete with our meditation app that aren't other meditation apps? Use jobs-to-be-done skill."*
- *"Write a job statement for someone buying a $3000 online course. Use jobs-to-be-done skill."*

---

### cro-methodology

Scientific, customer-centric approach to conversion rate optimization. Rejects "best practices" in favor of evidence-based testing—understand WHY visitors don't convert before changing anything.

**About the authors:** [Dr. Karl Blanks](https://www.karlblanks.com/) and [Ben Jesson](https://www.ben-jesson.co.uk/) are co-founders of Conversion Rate Experts (CRE), the world's leading conversion rate optimization agency. They received the Queen's Award for Enterprise twice—first for Innovation (codifying the scientific methodology now used by companies like Amazon and Google), and again for International Trade. Their client list includes Google, Apple, Facebook, Amazon, Dropbox, and many other leading tech companies. Their methodology has generated billions in additional revenue. [*"Making Websites Win"*](https://www.amazon.com/Making-Websites-Win-Customer-Centric-Methodology/dp/1544500513?tag=wondelai00-20) became an Amazon #1 bestseller in 15 categories. All profits from the book are donated to the charity Mary's Meals.

**Use when you need to:**
- Audit a landing page or website for conversion issues
- Identify why visitors aren't converting (objections vs. UX problems)
- Write persuasive copy that addresses customer objections
- Design A/B tests with bold hypotheses (not button color tests)
- Find hidden "persuasion assets" you're not using
- Map and optimize a conversion funnel
- Create an objection/counter-objection framework

**Example prompts:**
- *"Audit this landing page and list the top 5 objections a visitor might have. Use cro-methodology skill."*
- *"Create an O/CO (objection/counter-objection) table for our SaaS pricing page. Use cro-methodology skill."*
- *"What persuasion assets are we missing on this page? (testimonials, guarantees, credentials). Use cro-methodology skill."*
- *"Rewrite this headline to address the 'is this worth my time?' objection. Use cro-methodology skill."*

---

### refactoring-ui

Practical, opinionated UI design system for developers. Design in grayscale first, add color last. Start with too much white space, then remove.

**About the authors:** [Adam Wathan](https://x.com/adamwathan) is a full-stack developer and entrepreneur best known as the creator of Tailwind CSS, the utility-first CSS framework that has become one of the most popular styling tools in modern web development. [Steve Schoger](https://x.com/steveschoger) is a visual designer from Canada known for his practical design tips that went viral on Twitter, helping developers improve their UI skills. Together, they created [*"Refactoring UI"*](https://www.refactoringui.com/)—a book and video series teaching developers how to design beautiful interfaces without formal design training. Their collaboration bridges the gap between development and design, making good UI accessible to everyone who writes code.

**Use when you need to:**
- Make a UI "look less amateur" without a designer
- Fix visual hierarchy problems (everything looks the same importance)
- Choose a consistent spacing and typography scale
- Build a color palette with proper shades and contrast
- Add depth with shadows and layering
- Review UI code for common design mistakes
- Style components in Tailwind CSS

**Example prompts:**
- *"This dashboard looks cluttered. Fix the hierarchy. Use refactoring-ui skill."*
- *"Generate a color palette with 9 shades for a warm, friendly SaaS app. Use refactoring-ui skill."*
- *"Review this card component and suggest spacing/typography improvements. Use refactoring-ui skill."*
- *"The text is hard to read. What's wrong with the contrast and line height? Use refactoring-ui skill."*
- *"Convert this design to Tailwind classes. Use refactoring-ui skill."*

---

### ios-hig-design

Design native iOS apps that feel intuitive and aligned with Apple's platform conventions. Covers layout, typography, navigation, gestures, colors, and accessibility.

**About the source:** [Apple Inc.](https://x.com/Apple) has published Human Interface Guidelines since the original Macintosh in 1984, making it one of the oldest and most influential design documentation in computing history. The [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) define the design language for iOS, macOS, watchOS, tvOS, and visionOS—covering everything from typography and color to navigation patterns and accessibility. Apple's design philosophy emphasizes clarity, deference, and depth, creating interfaces that feel intuitive to billions of users worldwide. The HIG is continuously updated and represents decades of research into human-computer interaction.

**Use when you need to:**
- Design iPhone or iPad app interfaces
- Build SwiftUI or UIKit components that feel native
- Validate if a design follows iOS conventions
- Implement proper navigation patterns (tab bar, nav bar, modals)
- Ensure accessibility (VoiceOver, Dynamic Type, contrast)
- Handle safe areas, notch, and Dynamic Island correctly
- Choose correct touch target sizes and spacing

**Example prompts:**
- *"Review this SwiftUI view and check if it follows HIG guidelines. Use ios-hig-design skill."*
- *"What's the correct navigation pattern for a settings screen with sub-pages? Use ios-hig-design skill."*
- *"Add proper accessibility labels to these interactive elements. Use ios-hig-design skill."*
- *"This design uses a hamburger menu. What's the iOS-native alternative? Use ios-hig-design skill."*
- *"Generate the correct icon sizes for App Store submission. Use ios-hig-design skill."*

---

### scorecard-marketing

Lead generation system using interactive quiz/assessment funnels. Converts 30-50% vs 3-10% for traditional PDF lead magnets by creating psychological tension and self-qualification.

**About the author:** [Daniel Priestley](https://x.com/DanielPriestley) is a serial entrepreneur who has built and sold multiple businesses. He founded Dent Global, one of the world's leading business accelerators for entrepreneurs, and co-founded ScoreApp, a marketing software platform serving over 150,000 businesses globally. Priestley has won major business awards and authored seven books on entrepreneurship, including bestsellers *Key Person of Influence*, *Entrepreneur Revolution*, *Oversubscribed*, and *24 Assets*. [*"Scorecard Marketing"*](https://www.amazon.com/Scorecard-Marketing-four-step-playbook-getting/dp/1781337195?tag=wondelai00-20), co-authored with Glen Carlson, distills the methodology that powers ScoreApp into a practical playbook for generating qualified leads at scale.

**Use when you need to:**
- Create a lead magnet that actually converts
- Build a quiz funnel landing page
- Design assessment questions that qualify leads
- Write dynamic results content based on score tiers
- Set up automated follow-up sequences by segment
- Generate scorecard concepts for any industry

**Example prompts:**
- *"Create a scorecard concept for a B2B accounting software company. Use scorecard-marketing skill."*
- *"Write 15 assessment questions for a 'Marketing Maturity' scorecard with 5 categories. Use scorecard-marketing skill."*
- *"Generate landing page copy for a 'Are You Ready to Scale?' quiz using the 3 Cs formula. Use scorecard-marketing skill."*
- *"Write dynamic results page content for Low/Medium/High scoring tiers. Use scorecard-marketing skill."*
- *"What follow-up email sequence should we send based on scorecard results? Use scorecard-marketing skill."*

---

## Copyright & Disclaimer

The methodologies and frameworks referenced in these skills are the intellectual property of their respective authors and publishers. All copyrights belong to:

- **Jobs to Be Done**: Clayton M. Christensen, Taddy Hall, Karen Dillon, David S. Duncan
- **Making Websites Win**: Karl Blanks, Ben Jesson (Conversion Rate Experts)
- **Refactoring UI**: Adam Wathan, Steve Schoger
- **Human Interface Guidelines**: Apple Inc.
- **Scorecard Marketing**: Daniel Priestley, Glen Carlson

These skills were created without directly copying or reproducing content from the original books or materials. They are based on:
- Publicly available information about the methodologies
- General knowledge embedded in large language models
- Common industry practices and terminology

We encourage users to purchase and read the original books for the complete, authoritative treatment of each methodology. The skills in this repository are intended as practical aids, not replacements for the source materials.
