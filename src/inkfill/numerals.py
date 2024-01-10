"""[Numeral systems](https://en.wikipedia.org/wiki/Numeral_system)."""

# std
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from typing import Dict

# pkg
from .registry import Registrable


def commafy(num: int) -> str:
    """Return a comma-grouped number."""
    return f"{num:,}"


def to_decimal(num: int) -> str:
    """Decimal numerals."""
    # https://en.wikipedia.org/wiki/Decimal
    return str(num)


## Alphabetic numerals

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""English alphabet."""


def to_alpha(num: int) -> str:
    """English alphabetical numerals."""
    # https://en.wikipedia.org/wiki/English_alphabet
    result = ""
    if num < 1:
        return result

    while num > 0:
        num, remainder = divmod(num - 1, 26)
        result = ALPHABET[remainder] + result

    return result


ROMAN_VALS = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
"""Roman numeral values."""

ROMAN_SYMS = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
"""Roman numeral symbols."""


def to_roman(num: int) -> str:
    """Return the [Roman numeral](https://en.wikipedia.org/wiki/Roman_numerals)."""
    result = ""
    if num < 1:
        return result

    idx = 0
    while num > 0:
        for _ in range(num // ROMAN_VALS[idx]):
            result += ROMAN_SYMS[idx]
            num -= ROMAN_VALS[idx]
        idx += 1
    return result


## [English numerals](https://en.wikipedia.org/wiki/English_numerals)

NAME_ONES: Dict[int, str] = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}
"""Name of numbers under 20."""

NAME_TENS: Dict[int, str] = {
    2: "twenty",
    3: "thirty",
    4: "forty",
    5: "fifty",
    6: "sixty",
    7: "seventy",
    8: "eighty",
    9: "ninety",
}
"""Name of the tens."""

NAME_ILLIONS: Dict[int, str] = {
    1: "thousand",
    2: "million",
    3: "billion",
    4: "trillion",
    5: "quadrillion",
    6: "quintillion",
    7: "sextillion",
    8: "septillion",
    9: "octillion",
    10: "nonillion",
    11: "decillion",
}
"""Names of the larger numbers."""

ORDINAL_SUFFIXES = {
    "one": "first",
    "two": "second",
    "three": "third",
    "ve": "fth",  # five => fifth; twelve => twelfth
    "t": "th",  # eight => eighth
    "e": "th",  # nine => ninth
    "y": "ieth",  # twenty => twentieth
}
"""Special ordinal suffix replacements."""


def _space_join(*args: str) -> str:
    """Join non-empty arguments with a space."""
    return " ".join(arg for arg in args if arg)


def _divide(dividend: int, divisor: int, magnitude: str) -> str:
    return _space_join(_pos(dividend // divisor), magnitude, _pos(dividend % divisor))


def _pos(num: int) -> str:
    if num < 20:
        return NAME_ONES[num]
    if num < 100:
        tens = NAME_TENS[num // 10]
        ones = NAME_ONES[num % 10]
        if tens and ones:  # hyphenate numbers 21-99
            return f"{tens}-{ones}"
        return _space_join(tens, ones)
    if num < 1000:
        return _divide(num, 100, "hundred")

    illions_number, illions_name = 1, "thousand"
    for illions_number, illions_name in NAME_ILLIONS.items():
        if num < 1000 ** (illions_number + 1):
            break
    return _divide(num, 1000**illions_number, illions_name)


def to_cardinal(num: int) -> str:
    """English cardinal numerals."""
    # https://en.wikipedia.org/wiki/Cardinal_numeral
    # See: https://stackoverflow.com/a/54018199
    if num == 0:
        return "zero"
    if num < 0:
        return _space_join("negative", _pos(-num))
    return _pos(num)


def to_nth(num: int) -> str:
    """Numeric ordinal numerals ("1st", "2nd")."""
    # https://en.wikipedia.org/wiki/Ordinal_numeral
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        suffixes = {1: "st", 2: "nd", 3: "rd"}
        suffix = suffixes.get(num % 10, "th")
    return str(num) + suffix


def to_ordinal(num: int) -> str:
    """English ordinal numerals ("first", "second")."""
    # https://en.wikipedia.org/wiki/Ordinal_numeral
    cardinal = to_cardinal(num)
    for check, suffix in ORDINAL_SUFFIXES.items():
        if cardinal.endswith(check):
            return cardinal[: -len(check)] + suffix
    return cardinal + "th"


NUMERAL_FUNC = Callable[[int], str]
"""Render a numeral from an integer."""


@dataclass(frozen=True)
class NumFormat(Registrable):
    """Numeral formatter."""

    name: str
    """Numeral system name."""

    numeral: NUMERAL_FUNC
    """Function that converts an integer to a numeral."""

    prefix: str = ""
    """Prefix string when rendering."""

    suffix: str = ""
    """Suffix string when rendering."""

    def render(self, num: int, punctuation: bool = False) -> str:
        """Render the numeral."""
        val = self.numeral(num)
        return val if not punctuation else f"{self.prefix}{val}{self.suffix}"

    __call__ = render


def call_lower(f: NUMERAL_FUNC) -> NUMERAL_FUNC:
    """Call `.lower()` after calling a render function."""
    return lambda n: f(n).lower()


def call_title(f: NUMERAL_FUNC) -> NUMERAL_FUNC:
    """Call `.title()` after calling a render function."""
    return lambda n: f(n).title()


NULL_FORMAT = NumFormat("", lambda *_: "").add()
"""Special empty formatting."""

DECIMAL = NumFormat("decimal", to_decimal, prefix=".").add()
"""Arabic numerals: 1, 2, 3..."""
# https://www.w3.org/TR/predefined-counter-styles/#decimal

LOWER_ALPHA = NumFormat(
    "lower-alpha", call_lower(to_alpha), prefix="(", suffix=")"
).add()
"""Lowercase English alphabet: a, b, c, ..., aa, ab..."""
# https://www.w3.org/TR/predefined-counter-styles/#lower-alpha

UPPER_ALPHA = NumFormat("upper-alpha", to_alpha).add()
"""Uppercase English alphabet: A, B, C, ..., AA, AB..."""
# https://www.w3.org/TR/predefined-counter-styles/#upper-alpha

LOWER_ROMAN = NumFormat(
    "lower-roman", call_lower(to_roman), prefix="(", suffix=")"
).add()
"""Lowercase Roman numerals: i, ii, iii..."""
# https://www.w3.org/TR/predefined-counter-styles/#lower-roman

UPPER_ROMAN = NumFormat("upper-roman", to_roman).add()
"""Uppercase Roman numerals: I, II, III..."""
# https://www.w3.org/TR/predefined-counter-styles/#upper-roman

NUMERIC_ORDINAL = NumFormat("numeric-ordinal", to_nth).add()
"""Numeric ordinals: 1st, 2nd, 3rd..."""

LOWER_ORDINAL = NumFormat("lower-ordinal", to_ordinal).add()
"""Lowercase ordinals: first, second, third..."""

TITLE_ORDINAL = NumFormat("title-ordinal", call_title(to_ordinal)).add()
"""Title-case ordinals: First, Second, Third, Fourth, Fifth..."""

LOWER_CARDINAL = NumFormat("lower-cardinal", to_cardinal).add()
"""Lowercase cardinals: one, two, three, four, five..."""

TITLE_CARDINAL = NumFormat("title-cardinal", call_title(to_cardinal)).add()
"""Title-case cardinals: One, Two, Three, Four, Five..."""
