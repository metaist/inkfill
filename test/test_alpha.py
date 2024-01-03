"""Test alphabetic numeral converter."""

from inkfill import to_alpha


def test_single() -> None:
    """Single-letter numbers."""
    assert to_alpha(0) == ""
    assert to_alpha(1) == "A"
    assert to_alpha(26) == "Z"


def test_double() -> None:
    """Double-letter numbers."""
    assert to_alpha(26 + 1) == "AA"
    assert to_alpha(26 + 2) == "AB"
    assert to_alpha(26 + 26) == "AZ"
    assert to_alpha(26 + 26 + 1) == "BA"


def test_larger() -> None:
    """Larger numbers."""
    assert to_alpha((26**2) + (26**1) + 1) == "AAA"
    assert to_alpha((26**3) + (26**2) + (26**1) + 1) == "AAAA"
    assert to_alpha((26**4) + (26**3) + (26**2) + (26**1) + 1) == "AAAAA"
