# agent-hook

> Lifecycle hooks and middleware for LLM agents — zero dependencies, Python 3.10+

`agent-hook` lets you intercept any point in an LLM agent's execution loop
without touching the agent's core code.  Log calls, track costs, enforce safety
guards, or trim context — all through a clean hook/middleware API.

## Install

```bash
pip install agent-hook
```

## Quick Start — Agent Call Interception

```python
from agent_hook import HookPoint, HookRegistry, MiddlewareChain

registry = HookRegistry()

# ── 1. Register hooks via decorator ───────────────────────────────────────────

@registry.on(HookPoint.PRE_CALL)
def log_pre_call(payload: dict):
    print(f"[PRE_CALL]  model={payload['model']}  tokens={payload['tokens']}")

@registry.on(HookPoint.POST_CALL)
def track_cost(payload: dict):
    cost = payload.get("usage", {}).get("total_tokens", 0) * 0.000002
    print(f"[POST_CALL] cost=${cost:.6f}")

@registry.on(HookPoint.ON_ERROR)
def alert_on_error(exc: Exception):
    print(f"[ON_ERROR]  {type(exc).__name__}: {exc}")

# ── 2. Safety guard — veto the call if payload is suspicious ──────────────────

@registry.on(HookPoint.PRE_CALL, priority=-1)   # runs before other PRE_CALL hooks
def safety_guard(payload: dict) -> bool:
    if payload.get("prompt", "").lower().startswith("ignore all"):
        print("[GUARD] Prompt injection detected — blocking call.")
        return False   # fire_until_false will stop here
    return True

# ── 3. Wrap your actual LLM call with MiddlewareChain ─────────────────────────

import openai  # hypothetical

def raw_llm_call(prompt: str, model: str = "gpt-4o") -> str:
    # In real usage, call your LLM SDK here
    return f"<response to: {prompt!r}>"

chain = (
    MiddlewareChain(raw_llm_call)
    .before(lambda prompt, model="gpt-4o": registry.fire(
        HookPoint.PRE_CALL, {"model": model, "tokens": len(prompt), "prompt": prompt}
    ))
    .after(lambda prompt, result, model="gpt-4o": registry.fire(
        HookPoint.POST_CALL, {"model": model, "usage": {"total_tokens": len(result)}}
    ))
)

# ── 4. Use the chain ──────────────────────────────────────────────────────────

payload = {"model": "gpt-4o", "tokens": 128, "prompt": "Explain quantum computing"}

# Guard check before calling
if registry.fire_until_false(HookPoint.PRE_CALL, payload):
    response = chain("Explain quantum computing", model="gpt-4o")
    print(response)
```

## API Reference

### `HookPoint`

```python
class HookPoint(Enum):
    PRE_CALL        # Before each LLM API call
    POST_CALL       # After a successful LLM API call
    ON_ERROR        # When any error occurs
    ON_TOOL_USE     # Before/after a tool/function call
    ON_CONTEXT_TRIM # When the context window is trimmed
    PRE_RESPONSE    # Before delivering response to user
    POST_RESPONSE   # After response delivered
```

### `Hook`

```python
Hook(point, handler, name=None, priority=0)
hook.execute(*args, **kwargs)   # invoke handler
```

### `HookRegistry`

```python
registry = HookRegistry()
registry.register(hook)                          # fluent
registry.on(point, priority=0)                   # decorator factory
registry.fire(point, *args, **kwargs)            # → list[any]
registry.fire_until_false(point, *args, **kwargs)# → bool
registry.list_hooks(point=None)                  # → list[Hook]
registry.remove(name)                            # raises KeyError if missing
```

### `MiddlewareChain`

```python
chain = MiddlewareChain(func)
chain.before(middleware)   # fluent; middleware(*args, **kwargs)
chain.after(middleware)    # fluent; middleware(*args, result=..., **kwargs)
result = chain(*args, **kwargs)
```

## License

MIT © Darshankumar Joshi
