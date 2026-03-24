"""HookPoint enum — lifecycle points for LLM agent interception."""

from enum import Enum, auto


class HookPoint(Enum):
    """Lifecycle points at which hooks can be registered."""

    PRE_CALL = auto()
    POST_CALL = auto()
    ON_ERROR = auto()
    ON_TOOL_USE = auto()
    ON_CONTEXT_TRIM = auto()
    PRE_RESPONSE = auto()
    POST_RESPONSE = auto()
