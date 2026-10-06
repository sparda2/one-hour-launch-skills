---
name: offer-hunter
description: Daily hunt for scaling offers in Meta's Ad Library according to your format filter, and updates your master Google Sheet (or Excel) with the history. Asks for its settings at the start (or reuses the last ones). Includes a guided first-time setup that takes anyone from 'I just uploaded this file' to their first hunt. Use when the user says 'hunt offers', 'the hunter', 'find scaling offers', 'set up the offer hunter', uploads this skill and asks to set it up, or asks for the master sheet sweep.
---

# GUIDED SETUP — from "I just uploaded this file" to the first hunt

Run this section FIRST whenever the profile (`launch-profile.md`, section
`## Offer hunter`) does not say `Setup: complete`, or when the person asks to
set up / repair the hunter. Once setup is complete, skip straight to STEP 0.

**How to guide (non-negotiable):**
- Talk in the person's language. Assume they are NOT technical: one action at
  a time, exact click paths, what they will see, and how to tell it worked.
- CHECK before asking: detect everything you can yourself (tools, network,
  files, git). Only ask the person for what you can't detect or do.
- Batch every fix that needs a NEW session into ONE restart (connectors and
  network changes only load when a session starts). Never make them restart
  twice if one restart could do it.
- Keep a checklist in the profile (`## Offer hunter` → `Setup:` with each
  step ✅/❌) and commit + push it, so progress survives a restart.
- Show progress each turn as a short checklist: ✅ done, 👉 now, ⬜ next.
- Never ask for passwords, tokens or API keys in the chat.

**S1 — Where are we running?**
Check `echo $CLAUDE_CODE_REMOTE` (`true` = cloud session at claude.ai/code or
the desktop/mobile app; otherwise a local computer).
- Cloud: files are DELETED when the session ends. The work must live in a
  GitHub repository the session can push to. Check with `git remote -v` and a
  dry-run push. If there is no writable repo: guide them to create a private
  repo (github.com/new → name `my-launch-workspace` → Private → Create), make
  sure the Claude GitHub App can access it (github.com/apps/claude →
  Configure → add the repo), then start a NEW session on that repo and upload
  this skill file again. Give them the exact first message to paste (S8).
- Local: any folder works; recommend a git repo or a synced folder for backups.

