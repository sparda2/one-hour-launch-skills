---
name: winning-ads-creator
description: Winning Ads Creator — full daily creative pipeline for Meta Ads. For each product in your master Google Sheet it researches the best advertisers in the world via the Ad Library API (zero browser), creates 5 new AI image ads modeled on real winners, audits them one by one and delivers them to your Google Drive with links in the sheet. Includes a guided first-time setup that takes anyone from "I just installed this" to their first 5 ads. Use when the user says 'winning ads creator', 'create my ads', 'the ads routine', 'run the routine', 'regenerate the ads', 'set up the winning ads creator', uploads this skill and asks to set it up, or asks for the 5 ads of a product.
---

> Version 2 of the routine (Aug 4, 2026): 100% API research, winners bank,
> visual agent and cost discipline — all measured in real production.

# WHERE EVERYTHING LIVES — the person's Google Drive

Nothing is kept on the computer running this skill (cloud sessions are wiped
when they end). Everything lives in a Drive folder called
**"Winning Ads Creator"**:

```
Winning Ads Creator/
├── Winning Ads Creator — Master   (Google Sheet, tabs below)
├── Ads/<PRODUCT>/<YYYY-MM-DD>/AD01.jpg … AD05.jpg
├── Research/<PRODUCT>_<DATE>.md
└── Winners/<PRODUCT>/…            (winner creatives seen by the VISUAL agent)
```

| Tab | What it holds |
|---|---|
| Products | PRODUCT \| PRODUCT LINK (landing) \| LANGUAGE \| RESEARCH LINK \| CREATIVES LINK — one row = one product |
| Settings | setting \| value \| last updated — the person's answers + the setup checklist |
| My Rules | rule \| added on — the person's own extra rules |
| Winners Bank | date \| product \| advertiser \| page_id \| ad link \| duplications \| days running \| hook \| visual description \| spatial formula \| text position \| transcription |
| Concepts Log | date \| product \| AD# \| winner modeled \| formula \| funnel level \| headline \| 2 alternates |
| Landings Cache | product \| landing URL \| verified figures \| guarantee \| hero mockup URL \| real headlines \| verified on |
| Run Log | date \| product \| stage \| agent-minutes \| notes (cost rule 5) |

