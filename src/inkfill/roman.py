"""[Roman numerals](https://en.wikipedia.org/wiki/Roman_numerals)."""

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
