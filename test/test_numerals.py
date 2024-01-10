"""Test numeral systems."""
# lib
import pytest

# pkg
from inkfill import commafy
from inkfill import to_alpha
from inkfill import to_cardinal
from inkfill import to_decimal
from inkfill import to_nth
from inkfill import to_ordinal
from inkfill import to_roman
from inkfill import NumFormat
from inkfill.numerals import DECIMAL


def test_commafy() -> None:
    """Group digits."""
    assert commafy(100) == "100"
    assert commafy(1000) == "1,000"
    assert commafy(1_000_000) == "1,000,000"


def test_decimal() -> None:
    """Decimal numerals."""
    assert to_decimal(0) == "0"
    assert to_decimal(1000) == "1000"


def test_alpha() -> None:
    """Alphabetic numerals."""
    # single
    assert to_alpha(0) == ""
    assert to_alpha(1) == "A"
    assert to_alpha(26) == "Z"

    # double
    assert to_alpha(26 + 1) == "AA"
    assert to_alpha(26 + 2) == "AB"
    assert to_alpha(26 + 26) == "AZ"
    assert to_alpha(26 + 26 + 1) == "BA"

    # larger
    assert to_alpha((26**2) + (26**1) + 1) == "AAA"
    assert to_alpha((26**3) + (26**2) + (26**1) + 1) == "AAAA"
    assert to_alpha((26**4) + (26**3) + (26**2) + (26**1) + 1) == "AAAAA"


def test_roman() -> None:
    """Roman numerals."""
    # digits
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

    # larger
    assert to_roman(2023) == "MMXXIII"
    assert to_roman(2024) == "MMXXIV"


def test_cardinal() -> None:
    """Cardinal numerals spelled out."""
    assert to_cardinal(0) == "zero"
    assert to_cardinal(-1) == "negative one"
    assert to_cardinal(-256) == "negative two hundred fifty-six"
    assert to_cardinal(1) == "one"
    assert to_cardinal(10) == "ten"
    assert to_cardinal(11) == "eleven"
    assert to_cardinal(16) == "sixteen"
    assert to_cardinal(20) == "twenty"
    assert to_cardinal(21) == "twenty-one"
    assert to_cardinal(100) == "one hundred"
    assert to_cardinal(118) == "one hundred eighteen"
    assert to_cardinal(200) == "two hundred"
    assert to_cardinal(219) == "two hundred nineteen"
    assert to_cardinal(800) == "eight hundred"
    assert to_cardinal(801) == "eight hundred one"
    assert to_cardinal(1316) == "one thousand three hundred sixteen"
    assert to_cardinal(2023) == "two thousand twenty-three"
    assert to_cardinal(90210) == "ninety thousand two hundred ten"

    assert to_cardinal(1_000_000) == "one million"
    assert to_cardinal(2_000_000) == "two million"
    assert to_cardinal(3_000_200) == "three million two hundred"
    assert to_cardinal(7_000_000_000_000) == "seven trillion"

    assert to_cardinal(123_456_789) == (
        "one hundred twenty-three million "
        "four hundred fifty-six thousand "
        "seven hundred eighty-nine"
    )
    assert to_cardinal(43_259_876_345) == (
        "forty-three billion "
        "two hundred fifty-nine million "
        "eight hundred seventy-six thousand "
        "three hundred forty-five"
    )
    assert to_cardinal(1_000_000_000_000_000) == "one quadrillion"
    assert to_cardinal(1_000_000_000_000_000_000_000_000_000_000_000) == "one decillion"
    assert (
        to_cardinal(1_000_000_000_000_000_000_000_000_000_000_000_000)
        == "one thousand decillion"  # past largest
    )


def test_nth() -> None:
    """Ordinal numerals with numeric prefix."""
    assert to_nth(0) == "0th"
    assert to_nth(1) == "1st"
    assert to_nth(2) == "2nd"
    assert to_nth(3) == "3rd"
    assert to_nth(4) == "4th"
    assert to_nth(10) == "10th"
    assert to_nth(11) == "11th"
    assert to_nth(12) == "12th"
    assert to_nth(13) == "13th"
    assert to_nth(20) == "20th"
    assert to_nth(21) == "21st"
    assert to_nth(22) == "22nd"
    assert to_nth(23) == "23rd"
    assert to_nth(100) == "100th"
    assert to_nth(101) == "101st"
    assert to_nth(111) == "111th"
    assert to_nth(311) == "311th"


def test_ordinal() -> None:
    """Ordinal numerals spelled out."""
    # one, two, three => first, second, third
    assert to_ordinal(1) == "first"
    assert to_ordinal(21) == "twenty-first"
    assert to_ordinal(102) == "one hundred second"

    assert to_ordinal(2) == "second"
    assert to_ordinal(3) == "third"

    # ve => fth
    assert to_ordinal(5) == "fifth"
    assert to_ordinal(12) == "twelfth"

    # t => th
    assert to_ordinal(8) == "eighth"

    # e => th
    assert to_ordinal(9) == "ninth"

    # y => ieth
    assert to_ordinal(20) == "twentieth"
    assert to_ordinal(50) == "fiftieth"

    # else: +th
    assert to_ordinal(0) == "zeroth"
    assert to_ordinal(4) == "fourth"
    assert to_ordinal(6) == "sixth"
    assert to_ordinal(16) == "sixteenth"


def test_numeral() -> None:
    """Numeral system."""
    assert NumFormat.get("decimal") is DECIMAL
    assert NumFormat.get(DECIMAL) is DECIMAL
    with pytest.raises(LookupError):
        NumFormat.get("unknown")

    assert NumFormat.get("").render(1) == ""
    assert NumFormat.get("decimal").render(1) == "1"
    assert NumFormat.get("lower-alpha").render(1) == "a"
    assert NumFormat.get("upper-alpha").render(1) == "A"
    assert NumFormat.get("lower-roman").render(1) == "i"
    assert NumFormat.get("upper-roman").render(1) == "I"
    assert NumFormat.get("numeric-ordinal").render(1) == "1st"
    assert NumFormat.get("lower-ordinal").render(1) == "first"
    assert NumFormat.get("title-ordinal").render(1) == "First"
    assert NumFormat.get("lower-cardinal").render(1) == "one"
    assert NumFormat.get("title-cardinal").render(1) == "One"

    with pytest.raises(Exception):
        NumFormat("decimal", to_decimal).add()  # already exists
