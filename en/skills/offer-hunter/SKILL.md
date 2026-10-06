---
name: offer-hunter
description: Daily hunt for scaling offers in Meta's Ad Library according to your format filter, and updates your master Excel with the history. Use when the user says 'hunt offers', 'the hunter', 'find scaling offers' or asks for the master Excel sweep.
---

> **TEMPLATE — ADAPT BEFORE RUNNING.** Fill in the CONFIGURATION block.
> This skill is the canonical source of the routine: the scheduled task only
> reads it and runs it. Editing the routine = editing this file.

# CONFIGURATION (fill in EVERYTHING before the first run)

- WORK_FOLDER: <local path of your hunting folder, ideally synced with Drive>
- MASTER_EXCEL: <your file name, e.g. offers-master.xlsx — ALWAYS the same file>
- YOUR_FILTER: <which product format YOU can replicate (e.g. "low-ticket downloadable digital toolkits, replicable with AI"). Only what passes this filter gets logged>
- NICHE_CIRCLES: <circle 1 = your current niches; circle 2 = same buyer; circle 3 = adjacent. The hunt goes in that order>
- OWN_PAGES: <list of YOUR pages/stores, to EXCLUDE them from the hunt — otherwise you "discover" yourself as competition>
- KEYWORD_BANK: <file with your keyword bank by category and language; build one with hundreds>
- MIN_ADS: <threshold of active ads for the same product to count as "scaling"; suggested: 15>
- DAILY_FLOOR: <minimum new verified findings per run; suggested: 5>

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
