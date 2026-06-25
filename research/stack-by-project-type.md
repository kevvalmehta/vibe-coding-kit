# Research note — boring/proven stack by project type (feeds Conductor v3 `/stack`)

**Topic:** which "boring, proven, low-ops" stack fits each common project type a non-technical solo
business owner would build.
**Date:** 2026-06-25 · **Method:** research-scout, deep pass (4 parallel researchers, ~32 cited
searches) + separate citation pass.
**Consumers:** the new `/stack` skill (Conductor v3), `grill-me`, `/speckit-plan`.

> *Cited* = each claim links to the page it came from. Treat vendor/competitor blogs as informed-but-
> interested opinion; primary docs (Vercel/Streamlit/Astro/Anthropic/Supabase docs) are high-confidence.

---

## ⭐ The single most important finding (surfaced by 3 of 4 researchers independently)

**The kit's own default pairing — Streamlit + Vercel — is a MISMATCH.** Vercel is built for serverless
frontends (Next.js/React) and **does not host a Streamlit app**, which needs a persistent long-running
server process. Default Streamlit apps to **Streamlit Community Cloud** (free, GitHub-connected,
officially recommended). Keep **Vercel only for a real Next.js/React frontend** that calls a separate
API. Everything else in the kit's default (Python, Claude API, Supabase/Postgres+pgvector) is well
supported.
- Sources: https://vercel.com/docs/limits · https://docs.streamlit.io/deploy/streamlit-community-cloud ·
  https://medium.com/@pbollipalli/vercel-vs-streamlit-a-comparison-a15e2bb7ecee ·
  https://discuss.streamlit.io/t/easiest-streamlit-deployement-other-than-streamlit-community-cloud/94530

**Correction to retire:** the old "Vercel functions time out at 10s" claim is **outdated** — current
docs say 300s (Hobby) up to 800s (Pro). The real reason to avoid Vercel for backends is the serverless
model (no always-on process, cold starts), not the timeout. Source: https://vercel.com/docs/functions/limitations

---

## The decision table (project type → boring default)

| Project type | Language | Framework | Database | Hosting | Top "when this is WRONG → use instead" |
|---|---|---|---|---|---|
| **Internal dashboard / data tool** | Python | **Streamlit** | **SQLite** first → Supabase (Postgres) when ≥2 writers or you need logins/RLS | **Streamlit Community Cloud** (free) — *not Vercel* | High-traffic/public multi-user, or heavy chart interactivity → Plotly Dash or a real web framework |
| **Automation / scheduled script** | Python | plain script (`requests`/`pandas`/SDK) — no UI | usually **none** (Supabase only if output must be queried later) | **GitHub Actions cron** (free) — *not Vercel* | Needs guaranteed timing or long/stateful runs → Render Cron / Railway worker / cloud scheduler (GH Actions cron is best-effort: 5-min min, can be delayed, auto-disables after 60 days idle on public repos) |
| **Customer-facing web app** (login, data) | TypeScript (or Python) | **Next.js** (or **Django** if you want admin+ORM batteries) | **Supabase** (Postgres, RLS on by default) | **Vercel** (Next.js) / **Render** or **Railway** (Django) | **Streamlit is WRONG for a logged-in product for strangers** (full-page reload per input, no real auth/branding) |
| **API / backend service** | Python | **FastAPI** (Flask for simplest MVP) | **Supabase** (Postgres, RLS) | **Render** or **Railway** (always-on container) | Vercel's serverless model is wrong for an always-on API; Render free tier cold-starts → pay for always-on in prod |
| **Marketing / brochure site** (SEO matters) | — | **No-code builder** (Framer/Webflow/Squarespace) for a true non-techie; **Astro** if AI/dev builds | none (form service e.g. Formspree for contact) | Static host + CDN (Netlify / Cloudflare Pages / Vercel) | **Streamlit is WRONG** (no custom-domain SEO/sitemap/robots control); Supabase overkill unless it grows app features |
| **Mobile app** (iOS/Android) | — | **No-code** (FlutterFlow/Adalo) or **PWA** for non-techie; **React Native + Expo** (or Flutter) if coded | **Supabase** or Firebase (managed) | App Store + Google Play (builders auto-submit) / install-to-home-screen (PWA) | Streamlit/Vercel don't ship native apps; coded RN/Flutter needs a real dev; PWA can't be in the App Store |
| **AI / LLM app** (chatbot, agent, "chat with my docs") | Python | **Streamlit** for a data app *around* AI; **Gradio** or **Chainlit** for a pure chat window | **Supabase + pgvector** (only if RAG) | **Streamlit Community Cloud** (Streamlit) / container host (Gradio/Chainlit) — *not Vercel for Streamlit* | Pure chatbot on Streamlit is awkward (full reload breaks token streaming) → Gradio/Chainlit |
| **Other / advanced / doesn't fit** (e.g. "an AI OS", a desktop assistant that controls the machine, anything exotic) | — depends, clarify first | **No boring default — escape hatch** (see below) | — | — | Do NOT force a default. Clarify what it really is → research-scout → reality-check scope with /discover → if AI-heavy, agent-architect |

