# Winning Offer Spy: setup checklist

Follow these steps in order. It takes about 15 minutes. Every step has a ✅ check so you know it worked before moving on. The skill's built-in wizard checks all of this for you too, but doing it beforehand means you won't need a restart.

> ⚠️ **This skill MUST run in Claude Code, not in the regular Claude chat.**
> The spy opens every competitor's landing page to verify the offer, runs for 20–40 minutes, and saves its work to your Drive. Only Claude Code can do that. In the regular chat it can't read the landing pages, so it would get stuck.

---

## Step 1: Have an active Meta ad account

Meta only lets you search the Ad Library through Claude if you have at least one **active** ad account.

1. Go to **business.facebook.com** → **Business settings** → **Ad accounts**.
2. If you don't have one, create it. If yours is disabled, reactivate it. Meta usually asks for a payment method. You don't need to run any ads.

✅ Your ad account shows as **Active**.

## Step 2: Connect Meta to Claude (the Meta MCP)

1. Go to **claude.ai → Customize → Connectors** (claude.ai/customize/connectors).
2. Click **+** → **Add custom connector**.
3. Fill in:
   - **Name:** `Meta`
   - **URL:** `https://mcp.facebook.com/ads`
4. Click **Add**, then **Connect**.
5. Log in with the Facebook account that manages your ad account, and **approve all the permissions** it asks for (ads, business, pages).

✅ The Meta connector shows **Connected**.

## Step 3: Connect Google Drive AND Google Sheets

They are **two separate connectors**, and you need both.

1. On the same Connectors page, find **Google Drive** → **Connect** → choose your Google account → **Allow**.
2. Find **Google Sheets** → **Connect** → **Allow**.

✅ Google Drive and Google Sheets both show **Connected**.

## Step 4: Install the skill

1. Download `dist/winning-offer-spy-EN.zip` from the pack.
2. Go to **claude.ai → Settings → Capabilities → Skills → Upload skill** and choose the ZIP.

✅ "winning-offer-spy" appears in your skills list. It's also available in Claude Code cloud sessions automatically.

## Step 5: Open Claude Code in the cloud with full internet access

1. Open the **Claude desktop app → Code → Cloud**, or go to **claude.ai/code**.
2. Start a new session. If it asks for a repository, any of yours is fine; the spy saves everything in your Drive.
3. Turn on **full internet access**, so the spy can open competitors' landing pages:
   - In the session's title bar, click the **environment menu** → **Edit**.
   - **Network access → Full** → **Save**.
   - **Start a new session.** The change only applies to sessions started after saving.
4. In the new session:
   - Open its **connectors menu** and check that **Meta**, **Google Drive** and **Google Sheets** are switched **on**.
   - Pick the **Auto** permission mode, so the hunt doesn't stop to ask for approval at every step.

## Step 6: Check everything works (copy these prompts)

Send these one at a time in your new Claude Code session:

| Prompt | What you should see |
|---|---|
| `Do you have access to ads_library_search?` | "Yes" |
| `Run a test search in the Ad Library: "shoes", US, active ads.` | A few ads, plus an estimated total count |
| `Open https://gumroad.com and tell me its title.` | The page title. That means full internet access works |

> If Claude tries `facebook.com` directly and gets a **403**, that's normal. Facebook blocks automated visits. The Ad Library is read through the Meta connector, so it isn't affected.

## Step 7: Set up and run your first hunt

Type:

```
Set up the Winning Offer Spy for me step by step, then run my first hunt.
```

The wizard will:
- create your **"Winning Offer Spy"** folder and master Google Sheet in your Drive, and give you the link;
- ask for your **product filter**, **niches**, **Facebook pages**, **languages** and **thresholds**, in at most 2 rounds;
- run a quick test, then your first hunt (20–40 minutes). You can close the window, because it keeps running in the cloud.

✅ You get a summary with your top 3 offers, and your sheet is filled in.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "I don't have access to ads_library_search" | The Meta connector isn't connected, or it's switched off in this session's connectors menu. Fix it (Step 2), then start a new session |
| The Ad Library returns an ad account error | You have no **active** ad account (Step 1). After activating it, disconnect and reconnect the Meta connector |
| "Can't create or write the sheet" | Google Sheets isn't connected. You need it **in addition to** Google Drive (Step 3) |
| Landing pages won't open, or "EGRESS_BLOCKED" | Network access isn't set to **Full**, or you're still in a session started before you changed it (Step 5) |
| `facebook.com` returns 403 | Normal, nothing to fix |
| It keeps asking for approval | Switch the session to **Auto** permission mode |
| You're in the regular Claude chat | Move to **Claude Code → Cloud** (Step 5). The spy can't read landing pages from the regular chat |
