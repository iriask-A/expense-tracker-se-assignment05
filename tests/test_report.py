from expense_tracker.models import Expense
from expense_tracker.report import render_report


def test_text_report_contains_total():
    out = render_report([Expense("tea", 2.5, "food")], "text")
    assert "TOTAL: 2.50" in out
