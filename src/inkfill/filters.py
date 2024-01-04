"""Common helper functions."""

# std
from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Literal

# pkg
from .numerals import to_cardinal as say_number
from .numerals import to_nth

## Dates


def day_of_month(dt: datetime) -> str:
    """Return date as `{nth} day of {month} {year}`."""
    return f"{to_nth(dt.day)} day of {dt.strftime('%B %Y')}"


## English

FANBOYS = Literal["for", "and", "nor", "but", "or", "yet", "so"]
"""Common coordinating conjunctions."""


def compound(
    clauses: List[str],
    conjunction: FANBOYS = "and",
    oxford: bool = True,
) -> str:
    """Return `clauses` connected with `conjunction` and Oxford comma (optional)."""
    L = len(clauses)
    if L == 0:
        return ""
    if L == 1:
        return clauses[0]
    if L == 2:
        return f" {conjunction} ".join(clauses)

    first = ", ".join(clauses[0:-1])
    last = clauses[-1]
    return f"{first}{',' if oxford else ''} {conjunction} {last}"


## Money


def USD(num: float, cents: bool = False) -> str:
    """Return formatted US Dollars."""
    if cents:
        if 0 < num < 0.01:
            return f"US${num}"
        return f"US${num:,.2f}"
    return f"US${num:,}"


def dollars(num: float) -> str:
    """Return spelled-out dollars. Commonly used in contracts."""
    dec = Decimal(str(num))

    whole = int(dec)
    part = dec % 1
    if Decimal("0") < part < Decimal("0.01"):  # sub-cent
        return USD(num, cents=True)

    result = ""
    if whole or num == 0:
        result += f"{say_number(whole)} dollar{'s' if whole != 1 else ''}"

    if whole and part:
        result += " and "

    if part:
        part *= 100
        result += f"{say_number(int(part))} cent{'s' if part != 1 else ''}"
    elif num != 0:
        result += " exactly"

    result += f" ({USD(num, cents=part > 0 or num < 10)})"
    return result
