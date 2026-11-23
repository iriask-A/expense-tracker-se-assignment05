"""Regression tests for risk R2: CSV quoting and formula injection (mitigation M2)."""
import csv
import io

import pytest

from expense_tracker.models import Expense
from expense_tracker.report import render_report


def _rows(items):
    return list(csv.reader(io.StringIO(render_report(items, "csv"))))


def test_comma_in_description_is_quoted_and_round_trips():
    rows = _rows([Expense("Lunch, with team", 10, "food")])
    assert rows[1] == ["Lunch, with team", "10.00", "food"]
    assert all(len(r) == 3 for r in rows)


def test_quote_in_description_round_trips():
    assert _rows([Expense('The "big" one', 10, "food")])[1][0] == 'The "big" one'


BAD = ['=HYPERLINK("http://evil.example","x")', "+1+1", "-2+3", "@SUM(A1)"]


@pytest.mark.parametrize("bad", BAD)
def test_formula_prefixes_are_neutralised(bad):
    rows = _rows([Expense(bad, 10, "food"), Expense("ok", 1, bad)])
    assert rows[1][0].startswith("'")
    assert rows[2][2].startswith("'")


def test_normal_text_is_unchanged():
    assert _rows([Expense("Lunch", 10, "food")])[1] == ["Lunch", "10.00", "food"]
