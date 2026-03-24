"""Tests for HookPoint enum."""

import pytest
from agent_hook import HookPoint


def test_all_points_defined():
    expected = {
        "PRE_CALL", "POST_CALL", "ON_ERROR", "ON_TOOL_USE",
        "ON_CONTEXT_TRIM", "PRE_RESPONSE", "POST_RESPONSE",
    }
    assert {p.name for p in HookPoint} == expected


def test_hook_points_are_unique():
    values = [p.value for p in HookPoint]
    assert len(values) == len(set(values))


def test_hook_point_is_enum():
    from enum import Enum
    assert issubclass(HookPoint, Enum)
