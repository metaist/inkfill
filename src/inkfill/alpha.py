"""[English alphabet](https://en.wikipedia.org/wiki/English_alphabet)."""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""English alphabet."""


def to_alpha(num: int) -> str:
    """Return alphabetic form of a number."""
    result = ""
    if num < 1:
        return result

    while num > 0:
        num, remainder = divmod(num - 1, 26)
        result = ALPHABET[remainder] + result

    return result
