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
| Google Drive for desktop | The base folder syncs on its own | `~/Library/CloudStorage/GoogleDrive-…` exists |

## 2. Installation, step by step

1. Copy the `ads-routine` folder (the one you received, with its SKILL.md) to `~/.claude/skills/`. It should end up as `~/.claude/skills/ads-routine/SKILL.md`.
2. Open that SKILL.md in any editor and fill in the CONFIGURATION block with YOUR data. The table in the next section explains each field and where to get it.
3. Connect in Claude Code what the routine needs (requirements table above). If a connector is missing, the routine will fail at that step and tell you — better to connect it first.
4. Restart Claude Code (or open a new session) so the skill shows up in the list.
5. DON'T schedule it yet: first the on-demand test in section 3.

> **Golden rule.** The skill you received is a TEMPLATE of a real operation: every rule exists because something failed one day and cost money. Adapt the data (paths, accounts, criteria) but DON'T delete rules you don't understand — first ask your Claude what that rule protects.

### The CONFIGURATION fields, one by one

| Field | What it is | Where to get it / example |
|---|---|---|
| MASTER_SHEET | The ID of your products Google Sheet | From the sheet URL: `docs.google.com/spreadsheets/d/THIS_ID/edit`. One row per product |
| BASE_FOLDER | Root ads folder in Drive for desktop | Inside will live: one folder per product + `_assets/` (research, winners, audit, landings cache) |
| IMAGE_ENGINE | Your generator and its exact command | The most powerful you have, max resolution, 1:1. Write down the full command with its flags |
| ENGINE_LIMITS | Simultaneous jobs your plan supports | It's in your plan's docs (typical: 8). The pipeline's semaphore respects it |
| OWN_PAGES | Your pages, excluded from research | page_id of each one (library → your page → `view_all_page_id` in the URL) |
| NICHE_RULES | Your compliance by niche | Health: no medical claims or dosages. Money: no income promises. Write it explicitly |
| TOP_MODEL / ECO_MODEL | Which model each agent uses | TOP (the most powerful on your plan) ONLY for director+critic and repairer; ECO (e.g. Sonnet) for research, generation, audit and orchestration |
| DEADLINE | Delivery cutoff | E.g. "1 hour after start". Whatever doesn't make it is reported with its cause; the run is not stretched |

> **The 5 cost rules — read them twice.** 1) The handoff between agents goes THROUGH DISK (files), never by pasting content into prompts. 2) An image in context is RE-CHARGED every turn: audit on ~768px copies, open each image ONCE. 3) Research via API, ZERO browser exploring (it's the most expensive part of the pipeline). 4) A run that dies halfway is NOT relaunched without asking — it repeats the expensive stages already paid for. 5) Measure by stage before diagnosing: intuition usually blames the wrong stage.

## 3. First run (critical: this is how you start)

1. DON'T run all products. Type: `/ads-routine only for <YOUR MAIN PRODUCT>`.
2. Wait for that product's full pipeline: API research → bank → direction → generation → audit → delivery.
3. Look at the 5 with your own eyes. Perfect text? Do they look like professional photography or a template? Does the figure shown exist on your landing? Do they look like a real winner or generic?
4. Turn everything you DON'T like into a rule: tell Claude "add to the skill: [your rule]". That's how the original was built — through rejections.
5. Repeat with that product for 2-3 days. When it comes out well without touching anything, add the rest of the products (sequentially, one after another).
6. The BANK starts empty: the first week the visual agent will work harder seeing new winners. It's an investment: every winner seen stays deconstructed forever.

## 4. Scheduling it (once it went well 2-3 times)

Tell Claude Code: "create a scheduled task that runs every day at 9:00 AM with this prompt" — and paste exactly this pointer:

```
Read the ENTIRE file ~/.claude/skills/ads-routine/SKILL.md with
the Read tool and execute it to the letter as if it were this
prompt. Summarizing it or running the routine from memory is forbidden.
If the file doesn't exist or can't be read: STOP without running
anything and report that the skill is not available.
Context: you are the daily scheduled run at 9:00 AM.
```

- The pointer makes the scheduled task and the manual run ALWAYS the same routine: the skill is the single source of truth.
- Editing the routine = editing the SKILL.md. The scheduled task is never touched again.
- To pause it: "pause the scheduled task" (the skill stays available on demand). To resume: "activate it again".

## 5. Day-to-day management

- **Your daily job (5-10 min): the human spot-check.** Open the 5 ads of 1-2 products (rotate which) and look at them. The routine already does its own spot-check, but you set the bar.
- **Every rejection of yours = a new rule in the skill that same day.** It's the only way it won't repeat tomorrow. That's how the routine improves — it isn't redesigned, it accumulates rules.
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
- [ ] BASE_FOLDER created in Drive for desktop with `_assets/` inside.
- [ ] Image engine tested by hand once (command and balance OK).
- [ ] CONFIGURATION complete, including NICHE_RULES and OWN_PAGES.
- [ ] First run with ONE product only, reviewed with your own eyes.
- [ ] 2-3 good days with that product before adding the rest.
- [ ] Scheduled at 9:00 AM; daily human spot-check of 1-2 products.
- [ ] Every rejection of yours turned into a rule in the SKILL.md the same day.
