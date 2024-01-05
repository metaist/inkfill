"""Test cross-referencing."""

# lib
import pytest

# pkg
from inkfill import Ref
from inkfill import RefFormat
from inkfill import Division
from inkfill import Refs
from inkfill import slugify
from inkfill.numerals import DECIMAL
from inkfill.numerals import LOWER_ALPHA


def test_slugify() -> None:
    """Slugify strings."""
    assert slugify("") == ""
    assert slugify("This") == "this"
    assert slugify("This is a test") == "this-is-a-test"
    assert slugify("---this- - - works---") == "this-works"
    assert slugify("this-is-a-test") == "this-is-a-test"  # idempotent


def test_ref_format() -> None:
    """Reference formats."""
    ref = Ref(
        name="Name",
        slug="slug",
        values=[1, 2],
        numerals=[DECIMAL, LOWER_ALPHA],
    )
    assert ref.name in RefFormat.get("double-quotes").render(ref)
    assert "1(b)" in RefFormat.get("two-line").render(ref)
    assert ref.name in RefFormat.get("cite-name").render(ref)
    assert "(b)" in RefFormat.get("cite-last").render(ref)
    assert "1(b)" in RefFormat.get("cite-full").render(ref)
    assert ref.name == RefFormat.get("name-only").render(ref)


def test_ref_basic() -> None:
    """Basic references."""

    ref = Ref(slug="slug-1").copy()
    assert ref.above_below == "below"  # before being defined
    assert ref.refer() != ""
    assert ref.define() != ""
    assert ref.above_below == "above"  # after being defined
    with pytest.raises(Exception):
        ref.define()  # trying to define a second time


def test_ref_update_slug() -> None:
    """Update slug."""
    ref = Ref(values=[1, 2, 3], numerals=[DECIMAL, DECIMAL, LOWER_ALPHA])
    ref.update_slug()  # using kind + citation
    assert ref.slug == "section-1-2-c"

    ref.name = "Slug 2"
    ref.update_slug()  # using kind + name
    assert ref.slug == "section-slug-2"

    ref.update_slug("Slug 3")  # using given
    assert ref.slug == "slug-3"


def test_refs_basic() -> None:
    """Basic references."""
    refs = Refs()
    assert refs.undefined == []

    ref = refs.push().push().push("Subsection").up("Test")
    assert refs.current is ref
    assert ref.slug == "subsection-test"
    assert ref.name == "Test"
    assert ref.cite == "0.0.1"
    assert not ref.is_defined

    ref.define()
    assert ref.is_defined

    refs.pop(4)  # more than levels, but it's ok
    assert refs.stack == []
    refs.pop(0)  # no op


def test_refs_term_see() -> None:
    """Short hand functions."""
    refs = Refs()
    ref = refs.term("Corporation")  # new term
    assert ref.slug == "term-corporation"
    assert ref.name == "Corporation"
    assert ref.kind is Division.get("Term")

    ref2 = refs.term("Corporation")
    assert ref2 is ref  # same term

    ref3 = refs.see("Corporation", kind="Term")
    assert ref3 is ref