**S2 — Install the skill in the workspace (so it's there next time).**
If this skill is not already available as an installed skill or plugin, copy
THIS file to `.claude/skills/offer-hunter/SKILL.md` in the workspace (keep it
byte-for-byte; never edit its rules), then commit and push. From now on, any
session on this workspace has `/offer-hunter`.

**S3 — Detect what's missing (all at once).** Search the available tools
(including deferred tools / tool search) and test:
- **Meta Ad Library tool** (e.g. `ads_library_search`; the name varies by
  connector). Missing → ❌ Meta.
- **Google Drive / Sheets tools** that can create and write a Google Sheet
  (only if OUTPUT = google-sheet, the default). Missing → ❌ Drive.
- **Network (cloud only):** fetch `https://www.facebook.com/ads/library/` and
  one random non-allowlisted site (e.g. `https://gumroad.com`). Blocked →
  ❌ Network. (Competitor landings can be on any domain.)

**S4 — Fix everything in ONE round, then ONE restart.** Give one numbered
list with only the ❌ items:
- ❌ Meta → claude.ai → Settings → Connectors (claude.ai/customize/connectors)
  → find the Meta Ads connector in the directory, or "Add custom connector"
  with the URL of their Meta MCP server → Connect → log in to Meta → approve.
- ❌ Drive → same page → Google Drive → Connect → choose their Google account
  → allow access.
- ❌ Network (cloud) → in the session title bar, open the environment menu →
  Edit → Network access → **Full** → Save.
Then: commit + push the profile checklist, and tell them to start a NEW
session on the same workspace repo and paste the resume message (S8). If
nothing is ❌, skip the restart.

**S5 — Verify after the restart.** Re-run S3. Anything still ❌ → explain the
most likely cause in one line (e.g. "the connector was added after this
session started") and the one fix. Don't continue until Meta works (no Meta =
no hunt). If only Drive fails, offer OUTPUT = excel as a fallback.

**S6 — Settings.** Run STEP 0 → "How to get the settings" (first-time
questions, at most 2 rounds). Help sharpen YOUR_FILTER and NICHE_CIRCLES if
vague, never invent them. For OWN_PAGES, show how to find a page_id (Ad Library
→ search their page → click it → the URL shows `view_all_page_id=NUMBER`) or
look the names up with the Meta tool and confirm with them.

**S7 — Smoke test (2 minutes, before the real hunt).**
- Meta: one canary query (e.g. 'shoes', US, active). Results > 0 → ✅.
- Sheet: create the master sheet (or open the one they gave), write the
  header rows of the 4 tabs, read them back → ✅, and give them the link.
- Keyword bank: generate it (STEP 0 → point 5) and say where it is.
Mark `Setup: complete` in the profile, commit + push, then tell them: "Setup
done. Starting your first hunt now (20-40 min)." and go to THE ROUTINE.

**S8 — Resume message (give it whenever a restart is needed):**
`Continue setting up the offer hunter — read .claude/skills/offer-hunter/SKILL.md and resume the GUIDED SETUP from the checklist in launch-profile.md.`

**After the first hunt:** ask them to check 2-3 findings by hand (library
link: really that many active ads? landing: really a downloadable product with
direct checkout?). If the finds don't fit what they can make, their filter is
loose → offer "change some" and tighten it. Finally, offer to set up the daily
scheduled run (unattended mode) — only once they're happy with 2-3 runs.

# STEP 0 — HUNT SETTINGS (ask, never assume)

This skill has NO config block to edit. It gets its settings from the person
at the start of every hunt, and remembers the last answers in a profile file it
writes itself. This skill is the canonical source of the routine: scheduled
runs only point at it. Editing the routine = editing this file.

## The settings

| Setting | What it is | Default if the person doesn't care |
|---|---|---|
| WORK_FOLDER | Folder where the keyword bank and local files live | `./offer-hunter/` in the current project |
| OUTPUT | Where findings are logged: `google-sheet` (needs the Google Drive connector) or `excel` (local file, Python + openpyxl) | `google-sheet` |
| MASTER_SHEET | URL of the master Google Sheet (ALWAYS the same one). Only for OUTPUT = google-sheet | If none: create "Offer Hunter — Master" in the person's Drive on the first run and save its URL |
| MASTER_EXCEL | The master Excel file (ALWAYS the same file). Only for OUTPUT = excel | `WORK_FOLDER/offers-master.xlsx` |
| YOUR_FILTER | The product format the person can replicate. Only what passes it gets logged. E.g. "low-ticket downloadable digital toolkits (PDF guides, templates, prompt packs) I can produce with AI in days; no video courses, coaching or services" | **None — must be asked** |
| NICHE_CIRCLES | Circle 1 = current niches; 2 = same buyer, other topics; 3 = adjacent. 3-5 each. The hunt goes in that order | **None — must be asked** |
| OWN_PAGES | The person's own Facebook pages (names or page_ids), EXCLUDED from the hunt | Ask; "none" only if the person says so |
| LANGUAGES | Languages to search in | All languages, English first |
| MIN_ADS | Active ads for the same product to count as "scaling" | 15 |
| DAILY_FLOOR | Minimum new verified findings per run | 5 |
| KEYWORD_BANK | Keyword bank file, by category and language | `WORK_FOLDER/keyword-bank.md` |

## The profile file

`launch-profile.md` in the root of the current project, section
`## Offer hunter` (other skills of this pack keep their own sections in the
same file; `## Shared` holds OWN_PAGES for every skill). It stores the last
answers with their date. It is written BY THIS SKILL — nobody has to edit it
by hand (they may, if they want). Never store passwords, tokens or API keys in it.

## Personal rules

If `my-rules.md` exists in the root of the current project, read it before
starting and apply every rule in it as an extra HARD rule for this run. It is
how the person adds their own lessons without editing this skill (updates of
the pack would overwrite edits here). If a personal rule contradicts a rule of
this skill, follow the personal rule and mention it in the final summary.
When the person rejects something in a run and states a rule, offer to append
it to `my-rules.md` (create the file if needed).

## How to get the settings

1. **Settings in the invoking message win.** E.g. `/offer-hunter niches:
   keto meal plans, min ads 10` → use those directly and don't ask them again.
2. **Interactive run (a person is in the chat):**
   - Profile exists → show the saved settings as one compact table and ask ONE
     question: "Hunt with these, change some, or start fresh?"
   - No profile (first time) → ask for the missing settings in AT MOST 2
     rounds. Use the AskUserQuestion tool when available for the choice-type
     ones (LANGUAGES, MIN_ADS, DAILY_FLOOR), plain chat for the free-text ones
     (YOUR_FILTER, NICHE_CIRCLES, OWN_PAGES). Give the example from the table
     with each question. Offer the defaults; never invent YOUR_FILTER or
     NICHE_CIRCLES for the person — help them sharpen it if it's vague.
   - Then print the final settings table and START the hunt (no extra
     confirmation round).
3. **Unattended run (scheduled task, Grok Bot, headless `claude -p`, or the
   message says "unattended"):** NEVER ask — nobody is there to answer. Use
   the settings in the message, fill the rest from the profile, then defaults.
   If YOUR_FILTER or NICHE_CIRCLES are still missing: STOP without hunting and
   print which settings are missing plus an example command that includes
   them.
4. **Save** the final settings to the profile (update the `## Offer hunter`
   section in place, with today's date) before starting the hunt.
5. **Keyword bank:** if KEYWORD_BANK doesn't exist, generate one (100+
   keywords by niche circle × LANGUAGES, consumer AND professional angles,
   DOCUMENT keywords for B2B: checklist, template, protocol, worksheet),
   save it, and tell the person in one line where it is.
6. **Master sheet:** check the tools BEFORE hunting. For `google-sheet`, the
   Google Drive connector must be able to read AND write the sheet — if it
   can't, STOP and say exactly what to connect (don't hunt and then lose the
   results). If MASTER_SHEET is empty, create it with the 4 tabs described
   below ("Offers", "Pending", "History", "Search Log"), save its URL to the
   profile, and give the person the link. After that, NEVER create another one.
   For `excel`, same with MASTER_EXCEL.
