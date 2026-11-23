from expense_tracker.calculator import total, totals_by_category
from expense_tracker.models import Expense


def test_total_simple():
    assert total([Expense("a", 10.0, "food"), Expense("b", 5.5, "fun")]) == 15.5


def test_totals_by_category():
    items = [Expense("a", 10, "food"), Expense("b", 5, "food"), Expense("c", 2, "fun")]
    assert totals_by_category(items) == {"food": 15, "fun": 2}
