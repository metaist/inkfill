"""Common helper functions."""

# std
from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Literal

# pkg
from .numerals import to_cardinal
from .numerals import to_nth

## Dates


def nth_of_month_year(dt: datetime) -> str:
    """Return date as `{nth} day of {month} {year}`."""
    return f"{to_nth(dt.day)} day of {dt.strftime('%B %Y')}"


def month_day_year(dt: datetime) -> str:
    """Return date as `{month} {day}, {year}`."""
    return dt.strftime("%B %-d, %Y")


def day_month_year(dt: datetime) -> str:
    """Return date as `{day} {month} {year}."""
    return dt.strftime("%d %B %Y")


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


SPECIAL_PLURALS = {
    # ends in -(e)n
    "ox": "oxen",
    "child": "children",
    # NOTE: skipping "brother" / "brethren" in the frat/religious sense
    # Apophonic plurals
    "foot": "feet",
    "goose": "geese",
    "louse": "lice",
    "dormouse": "dormice",
    "man": "men",
    "mouse": "mice",
    "tooth": "teeth",
    "woman": "women",
    # Miscellaneous irregular plurals
    "person": "people",
    "die": "dice",
    "penny": "pence",
    # Latin Anglicization
    "data": "data",
    "stadium": "stadiums",
    "referendum": "referendums",
    "campus": "campuses",
    "bus": "buses",  # not Latin
    "octopus": "octopuses",  # from Greek
    "platypus": "platypuses",  # from Greek
    "prospectus": "prospectuses",
    "stylus": "styluses",
    "uterus": "uteruses",
    "virus": "viruses",
    "status": "statuses",
    # Japanese
    "samurai": "samurai",
    "futon": "futons",
    # Māori
    "Māori": "Māori",
    "Maori": "Maori",
    "waka": "waka",
    # Symbols
    "§": "§§",
    # Plurals without a singular
    "glasses": "glasses",
    "pants": "pants",
    "panties": "panties",
    "pantyhose": "pantyhose",
    "pliers": "pliers",
    "scissors": "scissors",
    "shorts": "shorts",
    "tongs": "tongs",
    "trousers": "trousers",
    "clothes": "clothes",
    # Determiners
    "this": "these",
    "that": "those",
}


def plural(word: str) -> str:
    """Return best attempt at forming an [English plural](https://en.wikipedia.org/wiki/English_plurals)."""
    if word in SPECIAL_PLURALS:
        return SPECIAL_PLURALS[word]

    if len(word) == 1:
        return f"{word}'s"
    if len(word) == 2 and word.endswith("."):
        return f"{word[0]}{word}"

    # ends in any sibilant
    for sibilant in [
        "ss",
        "se",
        "sh",
        "uch",
        "ge",
        "tch",
        "nch",
        "rch",
        "rich",
        "each",
        "oach",  # spell-checker: disable-line
        "wich",  # spell-checker: disable-line
        "ge",
        "tz",
    ]:
        if word.endswith(sibilant):
            return f"{word}{'s' if word.endswith('e') else 'es'}"

    # ends in voiceless constants
    for voiceless in ["p", "t", "ck", "ff", "gh", "ph", "th", "ech", "ich", "och"]:
        if word.endswith(voiceless):
            return f"{word}s"

    # vowels = "aeiou"  # spell-checker: disable-line
    consonants = "bcdfghjklmnpqrstvwxz"  # spell-checker: disable-line

    # NOTE: skipping consonant + o ending
    # if word[-1] == "o" and word[-2] in consonants:
    #     return f"{word}es"

    # ends in -y
    if word.endswith("y"):
        if word[-2] in consonants or word.endswith("quy"):
            return f"{word[:-1]}ies"
        return f"{word}s"

    # NOTE: skipping the -f transformation
    # if word.endswith("f"):
    #     return f"{word[:-1]}ves"

    # Latin (some skipped)
    # -a => -e
    # if word.endswith("a"):
    #     return f"{word}e"
    # We can do the inverse: if it's plural, leave it.
    if word.endswith("ae"):
        return word

    # -ex, -ix => -ices
    if word.endswith("ex") or word.endswith("ix"):
        return f"{word[:-2]}ices"
    # -is => -es (-polis => -poleis)  # spell-checker: disable-line
    if word.endswith("is"):
        if word.endswith("polis"):  # from Greek
            return f"{word[:-2]}eis"
        return f"{word[:-2]}es"
    # -ies => -ies
    if word.endswith("ies"):
        return word
    # -um => -a
    if word.endswith("um"):
        return f"{word[:-2]}a"
    # -us => -i
    if word.endswith("us"):
        return f"{word[:-2]}i"

    # Greek (some skipped)
    # -on => -a
    if word.endswith("on"):
        return f"{word[:-2]}a"
    # -as => -antes
    # if word.endswith("as"):
    #     return f"{word[:-2]}antes"
    # -ma => -mata  # spell-checker: disable-line
    # if word.endswith("ma"):
    #     return f"{word[:-2]}mata" # spell-checker: disable-line

    return f"{word}s"


def spell_number(num: int, unit: str, units: str = "") -> str:
    """Spell out the given number and units."""
    units = units or plural(unit)
    return f"{to_cardinal(num)} ({num}) {unit if abs(num) == 1 else units}"


## Money


def USD(num: float, cents: bool = False) -> str:
    """Return formatted US Dollars."""
    if cents:
        if 0 < num < 0.01:
            return f"US${num}"
        return f"US${num:,.2f}"
    return f"US${int(num):,}"


def dollars(num: float, exact: bool = False) -> str:
    """Return spelled-out dollars. Commonly used in contracts."""
    dec = Decimal(str(num))

    whole = int(dec)
    part = dec % 1
    if Decimal("0") < part < Decimal("0.01"):  # sub-cent
        return USD(num, cents=True)

    result = ""
    if whole or num == 0:
        result += f"{to_cardinal(whole)} dollar{'s' if whole != 1 else ''}"

    if whole and part:
        result += " and "

    if part:
        part *= 100
        result += f"{to_cardinal(int(part))} cent{'s' if part != 1 else ''}"
    elif num != 0 and exact:
        result += " exactly"

    cents = exact or part > 0 or num < 10
    result += f" ({USD(num, cents=cents)})"
    return result