### The escape-hatch lane (the 8th type)

When a request matches none of the seven rows, `/stack` MUST NOT invent a confident default. Instead:
1. **Clarify what it actually is** — the term may hide very different builds.
2. **research-scout** the specific thing (cited, current evidence).
3. **Reality-check scope with `/discover`** — is this solo-buildable at all, or a team/years effort?
4. **If AI-heavy → `agent-architect`** for the agent design.

Worked example — **"AI OS"** (a fuzzy term covering 3 different builds):
- **A real OS with AI baked in** — systems languages (C/Rust), kernel + drivers, teams/years. *Not* a
  boring/proven solo project; say so plainly.
- **An "AI operating layer" / agent platform** (what people usually mean) — really an ambitious AI app:
  Python/TS + an agent-orchestration framework + Claude API + Supabase + integrations + a normal web
  host. Maps onto the AI-app row at its high end; `agent-architect` essential.
- **A desktop assistant that controls the computer** — a desktop shell (Electron/Tauri or Python) +
  Claude API + OS-automation libs + serious permission/security care.

---

## Cross-cutting finding — plain prompt-to-API beats LangChain for a beginner

For an AI app, **start with direct Claude API calls; skip heavy frameworks (LangChain) until you
genuinely need multi-step agents.** Backed by both the model vendor and practitioners:
- Anthropic: "find the simplest solution possible… only increasing complexity when needed"; frameworks
  "create extra layers of abstraction that can obscure the underlying prompts… harder to debug."
  https://www.anthropic.com/research/building-effective-agents
- Practitioner critiques: https://www.designveloper.com/blog/is-langchain-bad/ ·
  https://news.ycombinator.com/item?id=36648272 ·
  https://dev.to/alexroor4/the-pros-and-cons-of-langchain-for-beginner-developers-25a7
- When a framework IS worth it (multi-step agents, many integrations): https://docs.langchain.com/oss/python/langchain/rag

Rule for this owner: **single LLM call + retrieval = no framework.** Add one only after a plain version
works and you hit a wall. (This matches `agent-architect`'s existing guidance — cross-link there.)

---

## Surfaced disagreements + confidence flags (not averaged)

1. **"Streamlit doesn't scale → use Dash"** — strongest claims come from Plotly's own blog (makes Dash)
   and monetized comparison sites. An independent engineer counters: default to Streamlit, ~80% of
   dashboards never need Dash. Consensus on the *dividing line*: data display = fine; interactive
   multi-user product with auth = not its job. https://plotly.com/blog/best-streamlit-alternatives-production-data-apps/ ·
   https://leandataengineer.com/blog/dash-vs-streamlit-vs-react-for-data-applications/
2. **SQLite → Postgres switch point** — sources agree SQLite is genuinely fine for single-user/internal
   tools (hard limit: one writer at a time) but disagree on when to leave it. *Confidence note: the
   SQLite guidance rests on secondary engineering blogs; sqlite.org's own "appropriate uses" page was
   not fetched this session.* https://www.dbpro.app/learn/sqlite/guides/sqlite-vs-postgresql
3. **FastAPI vs Django for APIs** — FastAPI for a pure API; Django when you also want a built-in
   admin/ORM. https://strapi.io/blog/fastapi-vs-flask-python-framework-comparison ·
   https://blog.jetbrains.com/pycharm/2025/02/django-flask-fastapi/
4. **Flutter vs React Native** — genuinely contested (Statista ~46% Flutter vs an enterprise survey
   ~42% RN; SO daily use near-tied). Either is a defensible default. *Confidence: medium — secondary
   sources quoting Statista/SO, primaries not fetched.*
5. **pgvector vs Pinecone** — direction agrees (pgvector cheaper below ~tens of millions of vectors;
   Pinecone auto-scales at very large scale). The "11x faster / $70 cheaper" magnitude is **Supabase's
   own claim**, cross-checked by Encore but treat as vendor figure. https://supabase.com/blog/pgvector-vs-pinecone ·
   https://encore.dev/articles/pgvector-vs-pinecone
6. **Hosting form/custom-domain feature claims** (Netlify/Cloudflare/Vercel) — *no primary page fetched
   this session* (a Netlify docs URL 404'd); these rest on general knowledge, flagged per no-fabrication.
7. **AI-assisted building lowers the "SSGs need the command line" barrier** — generic articles call
   Astro/SSGs developer-only; in this kit an AI drives the build, so Astro is viable for a non-techie.

---

## Recommendation for `/stack` (v3)

Build the skill's decision table from the rows above. Anchor it on three honest moves the kit isn't
making today: (1) **stop pairing Streamlit with Vercel** — route Streamlit apps to Streamlit Community
Cloud; (2) keep **Vercel + Supabase** as the default *only* for Next.js customer apps; (3) for each
project type, name the **one trigger that makes the default wrong** so the owner knows when to deviate.
Recommendation-only — the build step does setup (scaffolding = deferred to v7).
