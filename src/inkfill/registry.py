"""Name registry."""

from __future__ import annotations
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union
from typing import cast

T = TypeVar("T", bound="Registrable")
"""Generic type variable."""

NAME_REGISTRY: Dict[str, Registrable] = {}
"""Name registry."""


class Registrable:
    """Object that can be registered in the name registry."""

    name: str
    """Name of this object."""

    def add(self: T, override: bool = False) -> T:
        """Add this name to the registry."""
        name = self.name
        if name in NAME_REGISTRY and not override:
            raise Exception(f"Name {name} is already registered.")
        NAME_REGISTRY[name] = self
        return self

    @classmethod
    def get(cls: Type[T], name: Union[str, T], default: Optional[T] = None) -> T:
        """Get the requested named object."""
        if isinstance(name, cls):
            return name
        result = NAME_REGISTRY.get(cast(str, name), default)
        if not result:
            raise LookupError(f"Cannot find name: {name}")
        return cast(T, result)
