<!-- Flat card system, v2. docs/readme-redesign-v2.md has the reasoning.

     Image paths are relative on purpose: GitHub resolves them against this repo
     and this ref, so any branch renders its own assets and can be previewed
     before it reaches main. The ?v= params do nothing and are kept only so the
     versions line up with the files. Relative paths resolve to /raw/<ref>/...,
     GitHub's own route rather than the camo proxy, which caches by path with
     max-age=300 and ignores the query. A card you change looks stale for up to
     five minutes after the push and then fixes itself. Waiting works, bumping
     ?v= does not.

     Card rows use fixed pixel widths, never percentages. The profile README
     column is 846px at a wide viewport and 293px on a phone, so a percentage
     put each card at under 100px there and its copy at under 4px. At 846px,
     three 272s plus two word-spaces come to 825, and two 416s come to 836.
     Below that they wrap, and every card stays full size and readable. Keep
     each row's anchors on a single line: a line break adds a space wide enough
     to push the last card down.

     Vertical spacing comes from <p>, not from <br>. A <br> between two images
     inside a centred div does nothing at all, measured at 6px, the same as no
     tag: the line has already wrapped, so the break has nothing left to break.
     The rhythm on this page is three values and each one is chosen:

       6px   a title bar and the card directly beneath it, which are one unit
       16px  a <p> boundary, between units inside a section
       46px  a </div><br><div> boundary, between sections

     Horizontal gutters are 4px, the width of one space character. Anything
     wider would have to be a non-breaking space, and that would stop the rows
     wrapping on a phone, which costs far more than 4px buys. -->

<div align="center">

<p><img src="./assets/hero.svg?v=4" width="860" alt="Rudraksh Goswami, web developer at Vocsy Infotech in Surat, India" /></p>

<a href="https://rudrakshgoswami.vercel.app"><img src="./assets/links/site.svg?v=1" alt="rudrakshgoswami.vercel.app" /></a>
<a href="https://linkedin.com/in/rudrakshgoswami"><img src="./assets/links/linkedin.svg?v=1" alt="LinkedIn" /></a>
<a href="mailto:rudrakshgoswami5555@gmail.com"><img src="./assets/links/email.svg?v=1" alt="Email" /></a>

<!-- Only the digits are a badge. The label half is drawn like every other chip
     here and the count sits beside it as the one coloured thing. Keep the two
     images on one line with no space between them; the 5px gap is baked into
     views.svg.

     This was shields reading abacus.jasoncameron.dev, until it started printing
     "inaccessible" in place of the number. Abacus itself answers 200 from a
     browser and shields reaches its /healthcheck, but every counter key comes
     back unreachable to shields, which is what rate limiting a shared IP looks
     like. Komarev serves the SVG itself, so nothing sits in between. -->
<img src="./assets/links/views.svg?v=1" alt="profile views" /><img src="https://komarev.com/ghpvc/?username=rudrakshgoswami&label=&color=4F46E5&style=flat" alt="View count" />

</div>

<br>

<div align="center">

<img src="./assets/t-record.svg?v=1" width="860" alt="Section 01, the record" />

<p><img src="./assets/record.svg?v=1" width="860" alt="56 shipped: fifty blog-network sites, two live client stores, a portfolio site and three open-source repositories. 2 live client stores in production, 26 months at Vocsy from intern to developer, about a day per build" /></p>

<p><a href="https://rudrakshgoswami.vercel.app"><img src="./assets/tile-shipped.svg?v=2" width="272" alt="Shipped: 50+ sites. A blog network built on a standardised WordPress base, about a day per site." /></a> <a href="https://heliosexport.com"><img src="./assets/tile-running.svg?v=2" width="272" alt="Running: 2 stores. heliosexport.com and shop.sanmarfoods.com, both live in production." /></a> <a href="https://ai-engineer-roadmap-drab.vercel.app"><img src="./assets/tile-learning.svg?v=2" width="272" alt="Learning: 314 resources. An AI engineering curriculum rebuilt as a site you can actually work through." /></a></p>

