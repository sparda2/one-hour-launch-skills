---
name: ads-routine
description: Full daily creative pipeline for Meta Ads: reads your master products Sheet, researches the best advertisers via API in the Ad Library (zero browser), generates 5 new AI image ads per product, audits them one by one and delivers them to Drive with links in the Sheet. Use when the user says 'the ads routine', 'run the routine', 'regenerate the ads' or asks for the 5 ads of a product.
---

> **TEMPLATE — ADAPT BEFORE RUNNING.** Fill in the CONFIGURATION block.
> This skill is the canonical source of the routine: the scheduled task only
> reads it and runs it. Editing the routine = editing this file.
> Version 2 (Aug 4, 2026): 100% API research, winners bank, visual agent
> and cost discipline — all measured in real production.

# CONFIGURATION (fill in EVERYTHING before the first run)

- MASTER_SHEET: <ID of your Google Sheet of products. Columns: PRODUCT | PRODUCT LINK (landing) | LANGUAGE | RESEARCH LINK | CREATIVES LINK. One row = one product>
- BASE_FOLDER: <local path of your ads folder, synced with Drive; inside: one subfolder per product and an _assets/ folder for internal material (research, bank, specs, audit)>
- IMAGE_ENGINE: <your most powerful AI image generator and its command (CLI or connector), at the highest resolution it offers, aspect ratio 1:1>
- ENGINE_LIMITS: <your plan's simultaneous job limit (e.g. 8) — enforced with a semaphore, not by launching fewer>
- OWN_PAGES: <your pages/stores, to EXCLUDE them from competitor research>
- NICHE_RULES: <your compliance rules by niche: health = no medical claims or dosages; money = no income promises; etc.>
- TOP_MODEL: <the most powerful Claude model on your plan — ONLY where design happens: director+critic and repairer>
- ECO_MODEL: <an economical model (e.g. Sonnet) — research, generation, audit and the orchestrating session>
- DEADLINE: <delivery cutoff, e.g. "1 hour after start". Whatever doesn't make it is reported with its cause — the run is not stretched>

# THE ROUTINE

Run the FULL pipeline every run: EVERYTHING is regenerated every day, all the
products in the Sheet, and the new ads must be DIFFERENT from yesterday's.
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

Read the MASTER_SHEET (Google Drive connector). Each row = one product with its
landing and its language. New product (row without a folder in BASE_FOLDER) →
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
(`_assets/research/`) and the "Winning creatives" sheet of the research Excels,
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
`BASE_FOLDER/<PRODUCT>/<YYYY-MM-DD>/`. Verify resolution and FRESHNESS (JPG's
mtime ≥ its source's mtime — an old JPG passes the size check). Don't delete
previous days' folders. Write the folder link in the Sheet's CREATIVES LINK
column, and the research Excel's link in RESEARCH LINK.

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
