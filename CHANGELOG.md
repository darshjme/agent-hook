# Changelog

All notable changes to **agent-hook** are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-03-24

### Added
- `HookPoint` enum with seven lifecycle points: `PRE_CALL`, `POST_CALL`,
  `ON_ERROR`, `ON_TOOL_USE`, `ON_CONTEXT_TRIM`, `PRE_RESPONSE`, `POST_RESPONSE`.
- `Hook` class — wraps a handler callable with name, priority, and lifecycle binding.
- `HookRegistry` — registers, fires, and removes hooks; supports priority ordering,
  guard pattern via `fire_until_false`, and a `@registry.on(point)` decorator factory.
- `MiddlewareChain` — fluent before/after wrapper for any callable.
- Full pytest test suite (22+ tests).
- Zero runtime dependencies.
