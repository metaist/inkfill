"""[English numerals](https://en.wikipedia.org/wiki/English_numerals)."""

# std
from typing import Dict

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
    """Return the cardinal numeral spelled out.

    See:
        - https://en.wikipedia.org/wiki/Cardinal_numeral
        - https://stackoverflow.com/a/54018199
    """
    if num == 0:
        return "zero"
    if num < 0:
        return _space_join("negative", _pos(-num))
    return _pos(num)


def to_nth(num: int) -> str:
    """Return the ordinal numeral with a numeric prefix ("1st", "2nd").

    See: https://en.wikipedia.org/wiki/Ordinal_numeral
    """
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        suffixes = {1: "st", 2: "nd", 3: "rd"}
        suffix = suffixes.get(num % 10, "th")
    return str(num) + suffix


def to_ordinal(num: int) -> str:
    """Return the ordinal numeral spelled out ("first", "second").

    See: https://en.wikipedia.org/wiki/Ordinal_numeral
    """
    cardinal = to_cardinal(num)
    for check, suffix in ORDINAL_SUFFIXES.items():
        if cardinal.endswith(check):
            return cardinal[: -len(check)] + suffix
    return cardinal + "th"


def to_decimal(num: int) -> str:
    """Return the decimal numeral.

    See: https://en.wikipedia.org/wiki/Decimal
    """
    return str(num)


def commafy(num: int) -> str:
    """Return a comma-grouped number."""
    return f"{num:,}"
