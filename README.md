# One Hour Launch Skills

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
  guides/                         ← setup & usage guides (Markdown)
es/                               ← plugin "one-hour-launch-es" (mirror)
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  guias/                          ← setup & usage guides (PDF)
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

## Rule for editing

The skills are the single source of truth: scheduled runs only point at them. Change a rule in `en/` first, then mirror it to `es/` in the same commit.
