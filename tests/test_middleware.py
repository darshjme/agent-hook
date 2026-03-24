"""Tests for MiddlewareChain."""

import pytest
from agent_hook import MiddlewareChain


def test_chain_calls_func():
    chain = MiddlewareChain(lambda x: x * 2)
    assert chain(5) == 10


def test_before_middleware_runs():
    calls = []
    chain = MiddlewareChain(lambda x: x).before(lambda x: calls.append(("before", x)))
    chain(42)
    assert calls == [("before", 42)]


def test_after_middleware_runs_with_result():
    calls = []
    chain = (
        MiddlewareChain(lambda x: x + 1)
        .after(lambda x, result: calls.append(("after", x, result)))
    )
    chain(9)
    assert calls == [("after", 9, 10)]


def test_before_returns_self_for_chaining():
    chain = MiddlewareChain(lambda: None)
    assert chain.before(lambda: None) is chain


def test_after_returns_self_for_chaining():
    chain = MiddlewareChain(lambda: None)
    assert chain.after(lambda **kw: None) is chain


def test_multiple_before_run_in_order():
    order = []
    chain = (
        MiddlewareChain(lambda: None)
        .before(lambda: order.append(1))
        .before(lambda: order.append(2))
    )
    chain()
    assert order == [1, 2]


def test_multiple_after_run_in_order():
    order = []
    chain = (
        MiddlewareChain(lambda: None)
        .after(lambda result: order.append(1))
        .after(lambda result: order.append(2))
    )
    chain()
    assert order == [1, 2]


def test_func_result_returned():
    chain = MiddlewareChain(lambda: "hello")
    assert chain() == "hello"


def test_non_callable_func_raises():
    with pytest.raises(TypeError):
        MiddlewareChain("not_callable")


def test_non_callable_before_raises():
    with pytest.raises(TypeError):
        MiddlewareChain(lambda: None).before("not_callable")


def test_non_callable_after_raises():
    with pytest.raises(TypeError):
        MiddlewareChain(lambda: None).after(42)


def test_before_and_after_ordering():
    """before runs first, then func, then after."""
    timeline = []
    chain = (
        MiddlewareChain(lambda x: timeline.append("func") or x)
        .before(lambda x: timeline.append("before"))
        .after(lambda x, result: timeline.append("after"))
    )
    chain(1)
    assert timeline == ["before", "func", "after"]
