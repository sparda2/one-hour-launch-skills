# One Hour Launch Skills

> **Students: start with [`en/START-HERE.md`](en/START-HERE.md).** Fastest path: upload `en/skills/offer-hunter/SKILL.md` to a Claude Code session and say *"Set this up for me step by step"*. The skill guides you from zero to your first hunt.

The full launch system as Claude Code skills.

- **`en/` — plugin `one-hour-launch`: the product.** English is the master version: new skills and rule changes are written here first.
- **`es/` — plugin `one-hour-launch-es`:** Spanish mirror, kept in sync for internal use and a future Spanish edition.

| Step | English (`en/skills/`) | Spanish (`es/skills/`) | Status |
|---|---|---|---|
| 1. Find winning offers | `offer-hunter` | `cazador-de-ofertas` | ✅ v1 |
| 2. Model the product | `product-modeler` | `modelar-producto` | 🚧 to build |
| 3. Model the funnel | `funnel-modeler` | `modelar-funnel` | 🚧 to build |
| 4. Create the ads | `ads-routine` | `rutina-de-ads` | ✅ v2 |

Each step's output feeds the next one: winning offer → product spec → funnel → ads.

## Layout

```
.claude-plugin/marketplace.json   ← marketplace: lists both plugins
en/                               ← plugin "one-hour-launch" (master)
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  START-HERE.md                   ← student install & setup guide
  guides/                         ← per-skill usage guides
es/                               ← plugin "one-hour-launch-es" (mirror)
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  guias/v1-originales/            ← original PDF guides (pre-plugin; Spanish guide update pending)
```

Every skill exists in both languages with the same rules. Skill names differ per language so both plugins can be installed side by side without collisions.

## Install

In Claude Code (local, cloud session, or a Grok Bot cloud computer with Claude Code installed):

```
/plugin marketplace add sparda2/one-hour-launch-skills
/plugin install one-hour-launch@one-hour-launch-skills
```

Update later with `/plugin marketplace update one-hour-launch-skills`.

To auto-enable in a workspace repo (so every cloud session opening it has the skills), add to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "one-hour-launch-skills": { "source": { "source": "github", "repo": "sparda2/one-hour-launch-skills" } }
  },
  "enabledPlugins": { "one-hour-launch-es@one-hour-launch-skills": true }
}
```

## How settings work

No config files to edit. Each skill **asks for its settings** at the start of a run, then saves the answers to `launch-profile.md` in the user's project, with one section per skill and `## Shared` for settings every skill uses. Later runs offer "same / change some / start fresh". Unattended runs (scheduled, Grok Bot, `claude -p`) never ask questions: they use the saved profile and stop if an essential setting is missing. Users add their own rules in `my-rules.md`, which every skill reads and pack updates never overwrite.

## Rule for editing

The skills are the single source of truth: scheduled runs only point at them. Change a rule in `en/` first, then mirror it to `es/` in the same commit.
