# The Offer Hunter

Skill: `/offer-hunter` · Suggested schedule: daily, 8:00 AM · Your market radar

## 1. What it is and what you need

Every morning the hunter sweeps Meta's Ad Library looking for offers that ARE scaling (advertisers with many active ads for the same product, running for several days) and logs them in a master Excel with their history and trend. It's the first routine of the day because it feeds all the others: it produces product ideas with proven demand and tested sales angles.

| Requirement | What it's used for | How to know you have it |
|---|---|---|
| Meta Ads connector in Claude Code | API search of the Ad Library (`ads_library_search`) — the cheap, block-free way | Ask Claude: "do you have access to ads_library_search?" |
| Google Drive for desktop | The work folder and the Excel back themselves up | `~/Library/CloudStorage/GoogleDrive-…` exists on your Mac |
| Python with openpyxl | Read and update the master Excel without breaking it | Claude installs it if missing — do nothing |

## 2. Installation, step by step

1. Copy the `offer-hunter` folder (the one you received, with its SKILL.md) to `~/.claude/skills/`. It should end up as `~/.claude/skills/offer-hunter/SKILL.md`.
2. Open that SKILL.md in any editor and fill in the CONFIGURATION block with YOUR data. The table in the next section explains each field and where to get it.
3. Connect in Claude Code what the routine needs (requirements table above). If a connector is missing, the routine will fail at that step and tell you — better to connect it first.
4. Restart Claude Code (or open a new session) so the skill shows up in the list.
5. DON'T schedule it yet: first the on-demand test in section 3.

> **Golden rule.** The skill you received is a TEMPLATE of a real operation: every rule exists because something failed one day and cost money. Adapt the data (paths, accounts, criteria) but DON'T delete rules you don't understand — first ask your Claude what that rule protects.

### The CONFIGURATION fields, one by one

| Field | What it is | Where to get it / example |
|---|---|---|
| WORK_FOLDER | The folder where everything for the hunter lives | Create it INSIDE your Drive folder so it backs up on its own. E.g. `…/My Drive/offer-hunter` |
| MASTER_EXCEL | The single file with all the offers | A fixed name, e.g. `offers-master.xlsx`. On the first run tell Claude: "create it for me with the sheets Offers / Pending / History / Log" |
| YOUR_FILTER | YOUR definition of a replicable product — the heart of the routine | 2-3 sentences. E.g. "downloadable digital toolkits, low ticket, that I can produce with AI in days; no video courses or services" |
| NICHE_CIRCLES | The hunting order | Circle 1 = your current niches; 2 = same buyer, other topic; 3 = adjacent. List 3-5 per circle |
| OWN_PAGES | Your pages, to EXCLUDE them | The page_id comes from the library: search your page → click → the URL shows `view_all_page_id=NUMBER` |
| KEYWORD_BANK | Your keyword bank by category and language | Ask Claude: "generate an initial bank of 100 keywords for my niche in ES/EN" and save it as a file in the folder |
| MIN_ADS | "Is scaling" threshold | Start with 15. If your niche is small, drop to 10 — but note that you lowered the bar |
| DAILY_FLOOR | Minimum new verified findings | Start with 5. The summary must be honest if it isn't reached — never pad with mediocre ones |

## 3. First run (on demand, with you watching)

1. Type `/offer-hunter` in Claude Code. The run takes 20-40 minutes.
2. At the end you should have: the summary in the chat (new / increased / shut off / top 3) and the Excel with its 4 sheets populated.
3. Validate 2-3 findings by hand: open each one's library link (does it really have that many active ads?) and its landing (is it really a downloadable digital product with direct checkout?).
4. If it brought you things you couldn't replicate: the problem is YOUR_FILTER — tighten it and run again. The hunter's quality IS your filter's quality.

> **What to expect the first days.** For the first 2-3 days the hunter explores and burns the obvious keywords; the Excel grows fast. Then it stabilizes: few new ones per day, but the HISTORY starts to be worth gold — seeing an offer go from 20 to 70 ads in a week is the strongest buy signal there is.

## 4. Scheduling it (once it went well 2-3 times)

Tell Claude Code: "create a scheduled task that runs every day at 8:00 AM with this prompt" — and paste exactly this pointer:

```
Read the ENTIRE file ~/.claude/skills/offer-hunter/SKILL.md with
the Read tool and execute it to the letter as if it were this
prompt. Summarizing it or running the routine from memory is forbidden.
If the file doesn't exist or can't be read: STOP without running
anything and report that the skill is not available.
Context: you are the daily scheduled run at 8:00 AM.
```

- The pointer makes the scheduled task and the manual run ALWAYS the same routine: the skill is the single source of truth.
- Editing the routine = editing the SKILL.md. The scheduled task is never touched again.
- To pause it: "pause the scheduled task" (the skill stays available on demand). To resume: "activate it again".

## 5. Day-to-day management

- **Every morning (2 min):** read the summary. What matters: the ones that INCREASED (deltas like 40→70) and the top 3.
- **When an offer rises strongly several days in a row:** it's a candidate to clone IN YOUR FORMAT — move it to your list of products to make (the hunter closes each finding with "the product I would make").
- **Once a week (10 min):** prune the Pending sheet (what never took off, out) and review the Log to see which keywords are already burned.
- Don't edit the Excel by hand while the routine is running — there's an automatic backup, but better not to cross paths.
- Feed the keyword bank when you discover a new angle (a profession, a language, a format).

## 6. Common problems

| Symptom | Cause | Solution |
|---|---|---|
| The library returns 0 on every search | Rate-limit from many consecutive queries | Cool down 3-5 minutes and continue. It's NOT your session: don't log out |
| Brings findings you can't replicate | YOUR_FILTER is loose | Tighten the definition and tell Claude to re-evaluate the latest findings against the new filter |
| Your own page shows up as competition | Missing from OWN_PAGES | Add its page_id to the config and delete the row from the Excel |
| Counts that don't match what you see | You're reading "N ads use this creative" (variants of ONE ad) | The real count is the advertiser PAGE total (`view_all_page_id`) |
| Broken Excel or duplicate rows | Run interrupted mid-write | Restore the `*-backup.xlsx` (created before every run) and relaunch |

## 7. Checklist for this skill

- [ ] Drive folder created and path set in WORK_FOLDER.
- [ ] YOUR_FILTER written in your own words (and it's demanding).
- [ ] OWN_PAGES with the page_ids of ALL your pages.
- [ ] Initial keyword bank generated.
- [ ] First run validated by hand (2-3 findings checked).
- [ ] Scheduled at 8:00 AM with the pointer.
- [ ] You review the summary every morning and prune Pending every week.