**Two ways data moves (both cheap):**
- **Tables** (tabs above) → the Google Sheets / Google Drive connector. Read
  only the rows you need (e.g. the bank rows of this product's niche).
- **Files** (JPGs, reports) → NEVER through the chat (an image as text costs
  a fortune). They go through the person's **Drive uploader** with
  `assets/drive_sync.py` (next to this file), run with
  `UPLOADER_URL` / `UPLOADER_TOKEN` exported from the Settings tab.
  Local alternative: on a computer with Google Drive for desktop, write files
  straight into the synced "Winning Ads Creator" folder instead.

**`_assets/` = the local working folder of ONE run.** At the start of a run,
hydrate it from Drive: bank rows → `_assets/bank.md`, Landings Cache →
`_assets/landings_cache.json`, Concepts Log → `_assets/concepts.md`,
yesterday's 5 ads of each product → `_assets/yesterday/<PRODUCT>/`
(`drive_sync.py pull`). The cost rules' "handoff through disk" happens here.
At the end, persist back (STEP 6).

**Finding it in a new session:** search Drive for the exact name
"Winning Ads Creator — Master". One match → use it. Several → ask which.
None → first-time setup. Never create a second master sheet.

This skill has NO config block to edit. This skill is the canonical source of
the routine: scheduled runs only point at it. Editing the routine = editing
this file.

# GUIDED SETUP — from "I just installed this" to the first 5 ads

Run this section FIRST whenever there is no master sheet yet, or its Settings
tab doesn't say `Setup = complete`, or the person asks to set up / repair the
Winning Ads Creator. Once setup is complete, skip straight to STEP 0.

**How to guide (non-negotiable):**
- Talk in the person's language. Assume they are NOT technical: one action at
  a time, exact click paths, what they will see, and how to tell it worked.
- CHECK before asking: detect everything you can yourself (tools, network,
  environment variables). Only ask for what you can't detect or do.
- Batch every fix that needs a NEW session into ONE restart (connectors,
  network and environment variables only load when a session starts).
- Show progress each turn as a short checklist: ✅ done, 👉 now, ⬜ next.
- Never ask for passwords, tokens or API keys in the chat. Keys go into the
  environment's variables (see S2), never into the sheet or the chat.

**S1 — Detect what's missing (all at once).** Search the available tools
(including deferred tools / tool search) and test:
- **Meta Ad Library tool** (e.g. `ads_library_search`). Missing → ❌ Meta.
  Run one canary query ('shoes', US, active). An error about the ad account →
  ❌ Ad account (Meta only opens the Ad Library tool to people with at least
  one ACTIVE ad account).
- **Google Drive** tools (search, create files) AND **Google Sheets** tools
  (read/write cells) — TWO separate connectors. Either missing → ❌ Drive /
  ❌ Sheets.
- **Network (Claude Code cloud session, `echo $CLAUDE_CODE_REMOTE` = true):**
  curl `https://gumroad.com`, `https://www.google.com` and
  `https://script.google.com`. Blocked (proxy 403 / "EGRESS_BLOCKED") →
  ❌ Network. ⚠️ Don't test with facebook.com: Facebook answers 403 to every
  script even with Full network — normal; the Ad Library is read through the
  Meta connector.
- **Headless browser** for the VISUAL agent: `python3 -c "import playwright"`
  and a Chromium binary. Missing → install it yourself (`pip install
  playwright`; use the pre-installed Chromium if present, else `playwright
  install chromium`). Only ask if that fails.
- **Image engine:** ask ONE question (AskUserQuestion when available): which
  image generator will they use? Offer: an image API they already pay for
  (e.g. OpenAI images, Google Gemini/Imagen, fal.ai, Replicate — the most
  powerful they have, max resolution, 1:1, ideally accepting a reference
  image for their product mockup), a CLI, or a connector. For an API, check
  its key exists as an environment variable (e.g. `OPENAI_API_KEY`,
  `GEMINI_API_KEY`, `FAL_KEY`, `REPLICATE_API_TOKEN`) — test `[ -n "$NAME" ]`,
  never print it. Missing → ❌ Key. Warn: a connector that returns images
  into the chat is expensive (cost rule 2) — prefer an API.
- **The skill itself** shows up as an installed skill (not only an uploaded
  file). Not installed → ❌ Install.

**S2 — Fix everything in ONE round, then ONE restart.** One numbered list
with only the ❌ items:
- ❌ Install → claude.ai → Settings → Capabilities → Skills → "Upload skill"
  → choose the skill's ZIP (from the pack). Installed skills are available in
  the Claude app AND in Claude Code cloud sessions of the same account.
- ❌ Meta → claude.ai → **Customize → Connectors**
  (claude.ai/customize/connectors) → **+** → **Add custom connector** →
  Name: `Meta` → URL: `https://mcp.facebook.com/ads` → **Add** → **Connect**
  → log in with the Facebook account that manages their ad account → approve
  ALL the permissions it asks for → "Connected".
- ❌ Ad account → business.facebook.com → create or reactivate an ad account
  (it must be active; a payment method is usually required).
- ❌ Drive / ❌ Sheets → same Connectors page → **Google Drive** → Connect →
  Allow; then **Google Sheets** → Connect → Allow.
- ❌ Network → in the Claude Code session title bar, environment menu → Edit →
  Network access → **Full** → Save.
- ❌ Key → get the API key from the provider's dashboard → in the same
  environment Edit screen, add it under **Environment variables** as
  `NAME=key` (e.g. `OPENAI_API_KEY=…`) → Save. Never paste it in the chat.
Then tell them to start a NEW session (Claude desktop app → Code → Cloud, or
claude.ai/code) and send the resume message (S9). If nothing is ❌, skip it.

**S3 — Verify after the restart.** Re-run S1. Anything still ❌ → the most
likely cause in one line and the one fix. Don't continue until Meta, Drive
and the image engine all work.

**S4 — Create the home.** Search Drive for "Winning Ads Creator — Master".
None → create the "Winning Ads Creator" folder (Drive connector, folder mime
type) and the master sheet inside it with the 7 tabs and header rows (bold,
colored, frozen, filters on). Read the headers back. Give them the link.

**S5 — The Drive uploader (one time, ~3 minutes).** Explain in one line why:
"so your ad images go straight to your Drive without costing tokens".
1. Generate a random 32-character token (letters + digits).
2. Read `assets/drive-uploader.gs`, fill in ROOT_FOLDER_ID (the "Winning Ads
   Creator" folder id) and TOKEN, and give them the full code in one block.
3. Guide: script.google.com → **New project** → select all, paste → name it
   "Winning Ads Creator uploader" → 💾 Save → **Deploy → New deployment** →
   ⚙️ type **Web app** → Execute as **Me** → Who has access **Anyone** →
   **Deploy** → **Authorize access** → choose their account → if Google says
   "Google hasn't verified this app": **Advanced → Go to … (unsafe)** → Allow
   (it's their own script) → copy the **Web app URL** and paste it here.
4. Save UPLOADER_URL and UPLOADER_TOKEN in the Settings tab (the sheet is
   private; tell them not to share it).
5. Test: `drive_sync.py ping`, then upload a tiny test file to `Ads/_test`,
   list it, pull it back. All ok → ✅. Failing → most common causes: access
   not set to "Anyone", or they copied the editor URL instead of the /exec URL.
On a local computer with Google Drive for desktop, offer to skip S5 and save
files straight into the synced folder.

**S6 — Products.** Ask for their products (or import from the Winning Offer
Spy sheet if they want): for each, the name, the landing page URL and the ad
language. Write them to the Products tab. Open each landing ONCE: confirm it
loads, and fill the Landings Cache (real figures, guarantee, hero mockup URL,
real headlines — STEP 5 rule 5).

**S7 — Settings.** Run STEP 0 → "How to get the settings" (at most 2
rounds). OWN_PAGES: reuse the Winning Offer Spy's if its master sheet exists
(confirm), else ask (page_id: Ad Library → search their page → click it →
the URL shows `view_all_page_id=NUMBER`). NICHE_RULES: ask their niche and
propose the rules for it.

**S8 — Smoke test (before the real run).**
- Image engine: ONE cheap, small generation from a simple prompt → save →
  upload to `Ads/_test/` → give them the link to look at → ✅.
- Meta: the canary from S1 already passed.
Write `Setup = complete` in Settings, then say: "Setup done. Creating your
first 5 ads now for <ONE product> (≈ DEADLINE). You can close this window —
it keeps running in the cloud." and go to THE ROUTINE with
PRODUCTS_THIS_RUN = that ONE product (first run: always one product).

**S9 — Resume message (give it whenever a restart is needed):**
`Continue setting up the Winning Ads Creator from where we left off.`
(The checklist lives in the Settings tab. If the skill isn't installed yet,
they attach the skill file to that message.)

**After the first run:** ask them to look at the 5 ads with their own eyes:
perfect text? professional photography or template look? does every figure
exist on their landing? does it look like a real winner or generic? Every
"I don't like X" → offer to add it to the My Rules tab (that's how the
original routine was built: through rejections). Repeat with that product for
2-3 days; when it comes out well without touching anything, add the rest of
the products. Offer the daily scheduled run (unattended) only after that.

# STEP 0 — RUN SETTINGS (ask, never assume)

## The settings (stored in the Settings tab)

| Setting | What it is | Default if the person doesn't care |
|---|---|---|
| PRODUCTS_THIS_RUN | Which Products rows to run | All rows (first run: ONE product) |
| IMAGE_ENGINE | The most powerful AI image generator available, how to call it (API + env variable name, CLI command, or connector), max resolution, 1:1 | **None — must be asked** |
| ENGINE_LIMITS | The image plan's simultaneous job limit — enforced with a semaphore, not by launching fewer | Ask; 4 if unknown |
| OWN_PAGES | The person's own pages, EXCLUDED from competitor research | From the Winning Offer Spy sheet if it exists; else ask |
| NICHE_RULES | Compliance by niche: health = no medical claims or dosages; money = no income promises; etc. | No medical claims, dosages, income promises, before/after or invented ratings |
| TOP_MODEL | The most powerful Claude model on the plan — ONLY where design happens: director+critic and repairer | The most capable model available |
| ECO_MODEL | An economical model — research, generation, audit and the orchestrating session | A Sonnet-class model |
| DEADLINE | Delivery cutoff. Whatever doesn't make it is reported with its cause — the run is not stretched | 1 hour after start |
| UPLOADER_URL / UPLOADER_TOKEN | The Drive uploader (S5) | Set by the setup |

## Personal rules

Read the My Rules tab before starting and apply every rule in it as an extra
HARD rule for this run. It is how the person adds their own lessons without
editing this skill (updates of the pack would overwrite edits here). If a
personal rule contradicts a rule of this skill, follow the personal rule and
mention it in the final summary. When the person rejects something and states
a rule, offer to add it to the My Rules tab.

## How to get the settings

1. **Settings in the invoking message win.** E.g. `/winning-ads-creator only
   for <PRODUCT>` → PRODUCTS_THIS_RUN is set; don't ask it again.
2. **Interactive run (a person is in the chat):**
   - Settings tab filled → show the saved settings as one compact table and
     ask ONE question: "Run with these, change some, or start fresh?"
   - First time → ask the missing settings in AT MOST 2 rounds
     (AskUserQuestion for choice-type ones, plain chat for free text), with
     an example for each and the defaults offered.
   - Then print the final settings table and START (no extra confirmation).
3. **Unattended run (scheduled task, Grok Bot, headless `claude -p`, or the
   message says "unattended"):** NEVER ask. Use the message, then the
   Settings tab, then defaults. If the master sheet, the Products tab rows,
   IMAGE_ENGINE or the uploader are missing: STOP without running and print
   what is missing plus an example command that includes it.
4. **Save** the final settings to the Settings tab (with today's date).
5. **Pre-flight (every run):** Meta tool, Sheets read/write,
   `drive_sync.py ping` and the image engine's key must all work BEFORE the
   pipeline starts. If any fails, STOP and say exactly what to fix (S1-S2) —
   never generate ads that can't be delivered.

# THE ROUTINE

Run the FULL pipeline every run: EVERYTHING is regenerated every day, all the
products in PRODUCTS_THIS_RUN, and the new ads must be DIFFERENT from yesterday's.
Core philosophy: **MODEL THE BEST ADVERTISERS IN THE WORLD — never reinvent
the wheel.** The creativity is in the faithful ADAPTATION to your product.
Report short, results, zero theory.

## THE 5 COST RULES (measured in production — breaking them multiplies the bill)

1. **THE HANDOFF GOES THROUGH DISK, NOT CONTEXT.** Each agent writes its FULL
   result to a file in `_assets/` and returns ONE line to the chat. The next
   agent READS the file. Never paste one agent's content into the next one's
   prompt: you pay the same 4 times, and summarizing loses the winner's light,
   framing and text position.
2. **AN IMAGE IN CONTEXT IS RE-CHARGED EVERY TURN.** The approximate cost is
   (width × height) / 750 tokens, and it's paid again on every later turn of
   the agent that opened it. So: audit on small copies (~768px), open each
   image ONCE, and never put a 4K image into context. Don't raise the audit
   resolution without proof that a real defect is invisible at 768 — almost
   always the problem is the checklist, not the resolution.
3. **RESEARCH VIA API, ZERO BROWSER.** The browser with screenshots is the
   most expensive thing in the whole pipeline (measured: it cost several times
   more than the design). The Ad Library API gives the signal for almost
   nothing. The browser is only used for the one thing the API doesn't give:
   SEEING a specific creative — and the cheap way (see VISUAL agent).
4. **IF THE RUN DIES HALFWAY, IT IS NOT RELAUNCHED WITHOUT ASKING.** Relaunching
   repeats the expensive stages already paid for (research and direction). The
   right move: STOP, say what failed and how much repeating it would cost, and
   wait for an answer. If the owner isn't around: deliver what exists and report.
5. **MEASURE BEFORE DIAGNOSING.** When the routine is slow or expensive, get the
   real breakdown by stage (agent-minutes and cost) before touching anything.
   In our measurement research was 51% of the clock and 73% of the spend — and
   intuition blamed image generation, which was NOT the bottleneck.

## STEP 1 — Read the source of truth

Read the Products tab of the master sheet (Google Sheets connector). Each row
= one product with its landing and its language. New product (row without a
folder in the Drive `Ads/` folder) →
create its folder and run the full pipeline for it.

## STEP 2 — API research (all products, every day)

**FORBIDDEN to open the browser to explore the library.** All research goes
through the Ad Library API (`ads_library_search` from the Meta connector), in
TWO PASSES — because keyword search has a results cap and doesn't paginate, so
its counts are only a FLOOR:

1. **Discovery pass**: 3-5 niche keywords → identify 6-8 candidate `page_id`s
   (who is running ads on the topic).
2. **Measurement pass**: one call PER `page_id` — there the total count IS the
   advertiser's real size and duplication is counted exactly (same
   title/creative repeated in N ads = what that advertiser SCALES).

From each candidate the API gives you what's FRESH: who is scaling TODAY, how
many duplications, days running and the literal hook. Signals: ≥3
duplications interesting, ≥8 clear winner, ≥15 brutal; months running =
winner even without duplications. ALWAYS EXCLUDE your OWN_PAGES.

**THE BANK — your accumulated asset.** The API gives signal but NOT images. The
visual formula comes from your BANK: previous research reports
(`_assets/research/`, pulled from Drive `Research/`) and the Winners Bank tab,
where every winner SEEN was deconstructed (visual description, spatial
formula, transcription, hook). Research cross-checks each API candidate against
the bank and marks it **BANK: yes / no**:
- BANK: yes → fresh signal + verified visual structure. The best ones to model.
- BANK: no → goes to the VISUAL agent (step 2.5) to see it ONCE and add it to the bank.
**Never invent a visual description of something that wasn't seen.** The bank
starts empty: your first 1-2 weeks the visual agent works harder; after that
almost everything comes out BANK: yes. It's an investment, not a recurring cost.

Research writes its report to `_assets/research/<PRODUCT>_<DATE>.md` and
returns one line. Sets in other languages of the SAME product don't research
separately: they adapt the main sibling's report without softening it.

## STEP 2.5 — VISUAL agent: see the new winners (the cheap way)

Runs ONLY if research marked BANK: no winners. Its only job is to SEE those
ads — without photographing the screen:

1. Open the link of the SPECIFIC ad in the library (its snapshot), not the
   general search. The library serves the creative without login.
2. **ZERO screenshots.** Extract the creative's image URL from the DOM (the
   largest `<img>` from Facebook's CDN) with a single JavaScript call.
3. Download the JPG to `_assets/winners/<PRODUCT>/` with curl.
4. Open it with Read and deconstruct it: shot type, light, objects, WHERE the
   text lives, palette, people/hands/faces, spatial formula in one line,
   transcription. That goes to the bank → tomorrow that winner is BANK: yes.

Why this way: a ~600px JPG is ~480 tokens; a full-page screenshot ~2,000 and
it's re-charged every turn. Plus you get the ad's ORIGINAL FILE, not a photo of
a screen. Hard rules: max 5 winners per product; screenshot/zoom/reading the
whole page forbidden; if there are several visual agents, the browser goes ONE
AT A TIME (they share a tab and step on each other; parallel also triggers the
library's rate-limit).

**Director's rule:** if there were winners seen today, ONE of the 5 ads MUST
model a winner seen today — modeling its STRUCTURE, never copying its text or
its brand.

## STEP 3 — The agent chain per product

- **RESEARCH** (ECO_MODEL): two-pass API + cross-check against bank → report to
  disk. If it brings <5 usable winners, THAT research is repeated with TOP_MODEL.
- **VISUAL** (ECO_MODEL): only BANK: no → download and deconstruct (step 2.5).
- **DIRECTOR+CRITIC** (TOP_MODEL): reads the report FROM DISK (in full, not a
  summary) and designs the 5 ads AND self-attacks with the adversarial
  checklist in the same pass: hook softness, cover test, perfect language,
  compliance, fidelity to the winner's formula, safe zone, generability (texts
  quoted in exact quotes; props with text REMOVED). Writes
  `spec_<PRODUCT>.json` with: modeled winner, formula, funnel level, chosen
  headline + 2 alternates, EXACT overlay texts and the final prompt.
- **GENERATION** (mechanical): runs the IMAGE_ENGINE with the spec's 5 prompts.
  Respects ENGINE_LIMITS with a shared semaphore (so all products can run in
  parallel without inventing "waves" or manual batches).
- **AUDITOR** (ECO_MODEL): looks at the 5 as a ~768px copy, ONCE each. The
  format matters: **5 fixed questions per ad** (what visual proof of the
  product does it contain? is the text perfect and in the right language? is
  there an identifiable face, a price or a button? does it respect the
  winner's formula? does it speak to the real buyer?) + 1 VARIETY check of the
  full set (are the 5 different from each other and from yesterday's?). A free
  12-point checklist gets skimmed; 5 fixed questions don't. When in doubt,
  reject. If the verdict comes back with ZERO approved, repeat the audit ONCE
  (usually a sign of a race with generation: folder still empty) — and mark
  "not delivered" if a file is missing, instead of inventing a verdict.
- **REPAIRER** (TOP_MODEL, only if there are rejections): fixes THE CONCEPT in a
  single batch. FORBIDDEN to approve an ad without opening its image with Read.

All handoffs between agents go through disk (COST RULE 1). The main session
only orchestrates — and does its own **SPOT-CHECK**: before reporting, it opens
1-2 audit copies per product and looks at them. Nothing is declared delivered
without a pair of eyes having seen it — the day nobody looked, garbage was
delivered with a green verdict. Audit copies go in a folder BY DATE
(`_assets/audit/<PRODUCT>/<DATE>/`): with a flat folder, a product whose
generation fails keeps YESTERDAY's copies and the auditor approves them as if
they were today's.

## STEP 4 — Creative direction (the rules of the craft)

- **The set of 5 is a MINI-FUNNEL**: AD1 hidden pain the reader thinks is
  normal; AD2 validates the pain + hints at the way out (a DIFFERENT sub-pain);
  AD3 transformation achieved; AD4 unique mechanism / legitimate proof; AD5
  direct sale (CTA + guarantee + "instant download", NO price). Flexible map;
  the full set covers cold to hot.
- **Each ad models a different REAL winner** from the bank/research. Forbidden
  to repeat the previous day's winner, formula or structure (look at
  yesterday's and the concept log before directing).
- **Headlines — 3 candidates + the cover test**: different formats (question
  that hurts / soft accusation / mistake / revelation / confession / number);
  printed on a magazine competing with 20 others, does the reader pick it up?
  Max 8-10 words; brutal specificity; talks about the reader, not the product.
  The 2 alternates are logged (they're useful for the copy).
- **Cross-language**: the king signal is WORLDWIDE duplication, not the
  language. Sets in other languages model the TOP ones from any language and
  are adapted WITHOUT softening: the hook must match the original's voltage.
  "Soft" = rejection.
- **Mockups — NO quota**: if the modeled winner has a product in frame, that
  product is YOURS (official mockup from your landing as the generator's
  reference — never blank, generic or invented; and never the shortcut of
  putting text on top of it). If the winner has no product, don't force it in.
  Adapt to what you find, like a great designer.

## STEP 5 — Hard generation rules (breaking them = redo)

1. ALL visible text in the language of the Sheet row, perfect.
2. ZERO prices, currency symbols, %, strikethroughs or "value".
3. **PEOPLE — calibrated rule**: hands and bodies YES. What's forbidden is the
   **IDENTIFIABLE FACE**: a sharp, in-focus face with weight in the
   composition (an AI face gives the ad away). These DO pass — and are good
   design — the backlit silhouette, the face in shadow, the profile in
   half-light, the face blurred by depth of field and the small, distant
   figure. Don't be more extreme than this: the hard version ("if an eye is
   visible, out") costs good photography and gains nothing. (Possible
   exception: a product where the face IS the product — there it goes with a
   visible AI disclosure.)
4. No fabricated scarcity, no medical claims, no unverifiable social proof.
   Allowed: launch offer / instant download / lifetime access / real
   guarantee / imperative CTA.
5. **TRUTHFUL NUMBERS + LANDINGS CACHE**: every figure (counts, guarantee) is
   verified against the real landing ONCE and cached in
   `_assets/landings_cache.json` (counts, guarantee, hero mockup, real
   headlines). Following runs use the cache — only re-verified if the owner
   says they touched a landing. Use your landings' REAL headlines and copy in
   the briefs: they're better than invented ones. If a figure can't be
   verified, it goes without a figure.
6. **TEMPLATE LOOK FORBIDDEN**: no button, pill or badge (the CTA is ONE line
   of plain text); the headline-top/subtitle/button skeleton is banned (max 1
   of 5 with headline on top); the headline lives INSIDE the space the photo
   already has; photography with real light and concrete direction; the 5
   different from each other (framing, time of day, text position, formula).
7. **Props with text are REMOVED from the prompt** (rulers, tabs, spines,
   screens): asking for "blur" isn't enough, you get broken letters. The
   product's small text goes out of frame or heavily blurred; NEVER redraw it.
   And the rules go INTEGRATED into the prompt's description, never as a
   final list ("no gibberish, no faces") — the model prints it inside the ad.
8. **ANTI-SHORTCUT RULE**: forbidden to solve a technical problem by removing
   the element that sells. If something can't exist without breaking, THE
   CONCEPT CHANGES. Every frame needs VISUAL PROOF (recognizable product,
   mechanism or result) and must speak to the REAL buyer. Blank cover, empty
   page or mute prop = rejection even if it's "clean".
9. **Compliance sweep** on the visible text before generating (regex per
   NICHE_RULES): dosages, cure/treat, lose weight, before/after, "only N
   left", invented ratings. The fix keeps the voltage: move the hero from the
   forbidden term to the criterion/mechanism.
10. SAFE ZONE in every prompt: compose headline and key elements in the center
    so the 1:1 works cropped to 9:16 (works for Stories without regenerating).

## STEP 6 — Delivery

JPG at NATIVE resolution (no rescaling, quality ~95) as AD01.jpg…AD05.jpg in
`_assets/out/<PRODUCT>/<YYYY-MM-DD>/`. Verify resolution and FRESHNESS (JPG's
mtime ≥ its source's mtime — an old JPG passes the size check). Then upload
each one to Drive `Ads/<PRODUCT>/<YYYY-MM-DD>/` with `drive_sync.py upload`
and check every upload returned ok (a failed upload = "not delivered", never
"delivered"). Don't delete previous days' folders. Write the Drive folder link
in the Products tab's CREATIVES LINK column, and the research report's Drive
link (upload `_assets/research/<PRODUCT>_<DATE>.md` to `Research/`) in
RESEARCH LINK.

**Save the memory (same step, every run):** append the new deconstructed
winners to the Winners Bank tab, the 5 concepts to the Concepts Log, any
new/changed landing data to the Landings Cache, and the per-stage
agent-minutes to the Run Log. Upload new winner JPGs to `Winners/<PRODUCT>/`.
Tomorrow's run hydrates from these — skipping this step makes tomorrow repeat
today and re-pay the VISUAL agent.

## STEP 7 — Final summary

Per product: the day's winners (advertiser + duplications + BANK yes/no), the 5
ads indicating WHICH WINNER each one models and how they differ from yesterday,
folder path, and the spot-check result. Honest about what failed and what was
left outside the DEADLINE (with its cause).

## SCALING — from sequential to scripted (once it's stable)

Start SEQUENTIAL: one product end to end, then the next. Every systematic
failure detected gets fixed in the template BEFORE the next product (the error
is paid once, not N times). When the routine has been stable for 1-2 weeks, ask
your Claude to SCRIPT it: a pre-script that regenerates the data per product,
and a Workflow that runs ALL products in parallel (research → direction →
generation → audit → repair → delivery) with the generator's semaphore and the
DEADLINE per stage. Rules of scripted mode: the agents' prompts live WRITTEN in
the script (not drafted every morning); no inventing manual batches; and if the
pipeline needs to change, the script is changed COLD, the reason is written
down, and it runs the next day. The routine is not redesigned every morning.
