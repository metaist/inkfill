"""Test Roman numeral converter."""

from inkfill import to_roman


def test_digits() -> None:
    """Single-digit numbers."""
    assert to_roman(0) == ""
    assert to_roman(1) == "I"
    assert to_roman(2) == "II"
    assert to_roman(3) == "III"
    assert to_roman(4) == "IV"
    assert to_roman(5) == "V"
    assert to_roman(6) == "VI"
    assert to_roman(7) == "VII"
    assert to_roman(8) == "VIII"
    assert to_roman(9) == "IX"


def test_larger() -> None:
    """Larger numbers."""
    assert to_roman(2023) == "MMXXIII"
    assert to_roman(2024) == "MMXXIV"
