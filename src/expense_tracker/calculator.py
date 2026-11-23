from .models import Expense


def total(expenses):
    return sum(e.amount for e in expenses)


def totals_by_category(expenses):
    result = {}
    for e in expenses:
        result[e.category] = result.get(e.category, 0) + e.amount
    return result
