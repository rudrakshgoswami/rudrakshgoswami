<!-- Image paths are relative on purpose. GitHub resolves them against this repo
     and this ref, so any branch renders its own assets and can be previewed
     before it reaches main.

     The ?v= params do nothing and are kept only so the versions line up with
     the filenames. Relative paths resolve to /raw/<ref>/..., which is GitHub's
     own route rather than the camo proxy, and it caches by path with
     max-age=300 and ignores the query. So a card you change looks stale for up
     to five minutes after the push and then fixes itself. Bumping ?v= does not
     help; waiting does. -->

<div align="center">

<img src="./assets/hero.svg?v=3" width="860" alt="Rudraksh Goswami, web developer at Vocsy Infotech in Surat, India" />

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/links/site.svg?v=1" alt="rudrakshgoswami.vercel.app" /></a>
<a href="https://linkedin.com/in/rudrakshgoswami"><img src="./assets/links/linkedin.svg?v=1" alt="LinkedIn" /></a>
<a href="mailto:rudrakshgoswami5555@gmail.com"><img src="./assets/links/email.svg?v=1" alt="Email" /></a>

<!-- Only the digits are shields now. Asked for an empty label it returns the
     number alone, so the label half is drawn like every other chip here and the
     count sits beside it as the one coloured thing. Keep the two images on one
     line with no space between them; the 5px gap is baked into views.svg.
     If abacus disappears, shields renders "invalid" in place of the number. -->
<img src="./assets/links/views.svg?v=1" alt="profile views" /><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fabacus.jasoncameron.dev%2Fhit%2Frudrakshgoswami%2Fprofile&query=%24.value&label=&color=4F46E5&style=flat" alt="View count" />

</div>

<br>

<div align="center">

<img src="./assets/shipped.svg?v=2" width="860" alt="Fifty-six tiles arranged as an isometric field: fifty blog-network sites, two live client stores, a portfolio site and three open-source repositories" />

<img src="./assets/numbers.svg?v=1" width="860" alt="56 shipped: fifty sites, two stores, a portfolio and three repos. 2 live client stores in production, 26 months at Vocsy from intern to developer, about a day per build" />

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/tile-shipped.svg?v=1" width="32.5%" alt="Shipped: 50+ sites. A blog network built on a standardised WordPress base, about a day per site." /></a>
<a href="https://heliosexport.com"><img src="./assets/tile-running.svg?v=1" width="32.5%" alt="Running: 2 stores. heliosexport.com and shop.sanmarfoods.com, both live in production." /></a>
<a href="https://ai-engineer-roadmap-drab.vercel.app"><img src="./assets/tile-learning.svg?v=1" width="32.5%" alt="Learning: 314 resources. An AI engineering curriculum rebuilt as a site you can actually work through." /></a>

</div>

<br>

Two years at **Vocsy Infotech**, promoted from intern to developer in six months. Most profiles stop at the code. I get handed a domain and give back a site that is live, which means the DNS, the SSL, the server, the store and the theme are all mine to get right.

