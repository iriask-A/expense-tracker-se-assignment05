# expense-tracker

A tiny dependency-free command-line expense tracker (Python 3.12). Data is stored in a local
JSON file (`expenses.json` by default, change with `--file`).

## Setup
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements-dev.txt

## Usage
    export PYTHONPATH=src
    python -m expense_tracker.cli add "Lunch" 12.5 food
    python -m expense_tracker.cli report --format csv      # text | csv | json
    python -m expense_tracker.cli report --summary

## Checks
    pytest -v
    ruff check .
    mypy src
    python -m compileall -q src      # there is no packaging/build step

See `AGENTS.md` for rules for AI agents and contributors.