</div>

<br>

<div align="center">

<img src="./assets/t-work.svg?v=1" width="860" alt="Section 02, selected work" />

<p><a href="https://heliosexport.com"><img src="./assets/store-helios.svg?v=1" width="416" alt="heliosexport.com, WooCommerce, live. Jewellery export storefront. Product catalogue, categories and checkout, built from scratch." /></a> <a href="https://shop.sanmarfoods.com"><img src="./assets/store-sanmar.svg?v=1" width="416" alt="shop.sanmarfoods.com, Shopify and Liquid, live. Food and snacks retailer in Singapore. Theme sections and product pages customised in Liquid." /></a></p>

</div>

<br>

<div align="center">

<img src="./assets/t-source.svg?v=1" width="860" alt="Section 03, open source" />

<p><a href="https://github.com/rudrakshgoswami/ai-engineer-roadmap"><img src="./assets/repo-roadmap.svg?v=2" width="272" alt="ai-engineer-roadmap, HTML. Search, filters, progress and two themes over 314 counted resources. Live on Vercel." /></a> <a href="https://github.com/rudrakshgoswami/vincent-app"><img src="./assets/repo-vincent.svg?v=2" width="272" alt="vincent-app, JavaScript. MERN booking platform. Venue slots lock in real time over Socket.io, so no double books." /></a> <a href="https://github.com/rudrakshgoswami/ipl-data-analysis"><img src="./assets/repo-ipl.svg?v=2" width="272" alt="ipl-data-analysis, Python. Nine IPL seasons in pandas. The toss is a 50.7% coin flip and the model loses to chance." /></a></p>

</div>

<!-- The one text layer left on the page. It survives because this detail is the
     most credible thing here and a 12px card line cannot hold it, and because
     text in an SVG is unselectable and invisible to GitHub search. -->

| Repo | Beyond the card |
|------|-----------------|
| **[ai-engineer-roadmap](https://github.com/rudrakshgoswami/ai-engineer-roadmap)** | Live at [ai-engineer-roadmap-drab.vercel.app](https://ai-engineer-roadmap-drab.vercel.app). The 24-week plan is Aditya Dewaskar's, the build is mine. The 314 resources were lifted out of an 18-page PDF and counted against the arrow glyphs printed beside them, so the number is proved rather than claimed. |
| **[vincent-app](https://github.com/rudrakshgoswami/vincent-app)** | The slot lock has a cleanup sweeper behind it, so a dropped session cannot hold an evening hostage. Ships with a demo payment gateway and 110 seeded menu items, so it runs with no API keys at all. |
| **[ipl-data-analysis](https://github.com/rudrakshgoswami/ipl-data-analysis)** | Published as a negative result rather than hidden behind an accuracy score: the match-winner model loses to a trivial baseline, and the toss is a coin flip. |

<br>

<div align="center">

<p><img src="./assets/toolkit.svg?v=1" width="860" alt="Toolkit. AI layer: Claude Code, agents, automation. Code: PHP, JavaScript, Liquid, Python. Platform: WordPress, WooCommerce, Shopify. Database: MySQL. Server: DigitalOcean, Hostinger, cPanel, Cloudways. DNS and edge: Cloudflare, Namecheap, SSL." /></p>

<p><img src="./assets/now.svg?v=1" width="860" alt="Right now. Learning: LLM evaluation, agent orchestration and Python for production ML. Available: freelance website, e-commerce and automation work. Ask me about shipping e-commerce stores, AI-assisted development, hosting and migrations." /></p>

<p><img src="./assets/contact.svg?v=1" width="860" alt="Let's build something that ships. rudrakshgoswami5555@gmail.com" /></p>

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
     yet", and X reads 0 posts. A recruiter who clicks one lands on nothing,
     which is worse than never offering the link. -->

</div>
