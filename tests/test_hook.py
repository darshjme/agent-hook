"""Tests for Hook."""

import pytest
from agent_hook import Hook, HookPoint


def test_hook_basic_fields():
    def handler(): pass
    h = Hook(point=HookPoint.PRE_CALL, handler=handler, name="my_hook", priority=5)
    assert h.point == HookPoint.PRE_CALL
    assert h.handler is handler
    assert h.name == "my_hook"
    assert h.priority == 5


def test_hook_auto_name():
    h = Hook(point=HookPoint.POST_CALL, handler=lambda: None)
    assert h.name  # non-empty auto-generated UUID


def test_hook_default_priority():
    h = Hook(point=HookPoint.ON_ERROR, handler=lambda: None)
    assert h.priority == 0


def test_hook_execute_passes_args():
    results = []

    def handler(x, y, z=0):
        results.append((x, y, z))

    h = Hook(point=HookPoint.ON_TOOL_USE, handler=handler)
    h.execute(1, 2, z=3)
    assert results == [(1, 2, 3)]


def test_hook_execute_returns_value():
    h = Hook(point=HookPoint.PRE_CALL, handler=lambda x: x * 2)
    assert h.execute(21) == 42


def test_hook_invalid_point_raises():
    with pytest.raises(TypeError):
        Hook(point="PRE_CALL", handler=lambda: None)


def test_hook_non_callable_raises():
    with pytest.raises(TypeError):
        Hook(point=HookPoint.PRE_CALL, handler="not_a_function")
