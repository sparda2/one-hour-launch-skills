# The Offer Hunter

Skill: `/offer-hunter` · Suggested schedule: daily, 8:00 AM · Your market radar

## 1. What it is and what you need

Every morning the hunter sweeps Meta's Ad Library looking for offers that ARE scaling (advertisers with many active ads for the same product, running for several days) and logs them in a master Google Sheet in your Drive, with their history and trend. It's the first routine of the day because it feeds all the others: it produces product ideas with proven demand and tested sales angles.

| Requirement | What it's used for | How to know you have it |
|---|---|---|
| Meta Ads connector in Claude Code | API search of the Ad Library (`ads_library_search`) — the cheap, block-free way | Ask Claude: "do you have access to ads_library_search?" |
| Google Drive connector | Read and write your master Google Sheet | Ask Claude: "can you create a Google Sheet in my Drive?" |

## 2. Installation and settings

Install the pack by following **START-HERE.md**. There's no config file to fill in. On the first run the hunter asks you for these settings and saves them in the **Settings** tab of your "Offer Hunter — Master" Google Sheet:

| Setting | What it is | Example / default |
|---|---|---|
| Your filter | YOUR definition of a product you can replicate. It's the heart of the routine. | 2-3 sentences, e.g. "downloadable digital toolkits, low ticket, that I can produce with AI in days; no video courses or services" |
| Niche circles | The order the hunt follows | Circle 1 = your current niches; 2 = same buyer, other topic; 3 = adjacent. List 3-5 per circle |
| Own pages | Your pages, so the hunter EXCLUDES them | The page_id comes from the library: search your page → click → the URL shows `view_all_page_id=NUMBER` |
| Languages | Where to hunt | All languages, English first (default) |
| Min ads | The "is scaling" threshold | 15 (default). If your niche is small, drop to 10, but note that you lowered the bar |
| Daily floor | Minimum new verified findings per run | 5 (default). The summary must be honest if it isn't reached. Never pad with mediocre ones |
| Master sheet | Where everything is saved | Created on the first run in an "Offer Hunter" folder in your Drive. Tabs: Offers, Pending, History, Search Log, Keywords, Settings, My Rules |

On later runs it shows your saved settings and asks: *"Hunt with these, change some, or start fresh?"* For a one-off change, put it in the command: `/offer-hunter min ads 10`.

> **Golden rule.** This skill comes from a real operation: every rule in it exists because something failed one day and cost money. Don't delete rules you don't understand. First ask your Claude what that rule protects.

## 3. First run (on demand, with you watching)

1. Type `/offer-hunter` in Claude Code and answer its questions. The run takes 20-40 minutes.
2. At the end you should have: the summary in the chat (new / increased / shut off / top 3) and the master sheet with its 4 tabs populated.
3. Validate 2-3 findings by hand: open each one's library link (does it really have that many active ads?) and its landing (is it really a downloadable digital product with direct checkout?).
4. If it brought you things you couldn't replicate: the problem is your filter. Tighten it (*"change some"*) and run again. The hunter's quality IS your filter's quality.

> **What to expect the first days.** For the first 2-3 days the hunter explores and burns the obvious keywords; the sheet grows fast. Then it stabilizes: few new ones per day, but the HISTORY starts to be worth gold — seeing an offer go from 20 to 70 ads in a week is the strongest buy signal there is.

## 4. Scheduling it (once it went well 2-3 times)

Create a daily task: a scheduled task in the Claude desktop app, or claude.ai/code → Routines on the web. Set it for 8:00 AM with exactly this prompt:

```
Run the offer-hunter skill in unattended mode, using the saved settings
in the Settings tab of the "Offer Hunter — Master" sheet. Follow the skill to the letter; do not run the
routine from memory. If the skill is not available, stop and report it.
Context: you are the daily scheduled run at 8:00 AM.
```

- In unattended mode the skill never asks questions. It uses your saved settings, and if an essential one is missing it stops and tells you.
- The skill is the single source of truth. Updating the pack updates the routine, so the scheduled task is never touched again.
- To pause it, pause the scheduled task. The skill stays available on demand.

## 5. Day-to-day management

- **Every morning (2 min):** read the summary. What matters: the ones that INCREASED (deltas like 40→70) and the top 3.
- **When an offer rises strongly several days in a row:** it's a candidate to clone IN YOUR FORMAT — move it to your list of products to make (the hunter closes each finding with "the product I would make").
- **Once a week (10 min):** prune the Pending sheet (what never took off, out) and review the Log to see which keywords are already burned.
- Don't edit the sheet by hand while the routine is running. Google Sheets keeps version history, but it's better not to cross paths.
- Feed the keyword bank when you discover a new angle (a profession, a language, a format).
- Got a lesson of your own? Say "add to my rules: …". It's saved in the My Rules tab, which every run reads automatically.

## 6. Common problems

| Symptom | Cause | Solution |
|---|---|---|
| The library returns 0 on every search | Rate-limit from many consecutive queries | Cool down 3-5 minutes and continue. It's NOT your session: don't log out |
| Brings findings you can't replicate | Your filter is loose | Tighten it with *"change some"* and tell Claude to re-evaluate the latest findings against the new filter |
| Your own page shows up as competition | Missing from your own pages | Run with *"change some"*, add its page_id, and delete the row from the sheet |
| Counts that don't match what you see | You're reading "N ads use this creative" (variants of ONE ad) | The real count is the advertiser PAGE total (`view_all_page_id`) |
| Broken sheet or duplicate rows | Run interrupted mid-write | Google Sheets: File → Version history, restore the version from before the run (its start time is in the Search Log). |

## 7. Checklist for this skill

- [ ] Pack installed (START-HERE.md) and Meta Ads connector working.
- [ ] Your filter written in your own words (and it's demanding).
- [ ] Your own pages given with the page_ids of ALL of them.
- [ ] First run validated by hand (2-3 findings checked).
- [ ] Scheduled at 8:00 AM with the unattended prompt.
- [ ] You review the summary every morning and prune Pending every week.
