# Changelog

All notable changes to the Command Service Protocol will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

Changes staged for the next release.

---

## [1.0.0-draft] — 2026-03-02

### Added — Specification

- **RFC‑CSP‑1.0** — full formal standard document
  - Abstract, introduction, requirements language
  - Embedded CSS‑1.0 as normative definition
  - Merge rules, extensibility guidelines, examples
- **CSS‑1.0** — normative Command Service Specification
  - Grammar (EBNF): `g`, `up`, `m`, `sync` base commands
  - Full modifier set: `force`, `dry`, `no-version`, `no-status`, `only-version`, `only-status`, `validate`, `export`, `idea=`, `note=`
  - Argument semantics: bare argument → `idea=`
  - Priority rules for conflicting modifiers
  - Output contract: deterministic, idempotent, single-line one-liner
  - Error model: `syntax`, `semantic`, `runtime` error classes
  - Finite state machine (FSM): Idle → Parsed → Validated → Generated → Executed
  - Merge rules: conflict detection, resolution, `force` behavior
  - Compliance requirements

### Added — Reference Implementation (MVP)

- `parser.py` — tokenizer using `shlex`, `Command` dataclass, syntax validation
- `generator.py` — one-liner builder for `g`, `up`, `m`
- `updater.py` — action executor stub (`run`, `merge`)
- `main.py` — interactive REPL loop
- End-to-end cycle verified:
  ```
  g "Add CLI" → Command(base='g', argument='Add CLI') →
  python3 -c "import updater; updater.run(update_version=True, idea='Add CLI', dry=False)" →
  Executing: ['bump_version', 'update_statuses', 'update_next_step', 'update_workflow', 'add_idea:Add CLI']
  ```

### Added — LLM System Prompt

- `prompts/system-prompt-mvp.md` — MVP-mode CSP interpreter prompt
  - Supported commands: `g`, `up`, `m`
  - Supported flags: `force`, `dry`
  - Strict output contract: one-liner or `ERROR:` only
  - No explanations, no commentary

### Added — Project Infrastructure

- `README.md` — project overview, quick start, command reference, architecture
- `roadmap.md` — 7-package release roadmap
- `CONTRIBUTING.md` — contribution guide, test format, code conventions
- `LICENSE` — MIT
- `CHANGELOG.md` — this file
- GitHub repository structure defined

### Added — Compliance Suite (initial)

- `compliance/valid/basic.yaml` — 8 valid command test cases
- `compliance/valid/ideas.yaml` — 6 idea argument test cases
- `compliance/invalid/syntax.yaml` — 9 syntax error test cases
- `compliance/invalid/semantic.yaml` — 3 semantic error test cases
- `compliance/README.md` — how to run, format spec, coverage table

---

## Roadmap Targets

| Version | Target | Description |
|---------|--------|-------------|
| `1.0.0` | Package 2 | Full CSS‑1.0 implementation, `csp` CLI, PyPI release |
| `1.0.1` | Package 3 | Expanded compliance suite, edge case coverage |
| `1.1.0` | Package 7 | CSS‑1.1: capability negotiation, extended merge profiles |

---

[Unreleased]: https://github.com/petro-nazarenko/command-service-protocol/compare/v1.0.0-draft...HEAD
[1.0.0-draft]: https://github.com/petro-nazarenko/command-service-protocol/releases/tag/v1.0.0-draft
