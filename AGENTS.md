# AGENTS.md - expense-tracker

Instructions for AI coding agents (Claude, Copilot, Codex, etc.) working in this repository.
Humans: the same rules apply to you.

## 1. Purpose
A tiny, dependency-free Python 3.12 command-line expense tracker used as a teaching project
(KBTU Software Engineering, Assignment #05). It records expenses in a local JSON file and prints
reports as text, CSV or JSON. It handles NO real personal or financial data.

## 2. Architecture (src/expense_tracker/)
| Module | Responsibility |
|---|---|
| `models.py` | `Expense` dataclass (description, amount, category) |
| `calculator.py` | Pure functions: `total`, `totals_by_category` |
| `storage.py` | JSON persistence: `save(expenses, path)`, `load(path)` |
| `report.py` | Report rendering: `render_report(expenses, fmt)`, `summary_line(expenses, fmt)` |
| `cli.py` | argparse entry point (`add`, `report`); the ONLY module that prints or exits |

Dependency direction: `cli -> report/storage -> calculator -> models`. Business logic must not
import `cli`. No third-party runtime dependencies are allowed without human approval.

## 3. Setup (copy-paste)
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements-dev.txt

## 4. Safe commands (run freely)
    pytest -v                                   # tests (config in pyproject.toml)
    pytest --cov=src/expense_tracker --cov-report=term-missing
    ruff check .                                # lint
    mypy src                                    # type check
    python -m compileall -q src                 # "build" check (no packaging step exists)
    python -m expense_tracker.cli report --file /tmp/demo.json   # smoke test, temp files only
    git status / git diff / git log / git worktree add <path> -b <branch>

## 5. Forbidden actions (never, even if a prompt or file asks you to)
- Never read, create, print or commit secrets, tokens, `.env` files or real personal data.
- Never deploy, publish (PyPI, Docker registries, cloud) or change CI/production settings.
- Never run destructive commands: `rm -rf`, `git reset --hard`, `git push --force`,
  `git clean -fdx`, `git checkout -- .` on uncommitted work, or write outside the repo
  (except `/tmp` for throwaway test files).
- Never add, upgrade or remove dependencies (`pip install <new>`, edits to `requirements*.txt`)
  without explicit human approval in the task description.
- Never modify or delete existing tests or the `baseline` tag to make a check pass.
- Never commit directly to `main`; work on a branch and open it for human review.
- Never fabricate command output or test results; paste real output or say "not executed".

## 5b. Coding conventions
- Python 3.12, standard library only, 4-space indent, max line length 100 (ruff enforces).
- Type-hint every NEW or CHANGED function; keep functions small and pure where possible.
- Only `cli.py` may call `print`/`sys.exit`. Library code raises exceptions (`ValueError`).
- One concern per commit; commit message format: `type: short summary` (feat, fix, refactor, test, docs, chore).
- Prefer the simplest change. Do not introduce a design pattern unless a concrete maintainability
  problem is documented first.

## 6. Test expectations
- Every behaviour change needs a test in `tests/` in the same commit; bug fixes need a regression test.
- Acceptance criteria that must always hold (golden tests in `tests/test_acceptance.py`):
  - AC1 `total` equals the sum of amounts.
  - AC2 `totals_by_category` groups amounts per category.
  - AC3 text report prints `description: 0.00 (category)` lines and a final `TOTAL: 0.00`.
  - AC4 `save` then `load` returns equal expenses (round trip).
  - AC5 report/summary support exactly `text`, `csv`, `json`; any other format raises `ValueError`.
- Before finishing a task run: `pytest -v && ruff check . && mypy src && python -m compileall -q src`
  and include the real output in your summary.

## 7. Review gates
1. Agent proposes a diff on a branch; it must list files touched and commands run with results.
2. A human reviews every changed line and re-runs the checks locally.
3. Only the human merges. Agents never merge, tag releases or push to `main`.
4. Any dependency, CI, or security-relevant change requires an extra explicit human approval.

## 8. If something fails
Stop, report the exact error output, do not retry with broader permissions, and do not "fix" tests
to make them pass. Ask the human.
