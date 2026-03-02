# CSP Roadmap

**Command Service Protocol**
Author: Petro Nazarenko — AI Solutions Architect
Repository: github.com/petro-nazarenko/command-service-protocol
PyPI: csprotocol
Updated: 02 March 2026

---

## Vision

CSP is not a product — it is an infrastructure standard.
The goal is to make AI agents deterministic, interoperable, and auditable through a strict, minimal, and extensible command protocol — the way HTTP standardized web communication and JSON standardized data exchange.

---

## Current Status

| Artifact | Status |
|----------|--------|
| RFC‑CSP‑1.0 | ✅ Draft complete |
| CSS‑1.0 | ✅ Draft complete |
| System prompt (MVP) | ✅ Ready |
| MVP implementation (parser / generator / updater) | ✅ Working |
| End-to-end cycle verified | ✅ Confirmed |

The protocol is fully specified and proven in MVP. The roadmap below describes the path from MVP to industry standard.

---

## Package 1 — Open Standard Release

**Goal:** Make the standard publicly accessible and understandable.

- [ ] Create public GitHub repository (`command-service-protocol`)
- [ ] Publish RFC‑CSP‑1.0
- [ ] Publish CSS‑1.0
- [ ] Publish MVP reference implementation
- [ ] Publish system prompt
- [ ] Write README with value proposition and usage examples
- [ ] Add MIT license
- [ ] Add CONTRIBUTING.md

**Milestone:** Standard is publicly available and forkable.

---

## Package 2 — Reference Implementation 1.0

**Goal:** Give the industry a complete, production-ready reference implementation.

- [ ] Full CSS‑1.0 command support (`g`, `gen`, `generate`, `up`, `update`, `m`, `merge`, `sync`)
- [ ] Full modifier support (`force`, `dry`, `no-version`, `no-status`, `only-version`, `only-status`, `validate`, `export`, `idea=`, `note=`)
- [ ] Real updater:
  - file update engine
  - version management
  - task management
  - workflow generation
- [ ] CLI tool: `csp`
- [ ] Publish to PyPI as `csprotocol`

**Milestone:** `pip install csprotocol` works. `csp "g"` produces a valid one-liner.

---

## Package 3 — Compliance Suite

**Goal:** Enable any developer to verify their agent is CSP-compliant.

- [ ] Test corpus: valid commands
- [ ] Test corpus: invalid commands (syntax + semantic errors)
- [ ] Edge case coverage
- [ ] Determinism tests (same input → same output)
- [ ] Cross-implementation compatibility tests
- [ ] Compliance report format

**Milestone:** Any CSP implementation can be tested against the suite and certified.

---

## Package 4 — SDKs

**Goal:** Lower the barrier to adopting CSP in any stack.

- [ ] Python SDK (`csprotocol`) — parser, generator, validator, LLM integration
- [ ] JavaScript / TypeScript SDK
- [ ] Go SDK *(optional)*
- [ ] Rust SDK *(optional)*

Each SDK includes:
- command parser
- one-liner generator
- semantic validator
- LLM system prompt adapter

**Milestone:** Developers can integrate CSP in their language of choice with a single import.

---

## Package 5 — CSP‑Transport

**Goal:** Enable agents to communicate with each other through CSP.

- [ ] HTTP API specification
- [ ] WebSocket API specification
- [ ] IPC specification (local agent mode)
- [ ] Reference server implementation

**Milestone:** Two independent CSP agents can exchange commands over a defined transport.

---

## Package 6 — CSP‑Security

**Goal:** Make CSP safe for production and multi-agent environments.

- [ ] Command signing
- [ ] Integrity verification
- [ ] Access control model
- [ ] Sandbox execution mode
- [ ] Security threat model document

**Milestone:** CSP commands can be trusted, verified, and sandboxed.

---

## Package 7 — CSP‑1.1

**Goal:** Evolve the standard while preserving backward compatibility.

- [ ] Capability negotiation
- [ ] Feature flags
- [ ] Formal backward compatibility rules
- [ ] Extended merge profiles
- [ ] RFC‑CSP‑1.1 published

**Milestone:** CSP‑1.1 is a superset of CSP‑1.0 with no breaking changes.

---

## Summary

| Package | Deliverable | Priority |
|---------|-------------|----------|
| 1 | Open Standard Release | 🔴 Now |
| 2 | Reference Implementation 1.0 | 🔴 Now |
| 3 | Compliance Suite | 🟡 Next |
| 4 | SDKs | 🟡 Next |
| 5 | CSP‑Transport | 🟢 Future |
| 6 | CSP‑Security | 🟢 Future |
| 7 | CSP‑1.1 | 🟢 Future |

---

*CSP — deterministic commands for AI agents.*
