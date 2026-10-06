# The Daily Ads Routine

Skill: `/ads-routine` · Suggested schedule: daily, 9:00 AM · The queen of the system

## 1. What it is and what you need

It produces 5 NEW image creatives every day for EACH product in your master Sheet, modeling the best advertisers in the world (never inventing from scratch), audits them one by one and delivers them organized in Drive. It's the most powerful routine and the most delicate: this version (v2) incorporates the cost lessons measured in production — 100% API research, a winners bank that's paid for only once, and strict discipline with images in context.

| Requirement | What it's used for | How to know you have it |
|---|---|---|
| Master products Sheet | The source of truth: which products, which landing, which language | Create it FIRST: columns PRODUCT \| PRODUCT LINK \| LANGUAGE \| RESEARCH LINK \| CREATIVES LINK |
| Google Drive connector | Read the Sheet and write links | Claude can read your Sheet by its ID |
| Meta Ads connector | API research (`ads_library_search`) | Ask Claude if it has the tool |
| AI image engine (CLI or connector) | Generate the 5 ads per product at max resolution | You have the exact command and balance/credits |
| (Optional) a synced folder: Google Drive for desktop, or a GitHub repo on the web | Your ads get backed up automatically | Your base folder is inside it |

## 2. Installation and settings

Install the pack by following **START-HERE.md**. Before the first run, create your **master Sheet**: one row per product, with the columns PRODUCT | PRODUCT LINK | LANGUAGE | RESEARCH LINK | CREATIVES LINK.

There's no config file to fill in. On the first run the routine asks you for these settings, tests your image engine with a single cheap generation, and saves everything to `launch-profile.md`:

| Setting | What it is | Example / default |
|---|---|---|
| Master Sheet | Your products Google Sheet | Its URL or its ID (`docs.google.com/spreadsheets/d/THIS_ID/edit`) |
| Products this run | Which rows to run | All rows (default). On the very first run: just your main product |
| Base folder | Where the ads go: one folder per product + `_assets/` | `./ads/` (default) |
| Image engine | Your generator and its exact command or connector | The most powerful one you have, max resolution, 1:1 |
| Engine limits | How many jobs your image plan runs at the same time | It's in your plan's docs (typical: 8) |
| Own pages | Your pages, excluded from research | Reused from the Winning Offer Spy if you already gave them |
| Niche rules | Your compliance rules by niche | Health: no medical claims or dosages. Money: no income promises |
| Top / Eco model | Which model each agent uses | Top = the most powerful model on your plan, ONLY for director+critic and repairer. Eco (e.g. Sonnet) for everything else |
| Deadline | Delivery cutoff | 1 hour after start (default) |

On later runs it shows your saved settings and asks: *"Run with these, change some, or start fresh?"*

> **Golden rule.** This skill comes from a real operation: every rule in it exists because something failed one day and cost money. Don't delete rules you don't understand. First ask your Claude what that rule protects.

> **The 5 cost rules — read them twice.** 1) The handoff between agents goes THROUGH DISK (files), never by pasting content into prompts. 2) An image in context is RE-CHARGED every turn: audit on ~768px copies, open each image ONCE. 3) Research via API, ZERO browser exploring (it's the most expensive part of the pipeline). 4) A run that dies halfway is NOT relaunched without asking — it repeats the expensive stages already paid for. 5) Measure by stage before diagnosing: intuition usually blames the wrong stage.

## 3. First run (critical: this is how you start)

1. DON'T run all products. Type: `/ads-routine only for <YOUR MAIN PRODUCT>`.
2. Wait for that product's full pipeline: API research → bank → direction → generation → audit → delivery.
3. Look at the 5 with your own eyes. Perfect text? Do they look like professional photography or a template? Does the figure shown exist on your landing? Do they look like a real winner or generic?
4. Turn everything you DON'T like into a rule. Tell Claude "add to my rules: [your rule]". It goes into `my-rules.md` in your work folder, and every run reads that file automatically. That's how the original was built: through rejections.
5. Repeat with that product for 2-3 days. When it comes out well without touching anything, add the rest of the products (sequentially, one after another).
6. The BANK starts empty: the first week the visual agent will work harder seeing new winners. It's an investment: every winner seen stays deconstructed forever.

## 4. Scheduling it (once it went well 2-3 times)

Create a daily task: a scheduled task in the Claude desktop app, or claude.ai/code → Routines on the web. Set it for 9:00 AM with exactly this prompt:

```
Run the ads-routine skill in unattended mode, using the saved settings
in launch-profile.md. Follow the skill to the letter; do not run the
routine from memory. If the skill is not available, stop and report it.
Context: you are the daily scheduled run at 9:00 AM.
```

- In unattended mode the skill never asks questions. It uses your saved settings, and if an essential one is missing it stops and tells you.
- The skill is the single source of truth. Updating the pack updates the routine, so the scheduled task is never touched again.
- To pause it, pause the scheduled task. The skill stays available on demand.

## 5. Day-to-day management

- **Your daily job (5-10 min): the human spot-check.** Open the 5 ads of 1-2 products (rotate which) and look at them. The routine already does its own spot-check, but you set the bar.
- **Every rejection of yours = a new rule in your `my-rules.md` that same day.** It's the only way it won't repeat tomorrow. That's how the routine improves — it isn't redesigned, it accumulates rules.
- **Watch the bank:** over the weeks, almost all winners will come out "BANK: yes" and research will be dirt cheap. If the visual agent works a lot every day, something is wrong in the cross-check against the bank.
- **If one day it's expensive or slow:** ask for the breakdown by stage (agent-minutes and cost) BEFORE touching anything. In the original operation intuition blamed image generation; measurement showed research was 73% of the spend.
- **New product:** add it as a row to the Sheet — the routine creates its folder and pipeline on its own.
- **Once it's been stable for 1-2 weeks:** ask your Claude to script it (parallel pipeline with semaphore and deadline). Not before.

## 6. Common problems

| Symptom | Cause | Solution |
|---|---|---|
| Broken letters / pseudo-words in the image | A prop with text in the prompt (ruler, tab, spine, screen) | REMOVE the prop from the prompt (asking for "blur" isn't enough). Short headlines in pure text |
| A figure that doesn't exist on your landing | The director invented it and nobody verified | Use the landings cache; if it isn't verified, it goes without a figure |
| The 5 look like Canva templates | Button/pill, headline-subtitle-button skeleton | Art direction rules in STEP 5.6 — the text lives INSIDE the photo |
| Today's set is the same as yesterday's | The concept log wasn't checked | "Different from yesterday" rule: look at yesterday's 5 before directing |
| The auditor rejects all 5 (zero approved) | Almost always a race with generation: folder still empty | Repeat the audit ONCE; the auditor marks "not delivered" if a file is missing, doesn't invent a verdict |
| Suddenly very expensive run | Large images in context or browser in research | Review the 5 cost rules; audit at 768px; research API only |
| Died mid-run | Credits exhausted, engine error… | DON'T relaunch hot: report what failed, what repeating it would cost, and wait for the owner's OK |

## 7. Checklist for this skill

- [ ] Master Sheet created with the 5 columns and all your rows.
- [ ] Google Drive and Meta Ads connectors working.
- [ ] Image engine tested (the first run does this for you).
- [ ] Niche rules and own pages given on the first run.
- [ ] First run with ONE product only, reviewed with your own eyes.
- [ ] 2-3 good days with that product before adding the rest.
- [ ] Scheduled at 9:00 AM; daily human spot-check of 1-2 products.
- [ ] Every rejection of yours turned into a rule in `my-rules.md` the same day.
