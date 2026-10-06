# Winning Ads Creator

Skill: `/winning-ads-creator` · Suggested schedule: daily, 9:00 AM · The queen of the system

## 1. What it is and what you need

Every day it creates 5 NEW image ads for EACH product in your master sheet. It models them on the best advertisers in the world instead of inventing from scratch, audits them one by one, and delivers them to your Google Drive. It's the most powerful skill in the pack and the most delicate. This version comes with the cost lessons measured in production: 100% API research, a winners bank you only pay for once, and strict discipline with images in context.

| Requirement | What it's used for | How the setup checks it |
|---|---|---|
| Meta Ads connector + an **active Meta ad account** | Researching winners in the Ad Library (`ads_library_search`) | It runs one test search |
| Google Drive (+ Google Sheets) connector | Your master sheet: products, settings, winners bank, concepts | It creates the sheet and reads it back |
| The **Drive uploader** (a small Google script, set up once in about 3 minutes) | Sending ad images to your Drive without costing tokens | It uploads and downloads a test file |
| An **AI image generator** with credits: an API key, a CLI or a connector | Generating the 5 ads per product at max resolution | It generates one cheap test image |
| Claude Code cloud session with **Full** network access | Running the pipeline, opening landing pages, viewing winners | It opens 3 test sites |

## 2. Installation and setup: the wizard does it

1. Upload `dist/winning-ads-creator-EN.zip` at **claude.ai → Settings → Capabilities → Skills**.
2. Open a **Claude Code cloud session** (desktop app → Code → Cloud).
3. Type: *"Set up the Winning Ads Creator for me step by step."*

The wizard checks everything above and gives you one click-by-click fix list. It needs at most one restart. Then it creates your **"Winning Ads Creator"** Drive folder and master sheet, helps you deploy the Drive uploader, asks for your products and settings, runs a test, and makes your first 5 ads.

**Your API key** goes into the cloud environment's **Environment variables** (environment menu → Edit), for example `OPENAI_API_KEY=…`. Never paste it in the chat. The wizard tells you exactly where.

### The settings it will ask you (saved in the Settings tab)

| Setting | What it is | Example / default |
|---|---|---|
| Products | Your products: name, landing page URL, ad language | One row per product in the Products tab |
| Image engine | Your generator and how to call it | The most powerful one you have, max resolution, 1:1. An API is better than a connector (cheaper) |
| Engine limits | How many images your plan generates at the same time | It's in your plan's docs (4 if unknown) |
| Own pages | Your pages, excluded from research | Reused from the Winning Offer Spy if you have it |
| Niche rules | Your compliance rules | Health: no medical claims or dosages. Money: no income promises |
| Top / Eco model | Which Claude model each agent uses | Top = your most powerful model, ONLY for director+critic and repairer. Eco (Sonnet-class) for the rest |
| Deadline | Delivery cutoff | 1 hour after start |

On later runs it shows your settings and asks: *"Run with these, change some, or start fresh?"*

> **Golden rule.** This skill comes from a real operation: every rule in it exists because something failed one day and cost money. Don't delete rules you don't understand. First ask your Claude what that rule protects. To add your own rules, say *"add to my rules: …"*. They go into the **My Rules** tab, and pack updates never overwrite them.

