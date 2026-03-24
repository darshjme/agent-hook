"""Tests for HookRegistry."""

import pytest
from agent_hook import Hook, HookPoint, HookRegistry


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def make_hook(point, name, priority=0):
    return Hook(point=point, handler=lambda *a, **kw: name, name=name, priority=priority)


# --------------------------------------------------------------------------- #
# register / list_hooks
# --------------------------------------------------------------------------- #

def test_register_returns_self():
    reg = HookRegistry()
    h = make_hook(HookPoint.PRE_CALL, "h1")
    assert reg.register(h) is reg


def test_register_and_list_single():
    reg = HookRegistry()
    h = make_hook(HookPoint.PRE_CALL, "h1")
    reg.register(h)
    assert reg.list_hooks(HookPoint.PRE_CALL) == [h]


def test_list_hooks_all_points():
    reg = HookRegistry()
    h1 = make_hook(HookPoint.PRE_CALL, "h1")
    h2 = make_hook(HookPoint.POST_CALL, "h2")
    reg.register(h1).register(h2)
    assert set(reg.list_hooks()) == {h1, h2}


def test_list_hooks_empty_by_default():
    reg = HookRegistry()
    assert reg.list_hooks(HookPoint.ON_ERROR) == []


def test_register_invalid_type_raises():
    reg = HookRegistry()
    with pytest.raises(TypeError):
        reg.register("not_a_hook")


# --------------------------------------------------------------------------- #
# priority ordering
# --------------------------------------------------------------------------- #

def test_hooks_ordered_by_priority():
    reg = HookRegistry()
    order = []
    reg.register(Hook(HookPoint.PRE_CALL, lambda: order.append(2), name="b", priority=2))
    reg.register(Hook(HookPoint.PRE_CALL, lambda: order.append(0), name="a", priority=0))
    reg.register(Hook(HookPoint.PRE_CALL, lambda: order.append(1), name="c", priority=1))
    reg.fire(HookPoint.PRE_CALL)
    assert order == [0, 1, 2]


# --------------------------------------------------------------------------- #
# @on decorator
# --------------------------------------------------------------------------- #

def test_on_decorator_registers_hook():
    reg = HookRegistry()

    @reg.on(HookPoint.POST_CALL)
    def my_handler(x):
        return x + 1

    hooks = reg.list_hooks(HookPoint.POST_CALL)
    assert len(hooks) == 1
    assert hooks[0].name == "my_handler"


def test_on_decorator_returns_original_fn():
    reg = HookRegistry()

    @reg.on(HookPoint.PRE_CALL)
    def greet(name):
        return f"hello {name}"

    assert greet("world") == "hello world"


def test_on_decorator_priority():
    reg = HookRegistry()

    @reg.on(HookPoint.PRE_CALL, priority=10)
    def low_priority(): pass

    hooks = reg.list_hooks(HookPoint.PRE_CALL)
    assert hooks[0].priority == 10


# --------------------------------------------------------------------------- #
# fire
# --------------------------------------------------------------------------- #

def test_fire_returns_all_results():
    reg = HookRegistry()
    reg.register(Hook(HookPoint.PRE_CALL, lambda: 1, name="a"))
    reg.register(Hook(HookPoint.PRE_CALL, lambda: 2, name="b"))
    results = reg.fire(HookPoint.PRE_CALL)
    assert set(results) == {1, 2}


def test_fire_empty_point_returns_empty_list():
    reg = HookRegistry()
    assert reg.fire(HookPoint.ON_CONTEXT_TRIM) == []


# --------------------------------------------------------------------------- #
# fire_until_false
# --------------------------------------------------------------------------- #

def test_fire_until_false_all_pass():
    reg = HookRegistry()
    reg.register(Hook(HookPoint.PRE_CALL, lambda: True, name="a"))
    reg.register(Hook(HookPoint.PRE_CALL, lambda: True, name="b"))
    assert reg.fire_until_false(HookPoint.PRE_CALL) is True


def test_fire_until_false_stops_on_false():
    called = []
    reg = HookRegistry()
    reg.register(Hook(HookPoint.PRE_CALL, lambda: called.append(1) or False, name="a", priority=0))
    reg.register(Hook(HookPoint.PRE_CALL, lambda: called.append(2), name="b", priority=1))
    result = reg.fire_until_false(HookPoint.PRE_CALL)
    assert result is False
    assert 2 not in called  # second hook must NOT have run


def test_fire_until_false_empty_returns_true():
    reg = HookRegistry()
    assert reg.fire_until_false(HookPoint.ON_ERROR) is True


# --------------------------------------------------------------------------- #
# remove
# --------------------------------------------------------------------------- #

def test_remove_hook_by_name():
    reg = HookRegistry()
    h = make_hook(HookPoint.PRE_CALL, "to_remove")
    reg.register(h)
    reg.remove("to_remove")
    assert reg.list_hooks(HookPoint.PRE_CALL) == []


def test_remove_nonexistent_raises():
    reg = HookRegistry()
    with pytest.raises(KeyError):
        reg.remove("ghost")
