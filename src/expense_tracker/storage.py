import json

from .models import Expense


def save(expenses, path):
    with open(path, "w") as f:
        json.dump([e.__dict__ for e in expenses], f)


def load(path):
    with open(path) as f:
        return [Expense(**d) for d in json.load(f)]
