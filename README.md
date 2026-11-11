# Project Templates

One place for how Bruce's projects start and the agents they all share. It is two things:

1. **A Claude Code plugin marketplace** with one plugin, `engineering`: shared subagents and skills. Projects
   install it instead of copying agents, so an improvement made here reaches every project.
2. **The new-project template**, which lives inside the `new-project` skill: uv, ruff, pyright, pre-commit, CI,
   a `CLAUDE.md` with the working rules, and the concept → implementation → design map documents.

## Start a new project

In Claude Code, from any folder: *"create a new project called seed-drum"*. That runs the `new-project` skill.

Without Claude:

```bash
bash plugins/engineering/skills/new-project/new_project.sh seed-drum        # creates ~/Code/seed-drum
```

## Use the agents in an existing project

Add to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "project-templates": { "source": { "source": "github", "repo": "brucejiverson/project-templates" } }
  },
  "enabledPlugins": { "engineering@project-templates": true }
}
```

To try local, unpushed changes, point the source at the folder instead:
`{ "source": "directory", "path": "/home/bruce/Code/project-templates" }`.

## What is in the `engineering` plugin

| Agents | For |
|--------|-----|
| `python-pro`, `code-reviewer`, `debugger`, `test-automator`, `refactoring-specialist` | Day-to-day software work |
| `documentation-engineer`, `performance-engineer` | Docs and speed |
| `systems-engineer` | V-model requirements, concept selection, traceability |
| `mechanical-designer`, `embedded-systems` | Hardware calculations and firmware |

| Skills | For |
|--------|-----|
| `new-project` | Make a project folder and take it through the three planning documents |
| `new-hardware-module` | Take a machine or device through ConOps → requirements → concept → sizing → electrical → test plan |
| `part-data` | One sourced fact sheet per bought part |
| `cable-drawing` | WireViz cable drawings with gauge, shield, twist and revision rules |

## Layout

```
.claude-plugin/marketplace.json        the marketplace
plugins/engineering/
├── agents/                            subagents
└── skills/
    ├── new-project/
    │   ├── new_project.sh             makes the folder
    │   └── template/                  everything a new project starts with
    ├── new-hardware-module/templates/ release notes and unit traveler
    ├── part-data/
    └── cable-drawing/
snippets/                              reusable code to copy (from the old common_python_tools)
```