| Project | Stack | What it is |
|---------|-------|------------|
| **[heliosexport.com](https://heliosexport.com)** | WooCommerce | Jewellery export storefront. Full build: product catalogue, categories, checkout. |
| **[shop.sanmarfoods.com](https://shop.sanmarfoods.com)** | Shopify · Liquid | Food and snacks retailer in Singapore. Theme sections and product pages customized in Liquid. |
| **Blog network, 50+ sites** | WordPress · Claude Code | Designed, built and launched end to end. Standardized theme and plugin stack, every generated change reviewed per site, about a day per site. |

<br>

### ⚙️ How 50+ sites actually happen

The number is not a flex, it is the proof that the workflow holds up. What it is made of:

* **Agents that run multi-step jobs.** They plan, call tools and carry a task through, instead of one-off prompts.
* **A standardized base** so every site starts from the same reviewed theme and plugin stack, and only the real differences get built.
* **Every generated change reviewed before it ships.** The speed comes from the workflow, not from trusting the output.
* **Internal AI dashboards and tooling** so the people who are not developers can still run the thing.

<br>

<div align="center">

<img src="./assets/stack.svg?v=1" width="860" alt="The stack I work across as six exploded layers: DNS and edge, server, database, platform, code, and an AI layer on top" />

</div>

<br>

### 📦 Open source

<div align="center">

<a href="https://github.com/rudrakshgoswami/ai-engineer-roadmap"><img src="./assets/repo-roadmap.svg?v=1" width="32.5%" alt="ai-engineer-roadmap, HTML. Search, filters, progress and two themes over 314 counted resources. Live on Vercel." /></a>
<a href="https://github.com/rudrakshgoswami/vincent-app"><img src="./assets/repo-vincent.svg?v=1" width="32.5%" alt="vincent-app, JavaScript. MERN booking platform. Venue slots lock in real time over Socket.io, so no double books." /></a>
<a href="https://github.com/rudrakshgoswami/ipl-data-analysis"><img src="./assets/repo-ipl.svg?v=1" width="32.5%" alt="ipl-data-analysis, Python. Nine IPL seasons in pandas. The toss is a 50.7% coin flip and the model loses to chance." /></a>

</div>

| Repo | What is in it |
|------|---------------|
| **[ai-engineer-roadmap](https://github.com/rudrakshgoswami/ai-engineer-roadmap)** | A 24-week AI engineering plan, rebuilt as a site you can actually work through: [ai-engineer-roadmap-drab.vercel.app](https://ai-engineer-roadmap-drab.vercel.app). The roadmap is Aditya Dewaskar's, the build is mine. 314 free resources lifted out of an 18-page PDF and counted against the arrow glyphs printed beside them so the number is proved rather than claimed, then search, filters, progress tracking and two themes on top. |
| **[vincent-app](https://github.com/rudrakshgoswami/vincent-app)** | MERN restaurant, venue and catering booking platform. Venue slots lock in real time over Socket.io with a cleanup sweeper, so two people cannot book the same evening. Ships with a demo payment gateway and 110 seeded menu items, so it runs with no API keys at all. |
| **[ipl-data-analysis](https://github.com/rudrakshgoswami/ipl-data-analysis)** | Nine IPL seasons in pandas. The interesting part is the negative result: the toss is a 50.7% coin flip, and the match-winner model loses to a trivial baseline. Published as a finding rather than hidden behind an accuracy score. |

<br>

### 🚀 Right now

* 🔭 Running a 50+ site WordPress pipeline on Claude Code at **Vocsy Infotech**, plus the internal dashboard that lets non-devs drive it
* 🌱 Going deeper on **LLM evaluation, agent orchestration and Python for production ML**
* 🤝 Open to **freelance website, e-commerce and automation work**. Hire me on [Fiverr](https://www.fiverr.com/rudraksh_2005) or [Freelancer](https://www.freelancer.in/u/rudrakshgoswami7)
* 💬 Ask me about shipping e-commerce stores, AI-assisted development, hosting, DNS and migrations

<br>

<div align="center">

**Let's build something that ships.**

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/links/portfolio.svg?v=1" alt="Portfolio" /></a>
<a href="mailto:rudrakshgoswami5555@gmail.com"><img src="./assets/links/email.svg?v=1" alt="Email" /></a>
<a href="https://linkedin.com/in/rudrakshgoswami"><img src="./assets/links/linkedin.svg?v=1" alt="LinkedIn" /></a>
<a href="https://www.fiverr.com/rudraksh_2005"><img src="./assets/links/fiverr.svg?v=1" alt="Fiverr" /></a>
<a href="https://www.freelancer.in/u/rudrakshgoswami7"><img src="./assets/links/freelancer.svg?v=1" alt="Freelancer" /></a>
<!-- Upwork is deliberately not shown yet: profile visibility is locked to Private until
     Connects and identity verification are done, so the link is dead for everyone.
     The chip is built and committed. Delete the two comment markers once it is public.
<a href="https://www.upwork.com/freelancers/~01dd86b2aac38e4ee9"><img src="./assets/links/upwork.svg?v=1" alt="Upwork" /></a>
-->

<a href="https://x.com/rudxgoswami"><img src="./assets/links/x.svg?v=1" alt="X" /></a>
<a href="https://instagram.com/rudrakshgoswami_"><img src="./assets/links/instagram.svg?v=1" alt="Instagram" /></a>
<a href="https://behance.net/rudrakshgoswami3"><img src="./assets/links/behance.svg?v=1" alt="Behance" /></a>
<a href="https://codepen.io/Rudraksh-Goswami"><img src="./assets/links/codepen.svg?v=1" alt="CodePen" /></a>
<a href="https://bsky.app/profile/rudrakshgoswami"><img src="./assets/links/bluesky.svg?v=1" alt="Bluesky" /></a>
<a href="https://reddit.com/user/rudrakshgoswami"><img src="./assets/links/reddit.svg?v=1" alt="Reddit" /></a>
<a href="https://quora.com/profile/Rudraksh-Goswami-18"><img src="./assets/links/quora.svg?v=1" alt="Quora" /></a>
<a href="https://pinterest.com/rudrakshgoswami_"><img src="./assets/links/pinterest.svg?v=1" alt="Pinterest" /></a>

</div>
