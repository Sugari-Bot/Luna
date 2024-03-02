from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from luna.interpreter import Verb


class Adapter:
    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} at {hex(id(self))}>"

    def get_value(self, verb: Verb) -> Optional[str]:
        raise NotImplementedError
