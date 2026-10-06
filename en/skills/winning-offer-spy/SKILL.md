---
name: winning-offer-spy
description: Winning Offer Spy — hunts offers that are scaling right now in Meta's Ad Library according to your format filter, and logs them with their history in a master Google Sheet in your Google Drive (settings, keyword bank and your rules live there too). Includes a guided first-time setup that takes anyone from "I just installed this" to their first hunt. Use when the user says 'winning offer spy', 'spy on winning offers', 'hunt offers', 'find scaling offers', 'set up the Winning Offer Spy', uploads this skill and asks to set it up, or asks for the master sheet sweep.
---

# WHERE EVERYTHING LIVES — one Google Sheet in the person's Drive

Nothing is stored on the computer running this skill (cloud sessions are
wiped when they end). EVERYTHING lives in ONE Google Sheet called
**"Winning Offer Spy — Master"**, in a Drive folder called **"Winning Offer Spy"**:

| Tab | What it holds |
|---|---|
| Offers | The verified offers (see "Update the master sheet") |
| Pending | Promising but unverified / under threshold + 💡 gaps |
| History | date \| ID \| product \| ads today |
| Search Log | date \| keywords used \| useful results (+ each run's start time) |
| Keywords | keyword \| category \| language \| circle \| angle \| status (new / hot / burned) — the KEYWORD BANK |
| Settings | setting \| value \| last updated — the person's answers + the setup checklist |
| My Rules | rule \| added on — the person's own extra rules |

**Finding it in a new session:** search Drive for the exact name
"Winning Offer Spy — Master". One match → use it. Several → ask which one. None →
first-time setup. Never create a second master sheet.

This skill has NO config block to edit. This skill is the canonical source of
the routine: scheduled runs only point at it. Editing the routine = editing
this file.

# GUIDED SETUP — from "I just installed this" to the first hunt

Run this section FIRST whenever there is no master sheet yet, or its Settings
tab doesn't say `Setup = complete`, or the person asks to set up / repair the
Winning Offer Spy. Once setup is complete, skip straight to STEP 0.

**How to guide (non-negotiable):**
- Talk in the person's language. Assume they are NOT technical: one action at
  a time, exact click paths, what they will see, and how to tell it worked.
- CHECK before asking: detect everything you can yourself (tools, network).
  Only ask the person for what you can't detect or do.
- Batch every fix that needs a NEW session into ONE restart (connectors and
  network changes only load when a session starts). Never make them restart
  twice if one restart could do it.
- Show progress each turn as a short checklist: ✅ done, 👉 now, ⬜ next.
- Never ask for passwords, tokens or API keys in the chat.

**S0 — This MUST run in Claude Code, not in the regular Claude chat.**
The spy has to open every competitor's landing page (mandatory
verification), run long and save its work — only Claude Code can. Check: do
you have a shell/Bash tool? No → you are in the regular Claude chat: STOP and
tell them: "Open the Claude desktop app → **Code** → choose **Cloud** (or go
to claude.ai/code), start a new session and send: *Set up the Winning Offer
Spy for me step by step.*" Nothing else works from the regular chat.

**S1 — Detect what's missing (all at once).** Search the available tools
(including deferred tools / tool search) and test:
- **Meta Ad Library tool** (`ads_library_search`). Missing → ❌ Meta.
  Present: run one canary query ('shoes', US, active, limit 2). It returns
  results with an `estimated_total_count` → ✅. An error about the ad
  account → ❌ Ad account (Meta only opens the Ad Library tool to people with
  at least one ACTIVE ad account).
- **Google Drive** tools (search, create files) AND **Google Sheets** tools
  (read/write cells). They are TWO separate connectors. Either missing →
  ❌ Drive / ❌ Sheets.
