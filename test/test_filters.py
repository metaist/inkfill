"""Test helper functions."""

# std
from datetime import datetime

# pkg
from inkfill import compound
from inkfill import day_of_month
from inkfill import dollars
from inkfill import spell_number
from inkfill import USD

## Dates


def test_day_of_month() -> None:
    """Nth day of the month."""
    assert day_of_month(datetime(2024, 1, 1)) == "1st day of January 2024"
    assert day_of_month(datetime(2024, 1, 31)) == "31st day of January 2024"
    assert day_of_month(datetime(2024, 2, 2)) == "2nd day of February 2024"
    assert day_of_month(datetime(2024, 2, 3)) == "3rd day of February 2024"
    assert day_of_month(datetime(2024, 2, 29)) == "29th day of February 2024"


## English


def test_compound() -> None:
    """Compound clauses."""
    assert compound([]) == ""
    assert compound(["A"]) == "A"
    assert compound(["Bill", "Ted"]) == "Bill and Ted"
    assert compound(["A", "B", "C"]) == "A, B, and C"
    assert compound(["A", "B", "C"], oxford=False) == "A, B and C"
    assert compound(["A", "B", "C"], "or") == "A, B, or C"


def test_spell_number() -> None:
    """Spell out numbers."""
    assert spell_number(-10, "degree") == "negative ten (-10) degrees"
    assert spell_number(-1, "degree") == "negative one (-1) degree"
    assert spell_number(0, "dollar") == "zero (0) dollars"
    assert spell_number(1, "day") == "one (1) day"
    assert spell_number(10, "day") == "ten (10) days"


## Money


def test_USD() -> None:
    """US dollars."""
    assert USD(100) == "US$100"
    assert USD(1, cents=True) == "US$1.00"
    assert USD(1.25, cents=True) == "US$1.25"
    assert USD(0.001, cents=True) == "US$0.001"


def test_dollars() -> None:
    """Dollars in contracts."""
    # sub-cent
    assert dollars(0.001) == "US$0.001"

    # cents
    assert dollars(0.01) == "one cent (US$0.01)"
    assert dollars(0.25) == "twenty-five cents (US$0.25)"
    assert dollars(0.99) == "ninety-nine cents (US$0.99)"

    # whole dollars
    assert dollars(0) == "zero dollars (US$0.00)"
    assert dollars(1) == "one dollar exactly (US$1.00)"
    assert dollars(2) == "two dollars exactly (US$2.00)"
    assert dollars(10) == "ten dollars exactly (US$10)"
    assert dollars(10000) == "ten thousand dollars exactly (US$10,000)"

    # dollars and cents
    assert dollars(1.25) == "one dollar and twenty-five cents (US$1.25)"
    assert dollars(11_111_111.11) == (
        "eleven million "
        "one hundred eleven thousand "
        "one hundred eleven dollars "
        "and eleven cents (US$11,111,111.11)"
    )
