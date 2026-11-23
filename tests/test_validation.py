"""Regression tests for risk R1: invalid amounts/fields must be rejected (mitigation M1)."""
import pytest

from expense_tracker.cli import main
from expense_tracker.models import Expense


@pytest.mark.parametrize("amount", [-5, 0, float("nan"), float("inf"), float("-inf")])
def test_invalid_amounts_rejected(amount):
    with pytest.raises(ValueError):
        Expense("x", amount, "food")


@pytest.mark.parametrize("desc, cat", [("", "food"), ("   ", "food"), ("x", ""), ("x", "  ")])
def test_empty_text_rejected(desc, cat):
    with pytest.raises(ValueError):
        Expense(desc, 1.0, cat)


def test_valid_expense_still_accepted():
    assert Expense("Lunch", 12.5, "food").amount == 12.5


@pytest.mark.parametrize("amount", ["-5", "nan", "inf", "0"])
def test_cli_add_rejects_invalid_amount_and_writes_nothing(tmp_path, capsys, amount):
    path = tmp_path / "e.json"
    code = main(["add", "x", amount, "food", "--file", str(path)])
    assert code == 2
    assert not path.exists()
    assert "error:" in capsys.readouterr().err


def test_cli_add_valid_returns_zero(tmp_path):
    path = tmp_path / "e.json"
    assert main(["add", "Lunch", "12.5", "food", "--file", str(path)]) == 0
    assert path.exists()
