---
name: offer-hunter
description: Daily hunt for scaling offers in Meta's Ad Library according to your format filter, and updates your master Excel with the history. Asks for its settings at the start (or reuses the last ones). Use when the user says 'hunt offers', 'the hunter', 'find scaling offers' or asks for the master Excel sweep.
---

# STEP 0 — HUNT SETTINGS (ask, never assume)

This skill has NO config block to edit. It gets its settings from the person
at the start of every hunt, and remembers the last answers in a profile file it
writes itself. This skill is the canonical source of the routine: scheduled
runs only point at it. Editing the routine = editing this file.

## The settings

| Setting | What it is | Default if the person doesn't care |
|---|---|---|
| WORK_FOLDER | Folder where the Excel, keyword bank and backups live | `./offer-hunter/` in the current project |
| MASTER_EXCEL | The single master file (ALWAYS the same file) | `offers-master.xlsx` |
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
6. **Master Excel:** if it doesn't exist, create it with the 4 sheets
   described below ("Offers", "Pending", "History", "Search Log"). After that,
   NEVER create another one.

# THE ROUTINE

You are the "Scaling Offer Hunter". Run the full daily routine from
WORK_FOLDER. Goal: find offers that ARE scaling right now, verify them and
log them in the MASTER_EXCEL with their history.

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

1. First re-check the offers ALREADY logged in the Excel (update counts).
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

## Update the Excel (Python + openpyxl)

- ALWAYS the same MASTER_EXCEL. NEVER create a new Excel. Flow: backup to
  *-backup.xlsx → load_workbook → update/append IN PLACE.
- DEDUPLICATE by page ID: if the offer already exists → update it (move
  TODAY's count to YESTERDAY, recompute the Trend 📈/➡️/📉/❌, add a row to
  History). If it's new → add it with a sequential ID.
- Sheets: "Offers" (the verified ones), "Pending" (promising without a count
  or under threshold + 💡 gaps), "History" (date | ID | product | ads today),
  "Search Log" (date | keywords used | useful results).
- Keep the formatting: colored headers, filters, links as hyperlinks.

## Final summary (print it clearly)

How many new offers and from how many verticals; which ones increased ads (with
delta, e.g. 40→70); which ones shut off; TOP 3 of the day with one line of
justification each. BE HONEST: if you didn't reach the DAILY_FLOOR, say so and
show what did come out with its real count. Never inflate numbers or invent links.
