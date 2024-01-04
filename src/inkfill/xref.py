"""Cross-reference helpers."""

# std
from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Callable
from typing import Optional
from typing import Union
import re

# pkg
from .registry import Registrable
from .numerals import NumFormat
from .numerals import DECIMAL

RE_NON_SLUG = re.compile(r"[^a-z0-9_-]")
"""Match characters to convert to dash in a slug."""

RE_REPEATED_DASH = re.compile(r"-{2,}")
"""Match repeated dashes."""


def slugify(*names: str) -> str:
    """Return a slug version of a name."""
    return RE_REPEATED_DASH.sub(
        "-", RE_NON_SLUG.sub("-", "-".join(names).lower())
    ).strip("-")


@dataclass
class RefFormat(Registrable):
    """Reference format."""

    name: str
    """Reference format name."""

    render: Callable[[Ref], str]
    """Render the reference."""

    def __call__(self, ref: Ref) -> str:
        """Render the reference."""
        return self.render(ref)


def cite_name(ref: Ref) -> str:
    """Return citation format for most section headings."""
    cite = ref.cite
    if "." not in cite and not cite.endswith(")"):
        cite += "."
    return f"{cite} {ref.name}".strip()


DOUBLE_QUOTES = RefFormat(
    "double-quotes", lambda ref: f"&ldquo;{ref.name}&rdquo;"
).add()
"""Enclose `name` in double quotes (e.g., define a `Term`)."""

TWO_LINE = RefFormat(
    "two-line", lambda ref: f"{ref.kind} {ref.cite}<br />{ref.name}"
).add()
"""Show `kind`, `cite`, and `name` on two lines."""

CITE_NAME = RefFormat("cite-name", cite_name).add()
"""Show full citation and the name (e.g., define `Part`, `Section`, `Subsection`)."""

CITE_LAST = RefFormat(
    "cite-last", lambda ref: ref.numerals[-1].render(ref.values[-1], True)
).add()
"""Show only the end of the citation (e.g., define `Paragraph`, `Clause`)."""

RefFormat.DEFAULT = CITE_FULL = RefFormat(
    "kind-cite", lambda ref: f"{ref.kind} {ref.cite}"
).add()
"""Show `kind` and `cite` (e.g., refer to non-`Term`)."""

NAME_ONLY = RefFormat("name-only", lambda ref: ref.name).add()
"""Show only the name (e.g., refer to a `Term`)."""


@dataclass
class Division(Registrable):
    """Document section."""

    name: str
    """Name of this kind."""

    numeral: NumFormat = DECIMAL
    """Default numeral formatting for this kind."""

    define: RefFormat = CITE_NAME
    """Default formatting for defining a reference of this type."""

    refer: RefFormat = CITE_FULL
    """Default formatting for referring to a reference of this type."""

    def __str__(self) -> str:
        return self.name


# https://weagree.com/clm/contracts/contract-structure-and-presentation/articles-sections-clause-numbering/

Term = Division("Term", NumFormat.get(""), define=DOUBLE_QUOTES, refer=NAME_ONLY).add()
"""Defined term."""

Article = Division("Article", NumFormat.get("upper-roman"), define=TWO_LINE).add()
"""Often the top-most level."""

Part = Division("Part", NumFormat.get("upper-alpha")).add()

Division.DEFAULT = Section = Division("Section").add()
"""The most common and default level."""

Subsection = Division("Subsection").add()
"""Subdivision of a section."""

Paragraph = Division("Paragraph", NumFormat.get("lower-alpha"), define=CITE_LAST).add()
"""Items within a subsection."""

Item = Division("Item", NumFormat.get("lower-alpha"), define=CITE_LAST).add()
"""Similar to a paragraph."""

Clause = Division("Clause", NumFormat.get("lower-roman"), define=CITE_LAST).add()
"""Items within a paragraph."""

## Supplementary

Exhibit = Division("Exhibit", NumFormat.get("upper-alpha"), define=TWO_LINE).add()
"""Supporting document."""

Appendix = Division("Appendix", NumFormat.get("upper-alpha"), define=TWO_LINE).add()
"""Additional details."""

Annex = Division("Annex", NumFormat.get("upper-alpha"), define=TWO_LINE).add()
"""Substantial appendix."""

Schedule = Division("Schedule", NumFormat.get("upper-alpha"), define=TWO_LINE).add()
"""Supplementary material."""


