"""Multi-document template engine.

.. include:: ../../README.md
   :start-line: 2
"""
from .numerals import commafy
from .numerals import NumFormat
from .numerals import to_alpha
from .numerals import to_cardinal
from .numerals import to_decimal
from .numerals import to_nth
from .numerals import to_ordinal
from .numerals import to_roman

from .filters import compound
from .filters import day_month_year
from .filters import dollars
from .filters import month_day_year
from .filters import nth_of_month_year
from .filters import one_or_many
from .filters import plural
from .filters import spell_number
from .filters import USD

from .xref import Division
from .xref import Ref
from .xref import RefFormat
from .xref import Refs
from .xref import slugify

__version__ = "0.1.0"
__pubdate__ = ""

__all__ = [
    "__version__",
    "__pubdate__",
    # numeric
    "commafy",
    "NumFormat",
    "to_alpha",
    "to_cardinal",
    "to_decimal",
    "to_nth",
    "to_ordinal",
    "to_roman",
    # filters
    "compound",
    "nth_of_month_year",
    "month_day_year",
    "day_month_year",
    "dollars",
    "plural",
    "one_or_many",
    "spell_number",
    "USD",
    # xref
    "Division",
    "Ref",
    "RefFormat",
    "Refs",
    "slugify",
]
