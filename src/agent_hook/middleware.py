"""MiddlewareChain — wraps a callable with before/after middleware."""

from __future__ import annotations

from typing import Any, Callable


class MiddlewareChain:
    """Wraps a target callable with ordered before/after middleware layers.

    Middleware callables receive the same ``*args, **kwargs`` as the wrapped
    function.  The ``after`` middleware additionally receives the return value
    via the keyword argument ``result``.

    Usage::

        def llm_call(prompt: str) -> str:
            return f"response to: {prompt}"

        chain = (
            MiddlewareChain(llm_call)
            .before(lambda prompt: print("→", prompt))
            .after(lambda prompt, result: print("←", result))
        )

        answer = chain("hello")
    """

    def __init__(self, func: Callable) -> None:
        if not callable(func):
            raise TypeError("func must be callable")
        self._func: Callable = func
        self._before: list[Callable] = []
        self._after: list[Callable] = []

    def before(self, middleware: Callable) -> "MiddlewareChain":
        """Append a *before* middleware and return self for fluent chaining."""
        if not callable(middleware):
            raise TypeError("middleware must be callable")
        self._before.append(middleware)
        return self

    def after(self, middleware: Callable) -> "MiddlewareChain":
        """Append an *after* middleware and return self for fluent chaining."""
        if not callable(middleware):
            raise TypeError("middleware must be callable")
        self._after.append(middleware)
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the full before → func → after pipeline."""
        for mw in self._before:
            mw(*args, **kwargs)

        result = self._func(*args, **kwargs)

        for mw in self._after:
            mw(*args, result=result, **kwargs)

        return result

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"MiddlewareChain(func={self._func.__name__!r}, "
            f"before={len(self._before)}, after={len(self._after)})"
        )
