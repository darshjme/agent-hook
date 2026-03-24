"""Hook — a single lifecycle handler."""

from __future__ import annotations

import uuid
from typing import Any, Callable

from .hook_point import HookPoint


class Hook:
    """A single lifecycle handler bound to a HookPoint.

    Args:
        point:    The lifecycle point this hook fires on.
        handler:  Callable invoked when the hook fires.
        name:     Optional unique name; auto-generated if omitted.
        priority: Execution order (lower = earlier). Default 0.
    """

    def __init__(
        self,
        point: HookPoint,
        handler: Callable,
        name: str | None = None,
        priority: int = 0,
    ) -> None:
        if not isinstance(point, HookPoint):
            raise TypeError(f"point must be a HookPoint, got {type(point)}")
        if not callable(handler):
            raise TypeError("handler must be callable")

        self.point: HookPoint = point
        self.handler: Callable = handler
        self.name: str = name if name is not None else str(uuid.uuid4())
        self.priority: int = priority

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Invoke the handler with the given arguments."""
        return self.handler(*args, **kwargs)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Hook(point={self.point!r}, name={self.name!r}, priority={self.priority})"
        )
