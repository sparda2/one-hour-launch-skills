# One Hour Launch Skills — Start Here

This guide takes you from zero to your first offer hunt. Read it once, top to bottom. It takes about 30 minutes, most of it waiting for the first run.

**You never edit configuration files.** Each skill asks for its settings the first time you run it, remembers your answers, and on later runs asks: *"Use the same settings, change some, or start fresh?"*

---

## ⚡ The fast way (recommended): let the skill set itself up

You don't need to read the rest of this guide. The Offer Hunter has a **guided setup** built in: it checks what's missing, tells you exactly what to click, and takes you all the way to your first hunt.

1. **Create your workspace.** On GitHub, go to **github.com/new**, name it `my-launch-workspace`, choose **Private**, and click **Create repository**.
2. **Open Claude Code in the cloud.** Go to **claude.ai/code**, or in the Claude desktop app open **Code** and choose **Cloud**. Start a new session on `my-launch-workspace`. If GitHub asks for permission, allow access to that repository.
3. **Upload the skill.** Download `en/skills/offer-hunter/SKILL.md` from this pack and attach it to your first message.
4. **Type:**
   ```
   Set this up for me step by step, then run my first offer hunt.
   ```

Claude then guides you, one step at a time:

| ✅ | Step | What happens |
|---|---|---|
| 1 | Workspace | It checks it can save to your GitHub repository, so nothing is lost when the session ends |
| 2 | Install | It saves the skill into your workspace, so `/offer-hunter` works in every future session |
| 3 | Connections | It checks for the **Meta Ads** and **Google Drive** connectors and internet access, and gives you one short click-by-click list for anything missing |
| 4 | One restart | Connectors only load in a new session. It saves your progress and gives you a message to paste into the new session to continue |
| 5 | Your settings | It asks for your product filter, niches and pages, in at most 2 rounds |
| 6 | Quick test | One test search on Meta, and it creates your master Google Sheet and gives you the link |
| 7 | First hunt | 20–40 minutes, ending with your top 3 offers of the day |

> **After setup**, every time you want to hunt, open a session on `my-launch-workspace` and type `/offer-hunter`.

The sections below are the reference: what each piece is, other ways to install (your own computer, Grok Bot), automation, and troubleshooting.

---

## 1. What's in the pack

| Step | Skill | What it does | Status |
|---|---|---|---|
| 1 | **Offer Hunter** | Finds offers that are scaling right now in Meta's Ad Library and logs them in a master Google Sheet (or Excel) with their history | ✅ Ready |
| 2 | **Product Modeler** | Turns a winning offer into the spec of your own product | 🚧 Coming |
| 3 | **Funnel Modeler** | Builds your funnel using a proven landing page structure | 🚧 Coming |
| 4 | **Ads Routine** | Creates 5 new image ads per product every day, modeled on the world's best advertisers | ✅ Ready |

Each step feeds the next one: **winning offer → product → funnel → ads.**

---

## 2. What you need

| You need | Needed for | How to check |
|---|---|---|
| A Claude plan that includes **Claude Code** (Pro or Max) | Everything | You can open Claude Code (desktop app, terminal, or claude.ai/code) |
| A **GitHub account** with access to this pack | Installing and updating the skills | You accepted the GitHub invite you got after purchase, and you can open the pack's repository page |
| A **Meta Ads connector** that includes the Ad Library search tool | Offer Hunter, Ads Routine | Ask Claude: *"Do you have access to ads_library_search?"* |
| The **Google Drive** connector | Offer Hunter (writes your master Google Sheet), Ads Routine (reads your products Sheet) | Ask Claude: *"Can you read my Google Sheet <link>?"* |
| An **AI image generator** with credits (CLI or connector) | Ads Routine | You know the exact command or connector name |

You add connectors at **claude.ai → Settings → Connectors**. Start a new Claude Code session after connecting one, because connectors only load when a session starts.

> You only need the Meta connector to start with the Offer Hunter. Leave the Ads Routine requirements for later.

---

## 3. Choose where to run it

| Option | Best for | Notes |
|---|---|---|
| **A. Claude Code on your computer** (desktop app or terminal) | Most people. **Start here.** | Simplest setup. Your files stay on your computer. |
| **B. Claude Code on the web** (claude.ai/code) | Running from anywhere, including your phone | Your files live in a private GitHub repository. |
| **C. Grok Bot** (or any always-on agent with its own cloud computer) | Advanced: delegating runs to an agent | The bot runs Claude Code for you. Set up A first. |

---

## 4. Install the skills

### Option A — Claude Code on your computer

1. Create a folder for your work, for example `my-launch`, and open Claude Code in it.
2. Make sure git can reach your GitHub account, because the pack is private. If you have the GitHub CLI, run `gh auth login` once.
3. In Claude Code, type:
   ```
   /plugin marketplace add sparda2/one-hour-launch-skills
   /plugin install one-hour-launch@one-hour-launch-skills
   ```
4. Restart Claude Code, or start a new session.
5. Check it worked: type `/` and look for `offer-hunter` and `ads-routine` in the list. They may appear as `one-hour-launch:offer-hunter`.

### Option B — Claude Code on the web

1. On GitHub, create a **private** repository for your work, for example `my-launch-workspace`.
2. Add a file named `.claude/settings.json` to it with this content:
   ```json
   {
     "extraKnownMarketplaces": {
       "one-hour-launch-skills": {
         "source": { "source": "github", "repo": "sparda2/one-hour-launch-skills" }
       }
     },
     "enabledPlugins": { "one-hour-launch@one-hour-launch-skills": true }
   }
   ```
