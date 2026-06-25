# Stack decision table — the `/stack` skill's core knowledge

Grounded in `research/stack-by-project-type.md` (cited research-scout pass, 2026-06-25). Each row gives
the **boring/proven default** plus a **pay-for-better tier** (with rough cost + the concrete benefit),
and the **one trigger** that makes the default the wrong choice. *Tier = a level of option; the free/
boring one vs a paid/better one.* Costs are rough 2026 figures — confirm live before relying on them.

> ⭐ **The correction baked into every row: never host a Streamlit app on Vercel.** Vercel can't run
> Streamlit (Streamlit needs an always-running server; Vercel doesn't keep one alive). Streamlit →
> **Streamlit Community Cloud** (free) or a container host. Vercel is only for a Next.js/React frontend.

---

## 1. Internal dashboard / data tool
*A private tool for you/your team to see and poke at data.*
- **Language:** Python (free) — one language for the data + the screen.
- **Framework:** Streamlit (free) — a Python tool that turns a script into a web dashboard.
- **Database:** free/simple → **SQLite** ($0, a single file, one writer at a time); pay-for-better →
  **Supabase** (free tier, ~$25/mo Pro — multi-user writes, logins, automatic backups).
- **Hosting:** free → **Streamlit Community Cloud** ($0, sleeps when idle, public repo); pay-for-better
  → **Render**/Hugging Face Spaces (~$7/mo — always-on, your own domain). **Not Vercel.**
- **Wrong when:** many concurrent/public users or heavy chart-to-chart interactivity → use Plotly Dash
  or a real web framework.

## 2. Automation / scheduled script
*Code that runs on a timer or on demand and exits — no screen.*
- **Language:** Python (free).
- **Framework:** a plain script (`requests`/`pandas`/an SDK) — no UI framework.
- **Database:** usually **none**; add Supabase only if results must be stored and queried later.
- **Hosting/scheduler:** free → **GitHub Actions cron** ($0 public; ~2,000 min/mo private — but timing
  is best-effort, 5-min minimum, auto-disables after 60 days idle on public repos); pay-for-better →
  **Render Cron / Railway worker** (~$5–7/mo — reliable timing, long/stateful runs, retries). **Not
  Vercel** (serverless, can't keep a process alive).
- **Wrong when:** you need guaranteed on-time runs or long/stateful jobs → a dedicated scheduler/worker.

## 3. Customer-facing web app (login, data, interactive)
*A real product strangers log into and use.*
- **Language:** TypeScript (free) — or Python if you choose Django.
- **Framework:** **Next.js** (free; the modern full-stack web framework) — or **Django** (free; Python,
  batteries-included admin + ORM).
- **Database:** **Supabase** (free tier → ~$25/mo Pro) — managed Postgres with row-level security on by
  default (the safest beginner database).
- **Hosting:** **Vercel** for Next.js (free Hobby → ~$20/mo Pro); **Render/Railway** for Django (~$7/mo
  always-on).
- **Wrong when:** ❌ **Streamlit is the wrong tool here** — it reloads the whole page on every input and
  has no real auth/branding. Use Next.js or Django for a logged-in product.

## 4. API / backend service
*A programmatic backend other apps/devices call — no screen of its own.*
- **Language:** Python (free).
- **Framework:** **FastAPI** (free — auto docs, input validation, async) — Flask for the simplest MVP.
- **Database:** **Supabase** (Postgres, RLS).
- **Hosting:** **Render** or **Railway** (~$7/mo always-on container) — an API wants a process that
  stays running. Render's free tier cold-starts (slow first hit) → pay for always-on in production.
  **Vercel's serverless model is usually wrong** for an always-on API.
- **Wrong when:** unpredictable external traffic on a free sleeping host → pay for always-on, or use a
  managed container/Cloud Run.

## 5. Marketing / brochure / landing site (SEO matters)
*Mostly static pages; getting found on Google is the whole point.*
- **Framework:** for a true non-techie → a **no-code builder** (Framer/Webflow/Squarespace, ~$15–25/mo,
  hosting included); if an AI/dev builds it → **Astro** (free; built for fast, SEO-friendly content sites).
- **Database:** **none** (use a form service like Formspree for a contact form). Add a database only if
  it grows real app features.
- **Hosting:** static host + CDN — **Netlify / Cloudflare Pages / Vercel** (free tiers; paid for scale).
- **Wrong when:** ❌ **Streamlit is wrong** (no custom-domain SEO, sitemaps, or robots control); Supabase
  is overkill for a brochure.

## 6. Mobile app (iOS / Android)
*An app people install from the App Store / Google Play.*
- **Framework:** for a non-techie → a **no-code builder** (FlutterFlow/Adalo, ~$30–70/mo — they handle
  app-store submission) or a **PWA** (free — a website that installs to the home screen, no store
  review); if coded → **React Native + Expo** or **Flutter** (free, one codebase → both stores).
- **Database:** **Supabase** or Firebase (managed) — keep it.
- **Distribution:** App Store (~$99/yr) + Google Play (~$25 one-time); or PWA (no store, no fees).
- **Wrong when:** Streamlit/Vercel don't ship native apps; coded RN/Flutter needs a real developer;
  PWA can't be in the App Store.

## 7. AI / LLM app (chatbot, agent, "chat with my docs")
*An app with AI inside that reads/writes language. (Run the AI-inside check first.)*
- **Language:** Python (free).
- **Framework:** **Streamlit** for a data app *around* AI; **Gradio** or **Chainlit** (free) for a pure
  chat window (they handle token streaming Streamlit fumbles).
- **LLM approach:** call the **Claude API directly** (pay-per-use) — plain prompt-to-API. **Skip
  LangChain** until you genuinely need multi-step agents (it adds debug-killing abstraction for a
  beginner; Anthropic itself says start simple).
- **Database / vector store (only if RAG):** **Supabase + pgvector** (cheap; RAG = letting the AI look
  things up in your documents before answering); pay-for-better at huge scale → **Pinecone** (managed,
  auto-scales past tens of millions of items).
- **Hosting:** **Streamlit Community Cloud** (Streamlit) / container host (Gradio/Chainlit). **Not
  Vercel for Streamlit** — Vercel only for a Next.js/React frontend that calls a separate API.
- **Wrong when:** a pure chatbot on Streamlit (full reload breaks streaming) → Gradio/Chainlit; reaching
  for LangChain on day one → start with a plain API call. Route the agent design to `agent-architect`.

---

## 8. Other / advanced / doesn't fit — the escape hatch

When a request matches none of the 7 rows (e.g. "an AI OS", a desktop assistant that controls the
machine, a real operating system, anything exotic), **do NOT invent a confident default.** Instead:
1. **Clarify** what it actually is (the term may hide very different builds).
2. **research-scout** the specific thing (cited, current evidence).
3. **Reality-check scope with `/discover`** — is it solo-buildable, or a team/years effort?
4. **If AI-heavy → `agent-architect`** for the agent design.

Worked example — **"AI OS"** covers three very different builds:
- **A real OS with AI baked in** — systems languages (C/Rust), kernel + drivers, teams/years. *Not* a
  boring/proven solo project — say so honestly.
- **An "AI operating layer" / agent platform** (usual meaning) — really an ambitious AI app: Python/TS +
  an agent-orchestration framework + Claude API + Supabase + integrations + a normal web host. Maps onto
  row 7 at its high end; `agent-architect` essential.
- **A desktop assistant that controls the computer** — a desktop shell (Electron/Tauri or Python) +
  Claude API + OS-automation libraries + serious permission/security care.