- **Network (cloud session, `echo $CLAUDE_CODE_REMOTE` = true):** curl
  `https://gumroad.com` and `https://www.google.com`. Both 200 → ✅. Blocked
  (403 from the proxy / "EGRESS_BLOCKED") → ❌ Network.
  ⚠️ Do NOT test with facebook.com: Facebook answers 403 to every script even
  with Full network. That is normal and harmless — the Ad Library is read
  through the Meta connector, not the network.
- **The skill itself** is installed for next time: it shows up as an
  available skill (not only as an uploaded file in this chat). If it was only
  uploaded → ❌ Install.

**S2 — Fix everything in ONE round, then ONE restart.** One numbered list
with only the ❌ items, using these exact steps (tested end to end):
- ❌ Install → claude.ai → **Settings → Capabilities → Skills** → "Upload
  skill" → choose the skill's ZIP file (from the pack). Skills uploaded there
  are available in the Claude app AND in Claude Code cloud sessions of the
  same account.
- ❌ Meta → claude.ai → **Customize → Connectors**
  (claude.ai/customize/connectors) → **+** → **Add custom connector** →
  Name: `Meta` → URL: `https://mcp.facebook.com/ads` → **Add** → **Connect**
  → log in with the Facebook account that manages their Business / ad
  account → approve ALL the permissions it asks for (ads, business, pages)
  → it shows "Connected".
- ❌ Ad account → business.facebook.com → Business settings → Ad accounts →
  create or reactivate one (it must be ACTIVE; Meta usually asks for a
  payment method). Then disconnect/reconnect the Meta connector so it sees it.
- ❌ Drive / ❌ Sheets → same Connectors page → **Google Drive** → Connect →
  their Google account → Allow. Then **Google Sheets** → Connect → Allow.
- ❌ Network → in the Claude Code session title bar, open the environment
  menu → **Edit** → Network access → **Full** → Save. (Applies to sessions
  started after saving.)
Then tell them to start a NEW session (Claude desktop app → Code → Cloud, or
claude.ai/code), check in that session's connector menu that Meta, Google
Drive and Google Sheets are switched ON, and send the resume message (S7).
Tip: pick the **Auto** permission mode for the session so the 20-40 minute
hunt doesn't stop to ask for approvals. If nothing is ❌, skip the restart.

**How they can check it themselves (give them these prompts):**
- `Do you have access to ads_library_search?` → should say yes.
- `Run a test search in the Ad Library: "shoes", US, active ads.` → should
  show ads and an estimated total count.
- `Open https://gumroad.com and tell me its title.` → should work.

