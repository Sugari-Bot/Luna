from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from luna.interpreter import Context, Verb


class Adapter:
    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} at {hex(id(self))}>"

    def get_value(self, ctx: Union[Context, Verb]) -> Optional[str]:
        raise NotImplementedError
