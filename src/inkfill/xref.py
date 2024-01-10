"""Cross-reference helpers."""

# std
from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Dict
from typing import List
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


@dataclass(frozen=True)
class RefFormat(Registrable):
    """Reference format."""

    name: str
    """Reference format name."""

    render: Callable[[Ref], str]
    """Render the reference."""

    def __call__(self, ref: Ref) -> str:
        """Render the reference."""
        return self.render(ref)


def cite_sections(ref: Ref) -> str:
    """Cite until top-level-like items."""
    parent = ref
    top_like = [Article, Part, Exhibit, Appendix, Annex, Schedule]
    numerals: List[NumFormat] = []
    values: List[int] = []
    while parent.parent and parent.numerals and parent.kind not in top_like:
        numerals.insert(0, parent.numerals[-1])
        values.insert(0, parent.values[-1])
        parent = parent.parent

    return "".join(
        num(val, idx > 0) for idx, (val, num) in enumerate(zip(values, numerals))
    )


def cite_name(ref: Ref, cite: str = "") -> str:
    """Return citation format for most section headings."""
    cite = cite or cite_sections(ref)
    if "." not in cite and not cite.endswith(")"):
        cite += "."
    return f"""
        <span class="cite">{cite}</span>
        <span class="name">{ref.name}</span>
    """


NULL_REF = RefFormat("null-ref", lambda _: "").add()
"""Always return an empty string."""

DOUBLE_QUOTES = RefFormat(
    "double-quotes", lambda ref: f"&ldquo;{ref.name}&rdquo;"
).add()
"""Enclose `name` in double quotes (e.g., define a `Term`)."""

TWO_LINE = RefFormat(
    "two-line", lambda ref: f"{ref.kind} {ref.cite}<br />{ref.name}"
).add()
"""Show `kind`, `cite`, and `name` on two lines."""

CITE_LAST = RefFormat(
    "cite-last", lambda ref: ref.numerals[-1].render(ref.values[-1], True)
).add()
"""Show end of citation (e.g., define `Paragraph`, `Clause`)."""

CITE_LAST_NAME = RefFormat(
    "cite-last-name", lambda ref: cite_name(ref, CITE_LAST(ref))
).add()
"""Show end of citation and `name` (e.g., define `Part`)."""

CITE_SECTIONS = RefFormat("cite-sections", cite_sections).add()
"""Show citations up to top-level-like."""

CITE_NAME = RefFormat("cite-name", cite_name).add()
"""Show full citation and the name (e.g., define `Section`, `Subsection`)."""

KIND_CITE = RefFormat("kind-cite", lambda ref: f"{ref.kind} {ref.cite}").add()
"""Show `kind` and `cite` (e.g., refer to non-`Term`)."""

KIND_LAST = RefFormat("kind-last", lambda ref: f"{ref.kind} {CITE_LAST(ref)}").add()
"""Show `kind` and the last part of the citation (e.g., refer to a `Part`)."""

KIND_SECTIONS = RefFormat(
    "kind-sections", lambda ref: f"{ref.kind} {CITE_SECTIONS(ref)}"
).add()
"""Show `kind` and sections."""

NAME_ONLY = RefFormat("name-only", lambda ref: ref.name).add()
"""Show only the name (e.g., refer to a `Term`)."""


@dataclass
class Division(Registrable):
    """Document section."""

    name: str
    """Name of this kind."""

    numeral: NumFormat = field(default=DECIMAL)
    """Default numeral formatting for this kind."""

    define: RefFormat = field(default=CITE_NAME)
    """Default formatting for defining a reference of this type."""

    refer: RefFormat = field(default=KIND_CITE)
    """Default formatting for referring to a reference of this type."""

    def __str__(self) -> str:
        return self.name


# Not actually divisions

Term = Division("Term", NumFormat.get(""), define=NAME_ONLY, refer=NAME_ONLY).add()
"""Defined term."""

