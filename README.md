# launch-skills

The full launch system as Claude Code skills, in **Spanish (`es/`)** and **English (`en/`)**:

| Step | Spanish (`es/skills/`) | English (`en/skills/`) | Status |
|---|---|---|---|
| 1. Find winning offers | `cazador-de-ofertas` | `offer-hunter` | ✅ v1 |
| 2. Model the product | `modelar-producto` | `product-modeler` | 🚧 to build |
| 3. Model the funnel | `modelar-funnel` | `funnel-modeler` | 🚧 to build |
| 4. Create the ads | `rutina-de-ads` | `ads-routine` | ✅ v2 |

Each step's output feeds the next one: winning offer → product spec → funnel → ads.

## Layout

```
.claude-plugin/marketplace.json   ← marketplace: lists both plugins
es/                               ← plugin "launch-engine-es"
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  guias/                          ← setup & usage guides (PDF)
en/                               ← plugin "launch-engine-en"
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  guides/                         ← setup & usage guides (Markdown)
```

Every skill exists in both languages with the same rules. Skill names differ per language so both plugins can be installed side by side without collisions.

## Install

In Claude Code (local, cloud session, or a Grok Bot cloud computer with Claude Code installed):

```
/plugin marketplace add sparda2/launch-skills
/plugin install launch-engine-en@launch-skills    # or launch-engine-es
```

Update later with `/plugin marketplace update launch-skills`.

To auto-enable in a workspace repo (so every cloud session opening it has the skills), add to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "launch-skills": { "source": { "source": "github", "repo": "sparda2/launch-skills" } }
  },
  "enabledPlugins": { "launch-engine-es@launch-skills": true }
}
```

## Rule for editing

The skills are the single source of truth: scheduled runs only point at them. Change a rule in **both** languages in the same commit.
