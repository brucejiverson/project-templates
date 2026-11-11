# Snippets

Code worth reusing, kept here to copy, not to install. Copy only the function you need into the new
project's `src/`, add a test for it there, and let that project's ruff and pyright check it.
Moved here from the retired `common_python_tools` repo (2026-11-11).

| File | What is in it |
|------|---------------|
| [util.py](util.py) | Colored console logger and file logging (`get_formatted_logger`), JSON config read and nested update, busy-wait millisecond sleep, cosine similarity of two strings, latest git tag / commit hash |
| [example_ui.py](example_ui.py) | FreeSimpleGUI patterns: toggle switches, multi-page navigation, input cleaning, async event loop, config updates, running a subprocess from the UI |

Things to know before copying from `util.py`:

- Importing the whole file has side effects: it creates a `logs/` folder, prints the working directory and
  sets up a root logger. Copy individual functions instead of the file.
- Paths (`logs/`, `config.json`) are worked out from the file's own location, three folders up. Adjust them.
- `update_dict_with_value` updates **every** matching key in nested dicts, not only the first.
- `wait_for_ms` had its unit conversion backwards (it waited 1,000,000x too long); fixed here when it moved.
