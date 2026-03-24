"""agent-hook: Lifecycle hooks and middleware for LLM agents."""

from .hook_point import HookPoint
from .hook import Hook
from .registry import HookRegistry
from .middleware import MiddlewareChain

__all__ = ["HookPoint", "Hook", "HookRegistry", "MiddlewareChain"]
__version__ = "1.0.0"
