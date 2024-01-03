"""Multi-document template engine.

.. include:: ../../README.md
   :start-line: 2
"""


from .alpha import to_alpha
from .numeric import commafy
from .numeric import to_cardinal
from .numeric import to_decimal
from .numeric import to_nth
from .numeric import to_ordinal
from .roman import to_roman


__version__ = "0.1.0"
__pubdate__ = ""

__all__ = [
    "__version__",
    "__pubdate__",
    # numeric
    "commafy",
    "to_alpha",
    "to_cardinal",
    "to_decimal",
    "to_nth",
    "to_ordinal",
    "to_roman",
]
