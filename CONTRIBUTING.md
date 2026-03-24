# Contributing to agent-hook

Thank you for your interest in contributing!

## Setup

```bash
git clone https://github.com/darshjme-codes/agent-hook
cd agent-hook
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Guidelines

- Keep zero runtime dependencies.
- Add tests for every new feature or bug fix.
- Follow PEP 8; type-hint all public APIs.
- Open an issue before large changes.
- One feature per PR.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
