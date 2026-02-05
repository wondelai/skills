# Wondel.ai Skills

Agent skills for Claude Code and agentskills.io-compatible agents.

## Installation

### Via Claude Code Plugin Marketplace

```bash
# Add the marketplace
/plugin marketplace add wondelai/skills

# Install plugin collections
/plugin install product-strategy@wondelai-skills    # Jobs to Be Done
/plugin install ux-design@wondelai-skills           # Refactoring UI, iOS HIG, UX Heuristics, Hooked, Web Typography, Top Design
/plugin install marketing-cro@wondelai-skills       # CRO Methodology, StoryBrand, Scorecard Marketing
```

### Via skills.sh

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
npx skills add wondelai/skills/storybrand-messaging
npx skills add wondelai/skills/hooked-ux
npx skills add wondelai/skills/ux-heuristics
npx skills add wondelai/skills/web-typography
npx skills add wondelai/skills/top-design
npx skills add wondelai/skills/negotiation
```

## Available Skills

| Skill | Description | Based On |
|-------|-------------|----------|
| jobs-to-be-done | JTBD framework for product innovation | [Clayton Christensen](https://x.com/claychristensen)'s [*"Competing Against Luck"*](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612?tag=wondelai00-20) |
| cro-methodology | Conversion rate optimization methodology | [Karl Blanks](https://www.karlblanks.com/) & [Ben Jesson](https://www.ben-jesson.co.uk/)'s [*"Making Websites Win"*](https://www.amazon.com/Making-Websites-Win-Customer-Centric-Methodology/dp/1544500513?tag=wondelai00-20) |
| refactoring-ui | Practical UI design system | [Adam Wathan](https://x.com/adamwathan) & [Steve Schoger](https://x.com/steveschoger)'s [*"Refactoring UI"*](https://www.refactoringui.com/) |
| ios-hig-design | Native iOS app design guidelines | [Apple](https://x.com/Apple)'s [*Human Interface Guidelines*](https://developer.apple.com/design/human-interface-guidelines/) |
| scorecard-marketing | Quiz/assessment funnel lead generation | [Daniel Priestley](https://x.com/DanielPriestley)'s [*"Scorecard Marketing"*](https://www.amazon.com/Scorecard-Marketing-four-step-playbook-getting/dp/1781337195?tag=wondelai00-20) |
| storybrand-messaging | Clear brand messaging using story structure | [Donald Miller](https://x.com/donlonemiller)'s [*"Building a StoryBrand"*](https://www.amazon.com/Building-StoryBrand-Clarify-Message-Customers/dp/0718033329?tag=wondelai00-20) |
| hooked-ux | Habit-forming product design | [Nir Eyal](https://x.com/naboreeyal)'s [*"Hooked"*](https://www.amazon.com/Hooked-How-Build-Habit-Forming-Products/dp/1591847788?tag=wondelai00-20) |
| ux-heuristics | Usability evaluation and principles | [Steve Krug](https://x.com/skrug)'s [*"Don't Make Me Think"*](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515?tag=wondelai00-20) & [Jakob Nielsen](https://x.com/nngroup)'s [10 Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) |
| web-typography | Web typography principles and implementation | [Jason Santa Maria](https://x.com/jasonsantamaria)'s [*"On Web Typography"*](https://www.amazon.com/Web-Typography-Jason-Santa-Maria/dp/1937557065?tag=wondelai00-20) |
| top-design | Award-winning 10/10 web design matching elite agencies | Techniques from Locomotive, Studio Freight, AREA 17, Awwwards winners |
| negotiation | Tactical negotiation framework for high-stakes conversations | [Chris Voss](https://x.com/VossNegotiation)'s [*"Never Split the Difference"*](https://www.amazon.com/Never-Split-Difference-Negotiating-Depended/dp/0062407805?tag=wondelai00-20) |

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

### storybrand-messaging

StoryBrand framework for clarifying your message so customers will listen. Positions your customer as the hero and your brand as the guide in a story structure that resonates.

**About the author:** [Donald Miller](https://x.com/donlonemiller) is the CEO of StoryBrand, a company that has helped more than 10,000 businesses clarify their messaging. His StoryBrand Framework is used by brands ranging from small startups to Fortune 500 companies. Miller is a New York Times bestselling author and popular keynote speaker. [*"Building a StoryBrand"*](https://www.amazon.com/Building-StoryBrand-Clarify-Message-Customers/dp/0718033329?tag=wondelai00-20) has become one of the most influential marketing books of the past decade, teaching the 7-part framework that transforms confusing messaging into clear, compelling communication.

**Use when you need to:**
- Clarify your brand message so customers understand it instantly
- Write website copy that converts visitors to customers
- Create one-liners and elevator pitches
- Build landing pages with narrative structure
- Position your customer as the hero (not your brand)
- Diagnose why your current messaging isn't resonating
- Develop a brand script for consistent communication

**Example prompts:**
- *"Create a StoryBrand brand script for my SaaS project management tool. Use storybrand-messaging skill."*
- *"Write a one-liner for our accounting firm. Use storybrand-messaging skill."*
- *"Audit this homepage copy—is the customer positioned as the hero? Use storybrand-messaging skill."*
- *"What's the internal problem our customers face beyond the external one? Use storybrand-messaging skill."*
- *"Generate a 3-step plan section for our services page. Use storybrand-messaging skill."*

---

### hooked-ux

Hook Model framework for building habit-forming products. The four-phase process (Trigger → Action → Variable Reward → Investment) that connects users to your product through successive cycles.

**About the author:** [Nir Eyal](https://x.com/naboreeyal) is an author, lecturer, and investor who writes about the intersection of psychology, technology, and business. He previously taught at Stanford Graduate School of Business and has worked in the video gaming and advertising industries. [*"Hooked: How to Build Habit-Forming Products"*](https://www.amazon.com/Hooked-How-Build-Habit-Forming-Products/dp/1591847788?tag=wondelai00-20) has become essential reading for product designers and entrepreneurs, providing a practical framework for creating products that users return to repeatedly. His work has influenced product design at companies from startups to Fortune 500.

**Use when you need to:**
- Increase user engagement and retention
- Design habit loops in your product
- Audit why users aren't returning
- Create effective triggers and notifications
- Design variable reward systems
- Increase investment and switching costs
- Evaluate the ethics of your engagement tactics
- Optimize onboarding for habit formation

**Example prompts:**
- *"What's the internal trigger for our meditation app? Use hooked-ux skill."*
- *"Design a variable reward system for our fitness tracking app. Use hooked-ux skill."*
- *"Audit our onboarding—does it complete the full Hook cycle? Use hooked-ux skill."*
- *"How can we increase investment in our note-taking app to improve retention? Use hooked-ux skill."*
- *"Are we in the Habit Zone? Analyze our usage frequency vs. perceived value. Use hooked-ux skill."*

---

### ux-heuristics

Usability heuristics and evaluation principles combining Steve Krug's practical "Don't Make Me Think" approach with Jakob Nielsen's 10 heuristics for systematic interface evaluation.

**About the sources:** [Steve Krug](https://x.com/skrug) is a usability consultant whose book [*"Don't Make Me Think"*](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515?tag=wondelai00-20) has been the go-to guide for web usability since 2000, selling over 600,000 copies. His common-sense approach has influenced a generation of designers. [Jakob Nielsen](https://x.com/nngroup), co-founder of Nielsen Norman Group, is often called "the king of usability." His [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), published in 1994, remain the most-used framework for evaluating interface usability worldwide.

**Use when you need to:**
- Audit a UI for usability problems
- Identify why users are confused or frustrated
- Simplify navigation and information architecture
- Conduct heuristic evaluations
- Prioritize UX fixes by severity
- Review designs before development
- Improve form usability
- Validate that interfaces follow established UX principles

**Example prompts:**
- *"Run a heuristic evaluation on this checkout flow. Use ux-heuristics skill."*
- *"Apply the Trunk Test to this homepage—can users answer the 6 key questions? Use ux-heuristics skill."*
- *"Rate the severity of these usability issues from 0-4. Use ux-heuristics skill."*
- *"What UX heuristics is this error message violating? Use ux-heuristics skill."*
- *"Audit this form for usability issues and suggest fixes. Use ux-heuristics skill."*

---

### web-typography

Web typography principles for choosing, pairing, and implementing typefaces. Typography serves communication—the best typography is invisible, immersing readers in content rather than calling attention to itself.

**About the author:** [Jason Santa Maria](https://x.com/jasonsantamaria) is a graphic designer, author, and educator whose work focuses on the intersection of design and technology. He has worked with clients including The New York Times, AIGA, and Happy Cog. Santa Maria was Creative Director at Typekit (now Adobe Fonts) and co-founded A Book Apart, the influential publisher of books for web professionals. He teaches at the School of Visual Arts in New York. [*"On Web Typography"*](https://www.amazon.com/Web-Typography-Jason-Santa-Maria/dp/1937557065?tag=wondelai00-20), published by A Book Apart in 2014, distills his expertise into a practical guide for choosing, evaluating, and implementing type on the web.

**Use when you need to:**
- Select typefaces for body text, headlines, and UI
- Evaluate typeface quality for screen readability
- Pair fonts that work together (or decide to use just one)
- Set optimal line length, line height, and font size
- Implement responsive typography with CSS
- Build type hierarchies that guide readers
- Optimize web font loading for performance

**Example prompts:**
- *"Recommend a typeface pairing for a legal services website. Use web-typography skill."*
- *"Evaluate if this Google Font is suitable for long-form reading. Use web-typography skill."*
- *"Set up a fluid type scale using clamp() for responsive typography. Use web-typography skill."*
- *"What's wrong with the typography on this blog post? The text feels hard to read. Use web-typography skill."*
- *"Create CSS for optimal body text: font-size, line-height, and max-width. Use web-typography skill."*

---

### top-design

Create award-winning websites and applications with design and typography rated 10/10. Build premium digital experiences that match the quality of elite agencies like Locomotive, Studio Freight, AREA 17, Active Theory, Hello Monday, and Awwwards winners.

**About the source:** This skill synthesizes techniques from the world's top digital agencies—studios that consistently win FWA, Awwwards, CSS Design Awards, and Webby Awards. Every pixel is intentional, typography is architecture, motion creates emotion, and performance is non-negotiable.

**Use when you need to:**
- Build premium portfolio sites, brand websites, or agency-level experiences
- Create immersive web experiences with custom animations
- Implement exceptional typography with dramatic scale contrast
- Design scroll-based compositions with purposeful motion
- Match the quality of Awwwards-winning sites

**Example prompts:**
- *"Build a portfolio site at the level of Studio Freight or Locomotive. Use top-design skill."*
- *"Create an immersive hero section with award-winning typography. Use top-design skill."*
- *"Design a scroll-based experience for a luxury brand. Use top-design skill."*
- *"Review this website against top agency standards. Use top-design skill."*
- *"Add custom animations that feel like an Awwwards winner. Use top-design skill."*

---

### negotiation

Tactical empathy-based negotiation framework from FBI hostage negotiator Chris Voss. Master techniques like mirroring, labeling, calibrated questions, and the Ackerman bargaining method to navigate high-stakes conversations.

**About the author:** [Chris Voss](https://x.com/VossNegotiation) is a former FBI hostage negotiator who served as the lead international kidnapping negotiator for the FBI. During his 24-year career, he was trained in the art of negotiation by the FBI, Scotland Yard, and Harvard Law School. Voss has taught negotiation at Harvard, Georgetown, MIT, and USC. He founded The Black Swan Group, a consulting firm that trains Fortune 500 companies, including Microsoft, Google, and Cisco. [*"Never Split the Difference: Negotiating As If Your Life Depended On It"*](https://www.amazon.com/Never-Split-Difference-Negotiating-Depended/dp/0062407805?tag=wondelai00-20), co-authored with Tahl Raz, became a Wall Street Journal bestseller and has transformed how people negotiate in business, salary discussions, and everyday life.

**Use when you need to:**
- Prepare for salary or contract negotiations
- Handle difficult conversations with stakeholders
- Craft responses to unreasonable demands
- Analyze counterpart behavior and motivations
- Navigate vendor or partnership negotiations
- De-escalate tense situations
- Build rapport in adversarial settings
- Close deals without compromising your position

**Example prompts:**
- *"I'm negotiating a 20% raise. Help me prepare using the Ackerman method. Use negotiation skill."*
- *"My client said 'that's not fair.' How do I respond? Use negotiation skill."*
- *"Write calibrated questions to uncover why the vendor won't budge on price. Use negotiation skill."*
- *"Draft an accusation audit for a meeting where they think we've been unresponsive. Use negotiation skill."*
- *"How do I get them to say 'That's right' about our proposal? Use negotiation skill."*
- *"The other party has gone silent. What's my re-engagement strategy? Use negotiation skill."*

---

## Copyright & Disclaimer

The methodologies and frameworks referenced in these skills are the intellectual property of their respective authors and publishers. All copyrights belong to:

- **Jobs to Be Done**: Clayton M. Christensen, Taddy Hall, Karen Dillon, David S. Duncan
- **Making Websites Win**: Karl Blanks, Ben Jesson (Conversion Rate Experts)
- **Refactoring UI**: Adam Wathan, Steve Schoger
- **Human Interface Guidelines**: Apple Inc.
- **Scorecard Marketing**: Daniel Priestley, Glen Carlson
- **Building a StoryBrand**: Donald Miller
- **Hooked**: Nir Eyal
- **Don't Make Me Think**: Steve Krug
- **10 Usability Heuristics**: Jakob Nielsen (Nielsen Norman Group)
- **On Web Typography**: Jason Santa Maria
- **Top Design**: Techniques inspired by Locomotive, Studio Freight, AREA 17, Active Theory, Hello Monday, Dogstudio, Tonik, Instrument, Resn
- **Never Split the Difference**: Chris Voss, Tahl Raz

These skills were created without directly copying or reproducing content from the original books or materials. They are based on:
- Publicly available information about the methodologies
- General knowledge embedded in large language models
- Common industry practices and terminology

We encourage users to purchase and read the original books for the complete, authoritative treatment of each methodology. The skills in this repository are intended as practical aids, not replacements for the source materials.
