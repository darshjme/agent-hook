"""HookRegistry — manages hooks by lifecycle point."""

from __future__ import annotations

from typing import Any, Callable

from .hook import Hook
from .hook_point import HookPoint


class HookRegistry:
    """Central registry that stores and fires hooks by lifecycle point.

    Usage::

        registry = HookRegistry()

        @registry.on(HookPoint.PRE_CALL)
        def log_pre(payload):
            print("Before LLM call:", payload)

        registry.fire(HookPoint.PRE_CALL, payload={"model": "gpt-4"})
    """

    def __init__(self) -> None:
        self._hooks: dict[HookPoint, list[Hook]] = {p: [] for p in HookPoint}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, hook: Hook) -> "HookRegistry":
        """Register a Hook and return self for fluent chaining."""
        if not isinstance(hook, Hook):
            raise TypeError(f"Expected Hook instance, got {type(hook)}")
        self._hooks[hook.point].append(hook)
        self._hooks[hook.point].sort(key=lambda h: h.priority)
        return self

    def on(self, point: HookPoint, priority: int = 0) -> Callable:
        """Decorator factory that registers the decorated function as a hook.

        Args:
            point:    The lifecycle point to bind to.
            priority: Execution order (lower = earlier).

        Returns:
            Decorator that wraps the handler in a Hook and registers it.
        """
        def decorator(fn: Callable) -> Callable:
            hook = Hook(point=point, handler=fn, name=fn.__name__, priority=priority)
            self.register(hook)
            return fn

        return decorator

    # ------------------------------------------------------------------
    # Firing
    # ------------------------------------------------------------------

    def fire(self, point: HookPoint, *args: Any, **kwargs: Any) -> list[Any]:
        """Fire all hooks for *point* (ordered by priority) and collect results.

        Returns:
            List of return values from each hook handler.
        """
        return [hook.execute(*args, **kwargs) for hook in self._hooks[point]]

    def fire_until_false(self, point: HookPoint, *args: Any, **kwargs: Any) -> bool:
        """Fire hooks in priority order; stop and return False if any returns False.

        Useful as a guard: if any hook vetoes an action, execution halts.

        Returns:
            True if all hooks passed (or none were registered), False otherwise.
        """
        for hook in self._hooks[point]:
            result = hook.execute(*args, **kwargs)
            if result is False:
                return False
        return True

    # ------------------------------------------------------------------
    # Introspection & management
    # ------------------------------------------------------------------

    def list_hooks(self, point: HookPoint | None = None) -> list[Hook]:
        """Return registered hooks, optionally filtered by lifecycle point."""
        if point is not None:
            return list(self._hooks[point])
        return [hook for hooks in self._hooks.values() for hook in hooks]

    def remove(self, name: str) -> None:
        """Remove a hook by name across all lifecycle points.

        Raises:
            KeyError: If no hook with that name is registered.
        """
        for point in HookPoint:
            for hook in list(self._hooks[point]):
                if hook.name == name:
                    self._hooks[point].remove(hook)
                    return
        raise KeyError(f"No hook named {name!r} found in registry")

    def __repr__(self) -> str:  # pragma: no cover
        total = sum(len(v) for v in self._hooks.values())
        return f"HookRegistry(hooks={total})"