> **The 5 cost rules — read them twice.** 1) The handoff between agents goes THROUGH DISK (files), never by pasting content into prompts. 2) An image in context is RE-CHARGED every turn: audit on ~768px copies, open each image ONCE. 3) Research via API, ZERO browser exploring (it's the most expensive part of the pipeline). 4) A run that dies halfway is NOT relaunched without asking, because that repeats the expensive stages already paid for. 5) Measure by stage before diagnosing: intuition usually blames the wrong stage.

## 3. First run (critical: this is how you start)

1. The wizard runs **ONE product** only. Later, type `/winning-ads-creator only for <YOUR MAIN PRODUCT>`.
2. Wait for that product's full pipeline: API research → bank → direction → generation → audit → delivery to Drive.
3. Open the 5 ads in your Drive and look at them with your own eyes. Perfect text? Professional photography or a template look? Does every figure exist on your landing? Do they look like a real winner or generic?
4. Turn everything you DON'T like into a rule: *"add to my rules: [your rule]"*. That's how the original was built: through rejections.
5. Repeat with that product for 2–3 days. When it comes out well without touching anything, add the rest of your products, one after another.
6. The BANK starts empty, so the first week the visual agent works harder viewing new winners. That's an investment: every winner it views stays deconstructed in your Winners Bank tab for good.

## 4. Scheduling it (once it went well 2–3 times)

Create a daily task: a scheduled task in the Claude desktop app, or claude.ai/code → Routines. Set it for 9:00 AM with exactly this prompt:

```
Run the winning-ads-creator skill in unattended mode, using the saved
settings in the "Winning Ads Creator — Master" sheet. Follow the skill
to the letter; do not run the routine from memory. If the skill is not
available, stop and report it.
Context: you are the daily scheduled run at 9:00 AM.
```

- In unattended mode it never asks questions. If something essential is missing, it stops and tells you what.
- The skill is the single source of truth. Updating the pack updates the routine, so the scheduled task is never touched again.

## 5. Day-to-day management

- **Your daily job (5–10 min): the human spot-check.** Open the 5 ads of 1–2 products in Drive (rotate which). The routine does its own spot-check, but you set the bar.
- **Every rejection of yours = a new rule in My Rules that same day.** It's the only way it won't repeat tomorrow. The routine isn't redesigned; it accumulates rules.
- **Watch the bank:** over the weeks, almost every winner will come out "BANK: yes" and research will be dirt cheap. If the visual agent works a lot every day, something is wrong with the bank lookup.
- **If one day it's expensive or slow:** check the Run Log tab (time per stage) BEFORE touching anything. In the original operation research turned out to be 73% of the spend, not image generation.
- **New product:** add a row to the Products tab. The routine creates its folder and pipeline on its own.
- **Once it's been stable for 1–2 weeks:** ask your Claude to script it (parallel pipeline with semaphore and deadline). Not before.

## 6. Common problems

| Symptom | Cause | Solution |
|---|---|---|
| "Ad Library tool not available" or an ad account error | No active Meta ad account | Create or reactivate one at business.facebook.com |
| Images aren't reaching Drive | Uploader not set to "Anyone", or the wrong URL | Redeploy: Web app → Who has access **Anyone**; use the URL ending in `/exec` |
| "Key not found" for the image engine | The key isn't in the environment variables, or it was added after the session started | Add it under environment → Edit → Environment variables, then start a new session |
| Broken letters or pseudo-words in the image | A prop with text in the prompt (ruler, tab, spine, screen) | REMOVE the prop from the prompt; asking for "blur" isn't enough. Keep headlines short and in plain text |
| A figure that doesn't exist on your landing | The director invented it and nobody verified it | The Landings Cache tab has the verified figures. If a figure isn't verified, the ad goes without it |
| The 5 look like Canva templates | Button or pill, headline-subtitle-button layout | Art direction rules in STEP 5.6: the text lives INSIDE the photo |
| Today's set is the same as yesterday's | The concept log wasn't checked | "Different from yesterday" rule: it looks at yesterday's 5 ads and the Concepts Log tab before directing |
| The auditor rejects all 5 | Almost always a race with generation: the folder is still empty | It repeats the audit ONCE, and marks a missing file "not delivered" instead of inventing a verdict |
| Suddenly very expensive run | Large images in context, or the browser used in research | Review the 5 cost rules; audit at 768px; research by API only |
| Died mid-run | Credits ran out, engine error… | DON'T relaunch right away: it reports what failed and what repeating it would cost, and waits for your OK |

## 7. Checklist for this skill

- [ ] Skill uploaded at claude.ai → Settings → Capabilities → Skills.
- [ ] Meta connector + an active ad account, plus the Google Drive and Sheets connectors.
- [ ] Network set to Full; image engine key added as an environment variable.
- [ ] Drive uploader deployed and tested (the wizard does the test).
- [ ] Products tab filled; first run with ONE product, reviewed with your own eyes.
- [ ] 2–3 good days with that product before adding the rest.
- [ ] Scheduled at 9:00 AM; daily human spot-check of 1–2 products.
- [ ] Every rejection of yours turned into a rule in My Rules the same day.