# Divisions
# https://weagree.com/clm/contracts/contract-structure-and-presentation/articles-sections-clause-numbering/

Preamble = Division("Preamble", define=NULL_REF, refer=NAME_ONLY).add()
"""First section, typically unnumbered."""

Article = Division("Article", NumFormat.get("upper-roman"), define=TWO_LINE).add()
"""Often the top-most level."""

Part = Division(
    "Part", NumFormat.get("upper-alpha"), define=CITE_LAST_NAME, refer=KIND_LAST
).add()

Section = Division("Section", define=CITE_NAME, refer=KIND_SECTIONS).add()
"""The most common and default level."""

Subsection = Division("Subsection", define=CITE_NAME, refer=KIND_SECTIONS).add()
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

    kind: Division = field(default_factory=lambda: Section)
    """What kind of reference is this?"""

    values: List[int] = field(default_factory=list)
    """Citation numeral values."""

    numerals: List[NumFormat] = field(default_factory=list)
    """Citation numeral formats."""

    defines: List[RefFormat] = field(default_factory=list)
    """Definition formats."""

    refers: List[RefFormat] = field(default_factory=list)
    """Reference formats."""

    parent: Optional[Ref] = None
    """Parent reference."""

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
            parent=self.parent,
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
        return f"""<a class="ref{'' if self.is_defined else ' not-defined'}"
               href="#{self.slug}" data-kind="{self.kind}">{refer(self).strip()}</a>"""

    __str__ = refer


class Refs:
    """Reference manager."""

    stack: List[Ref]
    """Current document levels."""

    store: Dict[str, Ref]
    """Slugs mapped to references."""

    def __init__(self) -> None:
        """Construct a new reference manager."""
        self.reset()

    def __str__(self) -> str:
        """Return blank string to avoid rendering."""
        return ""

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

    def ancestor(self, kind: Union[str, Division]) -> Ref:
        """Return the ancestor that matches the `kind`."""
        kind = Division.get(kind)
        result = self.current
        while result.parent:
            if result.kind is kind:
                return result
            result = result.parent
        return result

    def push(
        self,
        kind: Union[str, Division] = Section,
        # formatting overrides
        numeral: Union[str, NumFormat, None] = None,
        define: Union[str, RefFormat, None] = None,
        refer: Union[str, RefFormat, None] = None,
    ) -> Refs:
        """Add another level."""
        level = self.current.copy()
        level.parent = self.current
        level.kind = Division.get(kind) or Section
        level.values.append(0)
        level.numerals.append(NumFormat.get(numeral or level.kind.numeral))
        level.defines.append(RefFormat.get(define or level.kind.define))
        level.refers.append(RefFormat.get(refer or level.kind.refer))
        self.stack.append(level)
        return self

    def up(self, name: str = "", slug: str = "") -> str:
        """Increment current level."""
        ref = self.current.copy()
        ref.name = name
        ref.values[-1] += 1
        ref.update_slug(slug)  # needs name & values updated
        self.stack[-1] = ref
        self.store[ref.slug] = ref
        return ref.define()

    def pop(self, num: int = 1) -> Refs:
        """Remove one or more level."""
        for _ in range(num):
            if len(self.stack) == 0:
                break
            self.stack.pop()
        return self

    ## Short-hand
    def add(self, ref: Ref) -> Ref:
        """Add a ref to the store."""
        self.store[ref.slug] = ref
        return ref

    def see(self, name: str = "", kind: str = "Section", slug: str = "") -> Ref:
        """Refer to a reference."""
        slug = slug or slugify(kind, name)
        if slug in self.store:
            return self.store[slug]

        ref = Ref(name=name, kind=Division.get(kind), parent=self.current)
        ref.update_slug(slug)
        return self.add(ref)

    def term(self, name: str) -> Ref:
        """Refer to a terms."""
        return self.see(name, "Term")