**S3 — Verify after the restart.** Re-run S1. Anything still ❌ → explain the
most likely cause in one line (e.g. "the connector was added after this
session started") and the one fix. Don't continue until Meta AND Drive work
(no Meta = no hunt; no Drive = nowhere to save).

**S4 — Create the home.** Search Drive for "Winning Offer Spy — Master". None →
create the "Winning Offer Spy" folder and the master sheet inside it with the 7
tabs and their header rows (bold, colored, frozen, filters on). Read the
headers back to confirm the write worked. Give the person the link.

**S5 — Settings.** Run STEP 0 → "How to get the settings" (first-time
questions, at most 2 rounds) and save the answers in the Settings tab. Help
sharpen YOUR_FILTER and NICHE_CIRCLES if vague; never invent them. For
OWN_PAGES, show how to find a page_id (Ad Library → search their page →
click it → the URL shows `view_all_page_id=NUMBER`) or look the names up with
the Meta tool and confirm with them.

**S6 — Smoke test (2 minutes, before the real hunt).**
- Meta: one canary query (e.g. 'shoes', US, active). Results > 0 → ✅.
- Keywords: generate the KEYWORD BANK into the Keywords tab (STEP 0 → 5).
Write `Setup = complete` in the Settings tab, then say: "Setup done. Starting
your first hunt now (20-40 min). You can close this window — it keeps
running in the cloud." and go to THE ROUTINE.

**S7 — Resume message (give it whenever a restart is needed):**
`Continue setting up the Winning Offer Spy from where we left off.`
(The checklist lives in the Settings tab, so the new session picks up there.
If the skill isn't installed yet, they attach the skill file to that message.)

**After the first hunt:** ask them to check 2-3 findings by hand (library
link: really that many active ads? landing: really a downloadable product with
direct checkout?). If the finds don't fit what they can make, their filter is
loose → offer "change some" and tighten it. Finally, offer the daily scheduled
run (unattended mode) — only once 2-3 runs have convinced them.

# STEP 0 — HUNT SETTINGS (ask, never assume)

## The settings (stored in the Settings tab)

| Setting | What it is | Default if the person doesn't care |
|---|---|---|
| YOUR_FILTER | The product format the person can replicate. Only what passes it gets logged. E.g. "low-ticket downloadable digital toolkits (PDF guides, templates, prompt packs) I can produce with AI in days; no video courses, coaching or services" | **None — must be asked** |
| NICHE_CIRCLES | Circle 1 = current niches; 2 = same buyer, other topics; 3 = adjacent. 3-5 each. The hunt goes in that order | **None — must be asked** |
| OWN_PAGES | The person's own Facebook pages (names or page_ids), EXCLUDED from the hunt | Ask; "none" only if the person says so |
| LANGUAGES | Languages to search in | All languages, English first |
| MIN_ADS | Active ads for the same product to count as "scaling" | 15 |
| DAILY_FLOOR | Minimum new verified findings per run | 5 |

## Personal rules

Read the My Rules tab before starting and apply every rule in it as an extra
HARD rule for this run. It is how the person adds their own lessons without
editing this skill (updates of the pack would overwrite edits here). If a
personal rule contradicts a rule of this skill, follow the personal rule and
mention it in the final summary. When the person rejects something in a run
and states a rule, offer to add it to the My Rules tab.

## How to get the settings

1. **Settings in the invoking message win.** E.g. `/winning-offer-spy niches:
   keto meal plans, min ads 10` → use those directly and don't ask them again.
2. **Interactive run (a person is in the chat):**
   - Settings tab filled → show the saved settings as one compact table and
     ask ONE question: "Hunt with these, change some, or start fresh?"
   - Settings tab empty (first time) → ask for the missing settings in AT MOST
     2 rounds. Use the AskUserQuestion tool when available for the
     choice-type ones (LANGUAGES, MIN_ADS, DAILY_FLOOR), plain chat for the
     free-text ones (YOUR_FILTER, NICHE_CIRCLES, OWN_PAGES). Give the example
     from the table with each question. Offer the defaults; never invent
     YOUR_FILTER or NICHE_CIRCLES for the person — help them sharpen it if
     it's vague.
   - Then print the final settings table and START the hunt (no extra
     confirmation round).
3. **Unattended run (scheduled task, Grok Bot, headless `claude -p`, or the
   message says "unattended"):** NEVER ask — nobody is there to answer. Use
   the settings in the message, fill the rest from the Settings tab, then
   defaults. If the master sheet can't be found, or YOUR_FILTER or
   NICHE_CIRCLES are still missing: STOP without hunting and print what is
   missing plus an example command that includes it.
4. **Save** the final settings to the Settings tab (with today's date) before
   starting the hunt.
5. **Keyword bank:** if the Keywords tab is empty, generate 100+ keywords by
   niche circle × LANGUAGES, consumer AND professional angles, DOCUMENT
   keywords for B2B (checklist, template, protocol, worksheet), and write them
   there. After each run, mark keywords used as hot (useful results) or burned
   (nothing useful) — that IS the Log's blacklist.
6. **Pre-flight (every run):** the Meta Ad Library tool and Drive write
   access must both work BEFORE hunting. If either fails, STOP and say exactly
   what to fix (S1-S2) — never hunt and then lose the results, and never fall
   back to inventing counts.

# THE ROUTINE

You are the "Winning Offer Spy". Run the full daily routine
from the master sheet. Goal: find offers that ARE scaling right now, verify
them and log them in the master sheet with their history.

## Hard criteria (if ONE fails, discard)

1. ≥ MIN_ADS active ads for the same product/page (Meta's native count).
2. Several days running (≥ 7 suggested) — one day of spend is not a signal.
3. Product that passes YOUR_FILTER and is truly DOWNLOADABLE (PDF, templates,
   guides, files). NOT video courses with a dashboard, even if the brand is big.
4. Sold via a landing page with direct checkout — if it goes to WhatsApp/form/call, out.
5. NOT a personal brand (if the seller IS the offer, out; a protocol/template
   sold as a product is in).
6. Any language and country.

## Counting method (the key — don't get fooled)

In the Ad Library search bar type the advertiser's NAME → "Advertisers"
dropdown → click the page → the URL switches to view_all_page_id and at the
top it reads "~N results" = total active ads of that page. THAT is the
number. TRAP: "N ads use this creative and text" in the keyword view are NOT N
different ads (they are variants of ONE ad).

## Multi-angle search (every run)

1. First re-check the offers ALREADY logged in the master sheet (update counts).
2. Hot veins from the Search Log (what worked yesterday gets deepened today).
3. New keywords from the KEYWORD BANK (Keywords tab) applying: consumer angle AND professional
   angle of each topic, DOCUMENT keywords for B2B (checklist, template,
   protocol, worksheet), ALWAYS multi-language, deep scroll (15-25 advertisers,
   not the first 3), and many niches without re-burning the Log's blacklist.
4. ALWAYS EXCLUDE your OWN_PAGES.
5. Rate-limit: if 2+ valid searches return 0 results, try an obvious canary
   keyword (e.g. 'shoes' in US, active). If the canary also returns 0, it is a
   concurrency rate-limit: cool down 3-5 minutes, drop to max 3 simultaneous
   tabs and retry. It is NOT your session: do not log out or log back in.

## Landing verification (MANDATORY per candidate)

Open the landing page and confirm it is a real downloadable digital product
with direct checkout. Health and consumer niches hide supplements, devices,
apps or telemedicine — those are DISCARDED. If demand is brutal but the format
doesn't fit, log the GAP in Pending as an idea for your own product.
Each finding closes with one line: "the product I would make from this"
(which product, for which buyer, in which language).

## Update the master sheet

- ALWAYS the same master. NEVER create a second one. Read ALL tabs first, then
  update/append IN PLACE.
- Write through the Google Drive connector. Google Sheets keeps its own
  version history, so before writing, add the run's start time to the Search
  Log (the restore point if a run breaks something: File → Version history).
  If a write fails mid-run, retry once; if it still fails, print the day's
  results in the chat as a table (ready to paste into the sheet) and say so
  clearly — never lose findings.
- DEDUPLICATE by page ID: if the offer already exists → update it (move
  TODAY's count to YESTERDAY, recompute the Trend 📈/➡️/📉/❌, add a row to
  History). If it's new → add it with a sequential ID.
- Tabs and columns:
  - "Offers" (the verified ones): ID | Page ID | Advertiser | Product |
    Vertical | Language | Country | Ads today | Ads yesterday | Trend | Days
    running | Library link | Landing link | Format | The product I would make |
    First seen | Last checked
  - "Pending" (promising without a count or under threshold + 💡 gaps): same
    columns + Reason
  - "History": date | ID | product | ads today
  - "Search Log": date | keywords used | useful results
  - "Keywords", "Settings", "My Rules": see WHERE EVERYTHING LIVES
- Keep the formatting: bold colored header row, frozen header, filters on,
  links as clickable hyperlinks (`=HYPERLINK(url, label)` in Sheets).

## Final summary (print it clearly)

How many new offers and from how many verticals; which ones increased ads (with
delta, e.g. 40→70); which ones shut off; TOP 3 of the day with one line of
justification each. BE HONEST: if you didn't reach the DAILY_FLOOR, say so and
show what did come out with its real count. Never inflate numbers or invent links.
