from dataclasses import dataclass


@dataclass
class Expense:
    description: str
    amount: float
    category: str