3. Go to **claude.ai/code**, connect GitHub if asked, and start a session on `my-launch-workspace`.
4. Check it worked: type `/` and look for the skills.
   - If they don't appear, add the `one-hour-launch-skills` repository to the session as well.
   - If they still don't appear, copy the folders in `en/skills/` into your workspace repository under `.claude/skills/`. That always works.
5. **Important:** web sessions run on temporary computers. At the end of each run, ask Claude to *commit and push* so your keyword bank and files are saved to your workspace repository.

### Option C — Grok Bot

1. Ask the bot to install Claude Code on its cloud computer: `npm install -g @anthropic-ai/claude-code`.
2. **Log in yourself.** Never give the bot your passwords.
3. In the bot's terminal, follow Option A, steps 1–5.
4. Do your first run yourself in **interactive** mode (step 6 below) so your settings get saved.
5. From then on, the bot can start runs with:
   ```
   claude -p "Run the offer-hunter skill in unattended mode."
   ```

---

## 5. Prepare your answers (5 minutes)

On the first run, the Offer Hunter asks you for the settings below. Have your answers ready:

| It will ask for | What to prepare | Example |
|---|---|---|
| **Your filter** | 2–3 sentences: what kind of product can **you** realistically make? Be strict, because the hunter's quality depends on your filter. | "Low-ticket downloadable digital products (PDF guides, templates, prompt packs) I can make with AI in a few days. No video courses, coaching or services." |
| **Your niches** | 3–5 niches for each of 3 circles. Circle 1: your current niches. Circle 2: the same buyer, other topics. Circle 3: adjacent niches. | Circle 1: meal planning, budgeting. Circle 2: home organization… |
| **Your own Facebook pages** | Their names, or better their page IDs. To find a page ID: open the Meta Ad Library, search your page, click it, and the URL shows `view_all_page_id=NUMBER`. | `My Brand`, `123456789` |
| **Languages** | Which languages to search in | All languages, English first (default) |
| **Minimum ads** | How many active ads an offer needs to count as scaling | 15 (default). Use 10 for small niches. |
| **Daily minimum** | How many new verified offers per run to aim for | 5 (default) |
| **Output** | Google Sheet (default) or a local Excel file | Google Sheet. Paste a sheet link, or let the hunter create one in your Drive |
| **Work folder** | Where the keyword bank goes | `./offer-hunter/` (default) |

You don't need a keyword bank or a sheet. On the first run the hunter creates both and gives you the sheet link.

---

## 6. Your first run (watch it)

1. Type `/offer-hunter`, or just say *"hunt offers"*.
2. Answer its questions. It asks at most 2 rounds, then shows your settings and starts.
3. Wait 20–40 minutes. At the end you get:
   - a summary in the chat: new offers, offers whose ad count went up, offers that stopped running, and the top 3 of the day;
   - your master Google Sheet with 4 tabs: Offers, Pending, History, Search Log.
4. **Check 2–3 findings by hand.** Open the Ad Library link: does it really have that many active ads? Open the landing page: is it really a downloadable digital product with direct checkout?
5. If the hunter brought you products you couldn't make, your filter is too loose. Run it again and choose *"change some"* to tighten the filter.

### Where your answers are saved

They're saved in **`launch-profile.md`** at the root of your work folder. The skills write this file themselves. You can open it to see your settings, but you never have to edit it.

### Your own rules

When a result isn't what you want, say *"add to my rules: …"*. The rule is saved in **`my-rules.md`** in your work folder, and every run of every skill reads it automatically. Updating the pack never overwrites this file.

### Changing settings later

- **For the next run:** just answer *"change some"* when it asks.
- **For a single run:** put the change in the command, for example `/offer-hunter min ads 10, niches: pet care`.

---

## 7. Automate it (only after 2–3 good runs)

Your first manual run saved your settings, so a scheduled run can work with nobody watching. Create a daily task:

- **On your computer:** in the Claude desktop app, create a scheduled task.
- **On the web:** go to claude.ai/code → Routines.

Pick a time, for example 8:00 AM, and use exactly this prompt:

```
Run the offer-hunter skill in unattended mode, using the saved settings
in launch-profile.md. Follow the skill to the letter; do not run the
routine from memory. If the skill is not available, stop and report it.
Context: you are the daily scheduled run.
```

- In unattended mode the skill **never asks questions**. If an essential setting is missing, it stops and tells you which one.
- To change the routine, update the pack (step 8). Never edit the scheduled task.

---

## 8. Updating the pack

When new skills or improvements are released:

```
/plugin marketplace update one-hour-launch-skills
```

Then restart Claude Code. Your settings and your sheet are not affected.

---

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| `/plugin marketplace add` says "repository not found" | You haven't accepted the GitHub invite yet, or git isn't logged in to GitHub. Run `gh auth login`. |
| The skills don't show up after installing | Restart Claude Code, or start a new session. |
| "I don't have access to ads_library_search" | The Meta Ads connector isn't connected. Connect it at claude.ai → Settings → Connectors, then start a **new** session. |
| Every Ad Library search returns 0 results | The Ad Library is limiting searches. The skill waits 3–5 minutes on its own. Don't log out. |
| It finds products you can't make | Your filter is too loose. Tighten it with *"change some"*. |
| Your own page shows up as competition | Add it to your own pages with *"change some"*, then delete its row from the sheet. |
| The sheet is broken or has duplicate rows | In Google Sheets: File → Version history, restore the version from before the run (its start time is in the Search Log tab). Excel users: restore `offers-master-backup.xlsx`. |
| "Can't write to the sheet" | Connect the Google Drive connector (claude.ai → Settings → Connectors) and start a new session. The day's results are kept in a `pending-sync` file and synced on the next run. |
| A scheduled run stopped with "missing settings" | Run the skill once yourself, in interactive mode, to save your settings. |

---

**Next:** read the guide for each skill in `guides/`, which covers daily use, tips and common problems.