@dataclass
class Ref:
    """Reference to a term or section of a document."""

    # `name` and `slug` are for referencing
    # `kind` and formats are for levels/sectioning.

    name: str = ""
    """Term or section title."""

    slug: str = ""
    """Unique ID of this reference (should include `kind` + `name`)."""

    kind: Division = Section
    """What kind of reference is this?"""

    values: List[int] = field(default_factory=list)
    """Citation numeral values."""

    numerals: List[NumFormat] = field(default_factory=list)
    """Citation numeral formats."""

    defines: List[RefFormat] = field(default_factory=list)
    """Definition formats."""

    refers: List[RefFormat] = field(default_factory=list)
    """Reference formats."""

    is_defined: bool = False
    """Whether or not this reference has been defined."""

    def copy(self) -> Ref:
        """Return a copy of this reference."""
        return Ref(
            name=self.name,
            slug=self.slug,
            kind=self.kind,
            values=self.values.copy(),
            numerals=self.numerals.copy(),
            defines=self.defines.copy(),
            refers=self.refers.copy(),
        )

    def update_slug(self, slug: str = "") -> Ref:
        """Update the slug when the name or citation has changed."""
        if slug:
            self.slug = slugify(slug)
        elif self.name:
            self.slug = slugify(f"{self.kind}-{self.name}")
        else:
            self.slug = slugify(f"{self.kind}-{self.cite}")
        return self

    @property
    def cite(self) -> str:
        """Return a citation (without the `kind`) to this reference."""
        return "".join(
            num(val, idx > 0)
            for idx, (val, num) in enumerate(zip(self.values, self.numerals))
        )

    @property
    def above_below(self) -> str:
        """Return 'above' if defined, otherwise 'below'."""
        return "above" if self.is_defined else "below"

    def define(self) -> str:
        """Return the reference definition."""
        if self.is_defined:
            raise Exception(f"{self.kind} {self.slug} already defined")
        self.is_defined = True

        refer = self.kind.refer if len(self.refers) == 0 else self.refers[-1]
        define = self.kind.define if len(self.defines) == 0 else self.defines[-1]
        return f"""<span class="def" id="{self.slug}" data-kind="{self.kind}"
                    data-cite="{refer(self).strip()}">{define(self).strip()}</span>"""

    def refer(self) -> str:
        """Return a link to the reference definition."""
        refer = self.kind.refer if len(self.refers) == 0 else self.refers[-1]
        return f"""<a class="ref" href="#{self.slug}"
                    data-kind="{self.kind}">{refer(self).strip()}</a>"""


class Refs:
    """Reference manager."""

    stack: List[Ref]
    """Current document levels."""

    store: Dict[str, Ref]
    """Slugs mapped to references."""

    def __init__(self) -> None:
        """Construct a new reference manager."""
        self.reset()

    def reset(self) -> Refs:
        """Reset the references."""
        self.stack = []
        self.store = {}
        return self

    @property
    def undefined(self) -> List[Ref]:
        """References that were never defined."""
        return [ref for ref in self.store.values() if not ref.is_defined]

    @property
    def current(self) -> Ref:
        """Reference to current level."""
        return Ref() if len(self.stack) == 0 else self.stack[-1]

    def push(
        self,
        kind: Union[str, Division] = Section,
        # formatting overrides
        numeral: Optional[NumFormat] = None,
        define: Optional[RefFormat] = None,
        refer: Optional[RefFormat] = None,
    ) -> Refs:
        """Add another level."""
        level = self.current.copy()
        level.kind = Division.get(kind) or Section
        level.values.append(0)
        level.numerals.append(numeral or level.kind.numeral)
        level.defines.append(define or level.kind.define)
        level.refers.append(refer or level.kind.refer)
        self.stack.append(level)
        return self

    def up(self, name: str = "", slug: str = "") -> Ref:
        """Increment current level."""
        ref = self.current.copy()
        ref.name = name
        ref.values[-1] += 1
        ref.update_slug(slug)  # needs name & values updated
        self.stack[-1] = ref
        self.store[ref.slug] = ref
        return ref

    def pop(self, num: int = 1) -> Refs:
        """Remove one or more level."""
        for _ in range(num):
            if len(self.stack) == 0:
                break
            self.stack.pop()
        return self
