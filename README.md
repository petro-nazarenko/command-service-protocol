# Command Service Protocol (CSP)

**A deterministic, text-based command interface for AI-assisted project management.**

[![Status](https://img.shields.io/badge/status-draft-yellow)](./standard/RFC-CSP-1.0.md)
[![Spec](https://img.shields.io/badge/spec-CSS--1.0-blue)](./standard/CSS-1.0.md)
[![PyPI](https://img.shields.io/badge/pypi-csprotocol-green)](https://pypi.org/project/csprotocol)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

---

## The Problem

AI agents are powerful but unpredictable. Without a formal interface, commands issued to LLMs become ambiguous, non-deterministic, and impossible to audit. Different models interpret the same instruction differently. There is no standard.

## The Solution

CSP defines a strict, minimal command grammar that transforms natural-language-style commands into deterministic Python one-liners. Same input — same output. Always.

```
g "Add CLI support"
```
```
python3 -c "import updater; updater.run(update_version=True, idea='Add CLI support', dry=False)"
```

CSP is to AI agents what HTTP is to web communication — a protocol, not a product.

---

## Quick Start

### Install

```bash
pip install csprotocol
```

### Use as a Python library

```python
from csprotocol import parse_command, generate_one_liner

cmd = parse_command('g "Add CLI support"')
print(generate_one_liner(cmd))
# python3 -c "import updater; updater.run(update_version=True, idea='Add CLI support', dry=False)"
```

### Use as a CLI tool

```bash
csp 'g "Add CLI support"'
csp 'up dry'
csp 'm force'
```

### Use as an LLM system prompt

Drop [`prompts/system-prompt-mvp.md`](./prompts/system-prompt-mvp.md) into any LLM to turn it into a compliant CSP interpreter. The model will accept CSP commands and return valid one-liners — nothing else.

---

## Command Reference

### Base Commands

| Command | Aliases | Meaning |
|---------|---------|---------|
| `g` | `gen`, `generate` | Generate one-liner, bump version, update project state |
| `up` | `update` | Same as `g`, but no version bump |
| `m` | `merge` | Merge session state into local files |
| `sync` | — | Full sync: update + merge + version bump |

### Modifiers

| Modifier | Type | Effect |
|----------|------|--------|
| `"text"` | argument | Shorthand for `idea="text"` |
| `idea="text"` | key=value | Add idea to Ideas Inbox |
| `note="text"` | key=value | Add note to Notes section |
| `force` | flag | Override merge conflicts |
| `dry` | flag | Generate but do not execute |
| `no-version` | flag | Skip version bump |
| `no-status` | flag | Skip status updates |
| `only-version` | flag | Only bump version |
| `only-status` | flag | Only update statuses |
| `validate` | flag | Validate project structure first |
| `export` | flag | Export project state |

---

## Examples

```bash
# Basic generate
g

# Add an idea
g "Improve onboarding flow"

# Update without bumping version
up "Refactor parser" no-version

# Dry run — see what would happen, don't execute
g dry

# Merge, overriding conflicts
m force

# Full sync with validation
sync validate

# Dry merge — preview only
m dry
```

---

## Error Model

CSP returns structured errors — never silent failures.

```
ERROR: syntax: unknown command 'go'
ERROR: syntax: invalid quotes
ERROR: semantic: multiple arguments not allowed
ERROR: semantic: only-version and no-version cannot be used together
ERROR: runtime: project.json not found
```

---

## Architecture

```
User input
    │
    ▼
parser.py        — tokenize, validate syntax, build Command object
    │
    ▼
generator.py     — apply semantics, produce Python one-liner
    │
    ▼
python3 -c "..."  — execute in your environment (Termux, shell, CI)
    │
    ▼
updater.py       — perform actual project updates
```

---

## Specification

CSP is formally specified in two documents:

- **[RFC‑CSP‑1.0](./standard/RFC-CSP-1.0.md)** — the full protocol standard
- **[CSS‑1.0](./standard/CSS-1.0.md)** — normative syntax, semantics, FSM, and error model

These documents are the source of truth. All implementations must conform to CSS‑1.0.

---

## Roadmap

| Package | Status |
|---------|--------|
| 1 — Open Standard Release | 🔴 In progress |
| 2 — Reference Implementation 1.0 | 🔴 In progress |
| 3 — Compliance Suite | 🟡 Planned |
| 4 — SDKs (Python, TS, Go, Rust) | 🟡 Planned |
| 5 — CSP‑Transport (HTTP, WS, IPC) | 🟢 Future |
| 6 — CSP‑Security | 🟢 Future |
| 7 — CSP‑1.1 | 🟢 Future |

Full roadmap: [roadmap.md](./roadmap.md)

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

CSP welcomes:
- compliance test cases
- SDK implementations in other languages
- feedback on the specification
- real-world usage reports

---

## License

MIT — see [LICENSE](./LICENSE).

---

## Author

**Petro Nazarenko** — AI Solutions Architect
[github.com/petro-nazarenko/command-service-protocol](https://github.com/petro-nazarenko/command-service-protocol)

---

*CSP — deterministic commands for AI agents.*
