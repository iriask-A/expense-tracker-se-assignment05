"""Report rendering. Each output format is a small strategy object with two methods."""
import csv
import io
import json
from typing import Protocol

from .calculator import total, totals_by_category
from .models import Expense


class Formatter(Protocol):
    def render(self, expenses: list[Expense]) -> str: ...

    def summary(self, expenses: list[Expense]) -> str: ...


class TextFormatter:
    def render(self, expenses: list[Expense]) -> str:
        lines = [f"{e.description}: {e.amount:.2f} ({e.category})" for e in expenses]
        lines.append(f"TOTAL: {total(expenses):.2f}")
        return "\n".join(lines)

    def summary(self, expenses: list[Expense]) -> str:
        return f"{len(expenses)} expenses, total {total(expenses):.2f}"


_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _csv_safe(value: str) -> str:
    """Neutralise spreadsheet formula injection (OWASP CSV injection guidance)."""
    return "'" + value if value.startswith(_FORMULA_PREFIXES) else value


def _csv_lines(rows: list[list[str]]) -> str:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue().rstrip("\n")


class CsvFormatter:
    def render(self, expenses: list[Expense]) -> str:
        rows = [["description", "amount", "category"]]
        for e in expenses:
            rows.append([_csv_safe(e.description), f"{e.amount:.2f}", _csv_safe(e.category)])
        rows.append(["TOTAL", f"{total(expenses):.2f}", ""])
        return _csv_lines(rows)

    def summary(self, expenses: list[Expense]) -> str:
        return f"count,total\n{len(expenses)},{total(expenses):.2f}"


class JsonFormatter:
    def render(self, expenses: list[Expense]) -> str:
        data = {
            "expenses": [e.__dict__ for e in expenses],
            "total": total(expenses),
            "by_category": totals_by_category(expenses),
        }
        return json.dumps(data, indent=2)

    def summary(self, expenses: list[Expense]) -> str:
        return json.dumps({"count": len(expenses), "total": total(expenses)})


FORMATTERS: dict[str, Formatter] = {
    "text": TextFormatter(),
    "csv": CsvFormatter(),
    "json": JsonFormatter(),
}


def get_formatter(fmt: str) -> Formatter:
    try:
        return FORMATTERS[fmt]
    except KeyError:
        raise ValueError("unknown format") from None


def render_report(expenses: list[Expense], fmt: str) -> str:
    return get_formatter(fmt).render(expenses)


def summary_line(expenses: list[Expense], fmt: str) -> str:
    return get_formatter(fmt).summary(expenses)
