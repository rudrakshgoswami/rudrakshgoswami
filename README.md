<!-- Image paths are relative on purpose. GitHub resolves them against this repo
     and this ref, so any branch renders its own assets and can be previewed
     before it reaches main.

     The ?v= params do nothing and are kept only so the versions line up with
     the filenames. Relative paths resolve to /raw/<ref>/..., which is GitHub's
     own route rather than the camo proxy, and it caches by path with
     max-age=300 and ignores the query. So a card you change looks stale for up
     to five minutes after the push and then fixes itself. Bumping ?v= does not
     help; waiting does.

     The three-across rows use width="272", not a percentage. The profile
     README column is 846px at a wide viewport but only 293px on a phone, so
     32.5% put each tile at 95px there and its copy at under 4px. Fixed widths
     mean the row wraps to two lines, then one, and every card stays readable.
     Keep each row's three anchors on a single line: at 846px the three cards
     plus two word-spaces come to 825px, and a line break would add enough to
     push the third one down. -->

<div align="center">

<img src="./assets/hero.svg?v=3" width="860" alt="Rudraksh Goswami, web developer at Vocsy Infotech in Surat, India" />

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/links/site.svg?v=1" alt="rudrakshgoswami.vercel.app" /></a>
<a href="https://linkedin.com/in/rudrakshgoswami"><img src="./assets/links/linkedin.svg?v=1" alt="LinkedIn" /></a>
<a href="mailto:rudrakshgoswami5555@gmail.com"><img src="./assets/links/email.svg?v=1" alt="Email" /></a>

<!-- Only the digits are a badge. The label half is drawn like every other chip
     here and the count sits beside it as the one coloured thing. Keep the two
     images on one line with no space between them; the 5px gap is baked into
     views.svg.

     This was shields reading abacus.jasoncameron.dev, until it started printing
     "inaccessible" in place of the number. Abacus itself is fine: /get/ and
     /hit/ both answer 200 from a browser, and shields reaches its /healthcheck
     and prints "ok". It is only the counter keys that come back unreachable to
     shields, including keys that do exist, which is what rate limiting a shared
     IP looks like from the outside. Komarev serves the SVG itself, so there is
     no second service in the chain to fail. -->
<img src="./assets/links/views.svg?v=1" alt="profile views" /><img src="https://komarev.com/ghpvc/?username=rudrakshgoswami&label=&color=4F46E5&style=flat" alt="View count" />

</div>

<br>

<div align="center">

<img src="./assets/shipped.svg?v=2" width="860" alt="Fifty-six tiles arranged as an isometric field: fifty blog-network sites, two live client stores, a portfolio site and three open-source repositories" />

<br>

<img src="./assets/numbers.svg?v=1" width="860" alt="56 shipped: fifty sites, two stores, a portfolio and three repos. 2 live client stores in production, 26 months at Vocsy from intern to developer, about a day per build" />

<br>

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/tile-shipped.svg?v=2" width="272" alt="Shipped: 50+ sites. A blog network built on a standardised WordPress base, about a day per site." /></a> <a href="https://heliosexport.com"><img src="./assets/tile-running.svg?v=2" width="272" alt="Running: 2 stores. heliosexport.com and shop.sanmarfoods.com, both live in production." /></a> <a href="https://ai-engineer-roadmap-drab.vercel.app"><img src="./assets/tile-learning.svg?v=2" width="272" alt="Learning: 314 resources. An AI engineering curriculum rebuilt as a site you can actually work through." /></a>

</div>

<br>

Two years at **Vocsy Infotech**, promoted from intern to developer in six months. Most profiles stop at the code. I get handed a domain and give back a site that is live, which means the DNS, the SSL, the server, the store and the theme are all mine to get right.

| Store | What I built |
|-------|--------------|
| **[heliosexport.com](https://heliosexport.com)** | Jewellery export storefront on WooCommerce. Product catalogue, categories and checkout, built from scratch. |
| **[shop.sanmarfoods.com](https://shop.sanmarfoods.com)** | Food and snacks retailer in Singapore, on Shopify. Theme sections and product pages customized in Liquid. |

<br>

### How the pipeline works

The number is not the point, the workflow is. What it is made of:

* **Agents that run multi-step jobs.** They plan, call tools and carry a task through, instead of one-off prompts.
* **Every generated change reviewed before it ships.** The speed comes from the workflow, not from trusting the output.
* **Internal AI dashboards and tooling** so the people who are not developers can still run the thing.

<br>

<div align="center">

<img src="./assets/stack.svg?v=1" width="860" alt="The stack I work across as six exploded layers: DNS and edge, server, database, platform, code, and an AI layer on top" />

</div>

<br>

### Open source

<div align="center">

<a href="https://github.com/rudrakshgoswami/ai-engineer-roadmap"><img src="./assets/repo-roadmap.svg?v=2" width="272" alt="ai-engineer-roadmap, HTML. Search, filters, progress and two themes over 314 counted resources. Live on Vercel." /></a> <a href="https://github.com/rudrakshgoswami/vincent-app"><img src="./assets/repo-vincent.svg?v=2" width="272" alt="vincent-app, JavaScript. MERN booking platform. Venue slots lock in real time over Socket.io, so no double books." /></a> <a href="https://github.com/rudrakshgoswami/ipl-data-analysis"><img src="./assets/repo-ipl.svg?v=2" width="272" alt="ipl-data-analysis, Python. Nine IPL seasons in pandas. The toss is a 50.7% coin flip and the model loses to chance." /></a>

</div>

| Repo | Beyond the card |
|------|-----------------|
| **[ai-engineer-roadmap](https://github.com/rudrakshgoswami/ai-engineer-roadmap)** | Live at [ai-engineer-roadmap-drab.vercel.app](https://ai-engineer-roadmap-drab.vercel.app). The 24-week plan is Aditya Dewaskar's, the build is mine. The 314 resources were lifted out of an 18-page PDF and counted against the arrow glyphs printed beside them, so the number is proved rather than claimed. |
| **[vincent-app](https://github.com/rudrakshgoswami/vincent-app)** | The slot lock has a cleanup sweeper behind it, so a dropped session cannot hold an evening hostage. Ships with a demo payment gateway and 110 seeded menu items, so it runs with no API keys at all. |
| **[ipl-data-analysis](https://github.com/rudrakshgoswami/ipl-data-analysis)** | Published as a negative result rather than hidden behind an accuracy score: the match-winner model loses to a trivial baseline, and the toss is a coin flip. |

<br>

### Right now

* Going deeper on **LLM evaluation, agent orchestration and Python for production ML**
* Open to **freelance website, e-commerce and automation work**. Hire me on [Fiverr](https://www.fiverr.com/rudraksh_2005) or [Freelancer](https://www.freelancer.in/u/rudrakshgoswami7)
* Ask me about shipping e-commerce stores, AI-assisted development, hosting and migrations

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

<!-- All eight social chips were here: X, Instagram, Behance, CodePen, Bluesky,
     Reddit, Quora and Pinterest. Every one is built and committed under
     assets/links/, so restoring any of them is a single line.

     They came out because every account behind them is empty. Checked on
     2026-11-24: Behance has no projects, CodePen says "hasn't created any Pens
     yet", and X reads 0 posts. A recruiter who clicks one of those lands on
     nothing, which is worse than never offering the link. Put work in one of
     them and its chip has earned its place back. -->

</div>
