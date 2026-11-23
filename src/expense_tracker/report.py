import json

from .calculator import total, totals_by_category


def render_report(expenses, fmt):
    if fmt == "text":
        lines = [f"{e.description}: {e.amount:.2f} ({e.category})" for e in expenses]
        lines.append(f"TOTAL: {total(expenses):.2f}")
        return "\n".join(lines)
    elif fmt == "csv":
        lines = ["description,amount,category"]
        for e in expenses:
            lines.append(f"{e.description},{e.amount:.2f},{e.category}")
        lines.append(f"TOTAL,{total(expenses):.2f},")
        return "\n".join(lines)
    elif fmt == "json":
        data = {
            "expenses": [e.__dict__ for e in expenses],
            "total": total(expenses),
            "by_category": totals_by_category(expenses),
        }
        return json.dumps(data, indent=2)
    else:
        raise ValueError("unknown format")


def summary_line(expenses, fmt):
    if fmt == "text":
        return f"{len(expenses)} expenses, total {total(expenses):.2f}"
    elif fmt == "csv":
        return f"count,total\n{len(expenses)},{total(expenses):.2f}"
    elif fmt == "json":
        return json.dumps({"count": len(expenses), "total": total(expenses)})
    else:
        raise ValueError("unknown format")
