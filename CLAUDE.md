# CLAUDE.md - project-templates

This repo is a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) plus the template every new
project starts from. See `README.md` for the layout.

## Rules for changing it

- **Generic only.** Anything here ships to every project. Project-specific rules, paths and part names stay in
  that project's own `CLAUDE.md`, plugins or skills. If an improvement comes from a project (e.g.
  recursive_robotics), strip its specifics before bringing it here.
- **The template is a real project.** After changing anything under `plugins/engineering/skills/new-project/`,
  generate one and check it passes:

  ```bash
  d=$(mktemp -d) && bash plugins/engineering/skills/new-project/new_project.sh smoke-test "$d" \
    && (cd "$d/smoke-test" && make dev); rm -rf "$d"
  ```

- `template/gitignore` is stored without the leading dot on purpose; the script renames it.
- Placeholders in the template: `__PROJECT__` (folder/distribution name) and `__PACKAGE__` (Python package).
- Agents say which project file wins (the project's `CLAUDE.md`). Don't add made-up inter-agent protocols,
  canned "delivery messages", or references to agents that don't exist here.
- Bump `version` in `plugins/engineering/.claude-plugin/plugin.json` when agents or skills change, so projects
  pick up the update.
- Validate the JSON manifests after editing them: `python3 -m json.tool .claude-plugin/marketplace.json`.