7. **Meta tools:** confirm the Meta connector exposes an Ad Library search
   tool (usually `ads_library_search`; the name can vary by connector). If
   there is none, STOP and say so — never fall back to inventing counts.

# THE ROUTINE

You are the "Scaling Offer Hunter". Run the full daily routine from
WORK_FOLDER. Goal: find offers that ARE scaling right now, verify them and
log them in the master sheet (MASTER_SHEET or MASTER_EXCEL) with their history.

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
3. New keywords from the KEYWORD_BANK applying: consumer angle AND professional
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
- **Google Sheet (default):** write through the Google Drive connector.
  Google Sheets keeps its own version history, so before writing, add the
  run's start time to the Search Log (the restore point if a run breaks
  something: File → Version history). If a write fails mid-run, save the
  day's results to `WORK_FOLDER/pending-sync-<DATE>.csv`, report it, and
  sync them on the next run — never lose findings.
- **Excel:** Python + openpyxl. Backup to `*-backup.xlsx` → load_workbook →
  update/append IN PLACE.
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
- Keep the formatting: bold colored header row, frozen header, filters on,
  links as clickable hyperlinks (`=HYPERLINK(url, label)` in Sheets).

## Final summary (print it clearly)

How many new offers and from how many verticals; which ones increased ads (with
delta, e.g. 40→70); which ones shut off; TOP 3 of the day with one line of
justification each. BE HONEST: if you didn't reach the DAILY_FLOOR, say so and
show what did come out with its real count. Never inflate numbers or invent links.
