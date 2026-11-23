import argparse
import sys

from .models import Expense
from .report import render_report, summary_line
from .storage import load, save


def main(argv=None):
    p = argparse.ArgumentParser(prog="expense-tracker")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("description")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("--file", default="expenses.json")
    r = sub.add_parser("report")
    r.add_argument("--format", default="text")
    r.add_argument("--summary", action="store_true")
    r.add_argument("--file", default="expenses.json")
    args = p.parse_args(argv)

    if args.cmd == "add":
        try:
            expense = Expense(args.description, args.amount, args.category)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        try:
            items = load(args.file)
        except FileNotFoundError:
            items = []
        items.append(expense)
        save(items, args.file)
        print("added")
    else:
        items = load(args.file)
        if args.summary:
            print(summary_line(items, args.format))
        else:
            print(render_report(items, args.format))
    return 0


if __name__ == "__main__":
    sys.exit(main())
