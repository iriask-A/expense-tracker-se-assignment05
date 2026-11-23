import math
from dataclasses import dataclass


@dataclass
class Expense:
    description: str
    amount: float
    category: str

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("description must not be empty")
        if not self.category.strip():
            raise ValueError("category must not be empty")
        if not math.isfinite(self.amount) or self.amount <= 0:
            raise ValueError("amount must be a finite number greater than 0")
