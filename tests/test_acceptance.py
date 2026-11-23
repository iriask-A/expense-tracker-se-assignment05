"""Acceptance criteria AC1-AC5 (see AGENTS.md). Golden outputs were captured from the
baseline version BEFORE any refactoring and must stay identical afterwards."""
import json

import pytest

from expense_tracker.calculator import total, totals_by_category
from expense_tracker.models import Expense
from expense_tracker.report import render_report, summary_line
from expense_tracker.storage import load, save

ITEMS = [
    Expense("Lunch", 12.5, "food"),
    Expense("Bus", 1.2, "transport"),
    Expense("Coffee", 3.3, "food"),
]


def test_ac1_total():
    assert total(ITEMS) == pytest.approx(17.0)


def test_ac2_totals_by_category():
    assert totals_by_category(ITEMS) == pytest.approx({"food": 15.8, "transport": 1.2})


def test_ac3_text_report_golden():
    assert render_report(ITEMS, "text") == (
        "Lunch: 12.50 (food)\nBus: 1.20 (transport)\nCoffee: 3.30 (food)\nTOTAL: 17.00"
    )


def test_ac4_storage_round_trip(tmp_path):
    path = tmp_path / "e.json"
    save(ITEMS, str(path))
    assert load(str(path)) == ITEMS


def test_ac5_csv_report_golden():
    assert render_report(ITEMS, "csv") == (
        "description,amount,category\nLunch,12.50,food\nBus,1.20,transport\n"
        "Coffee,3.30,food\nTOTAL,17.00,"
    )


def test_ac5_json_report_structure():
    data = json.loads(render_report(ITEMS, "json"))
    assert set(data) == {"expenses", "total", "by_category"}
    assert data["total"] == pytest.approx(17.0)
    assert len(data["expenses"]) == 3


@pytest.mark.parametrize(
    "fmt, expected",
    [
        ("text", "3 expenses, total 17.00"),
        ("csv", "count,total\n3,17.00"),
        ("json", '{"count": 3, "total": 17.0}'),
    ],
)
def test_ac5_summary_golden(fmt, expected):
    assert summary_line(ITEMS, fmt) == expected


@pytest.mark.parametrize("fn", [render_report, summary_line])
def test_ac5_unknown_format_rejected(fn):
    with pytest.raises(ValueError):
        fn(ITEMS, "xml")
