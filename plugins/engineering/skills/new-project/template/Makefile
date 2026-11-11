.PHONY: install dev fix lint typecheck test clean

# Create .venv from uv.lock and install the git hooks
install:
	uv sync
	uv run pre-commit install --hook-type pre-commit --hook-type pre-push

# Full validation: lint, typecheck, test. Run before every commit.
dev: lint typecheck test

# Auto-fix formatting and lint
fix:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run pyright

# Hardware tests are skipped by default; run them with: uv run pytest -m hardware
test:
	uv run pytest -m "not hardware" --cov=__PACKAGE__ --cov-report=term-missing

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
