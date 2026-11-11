#!/usr/bin/env bash
# Create a new project from ./template.
#
#   new_project.sh <name> [parent_dir]
#
# <name> is the folder and distribution name (e.g. seed-drum); the Python package is the same name in
# snake_case (seed_drum). parent_dir defaults to ~/Code. Refuses to touch an existing folder.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "usage: $0 <name> [parent_dir]" >&2
    exit 2
fi

name="$1"
parent="${2:-$HOME/Code}"
if [[ ! "$name" =~ ^[a-z][a-z0-9_-]*$ ]]; then
    echo "name must be lower case letters, digits, '-' or '_', starting with a letter; got '$name'" >&2
    exit 2
fi
package="${name//-/_}"
target="$parent/$name"
template="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/template"

if [[ -e "$target" ]]; then
    echo "$target already exists; not touching it" >&2
    exit 1
fi

mkdir -p "$parent"
cp -r "$template" "$target"
cd "$target"

# Stored without the dot so it does not act as an ignore file inside the template repo.
mv gitignore .gitignore
mv src/__PACKAGE__ "src/$package"
grep -rlZ -e '__PROJECT__' -e '__PACKAGE__' . | xargs -0 sed -i -e "s/__PROJECT__/$name/g" -e "s/__PACKAGE__/$package/g"

git init -q
if command -v uv >/dev/null; then
    uv lock -q
    uv sync -q
    uv run -q pre-commit install --hook-type pre-commit --hook-type pre-push >/dev/null
    uv run -q ruff format . >/dev/null
else
    echo "uv not found: run 'make install' after installing uv" >&2
fi
git add -A
git commit -q -m "Start $name from project-templates"

echo "Created $target (package: $package)"
