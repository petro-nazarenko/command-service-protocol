# Contributing to CSP

Thank you for your interest in the Command Service Protocol.

CSP is an open standard. Contributions are welcome across four areas: the specification, the reference implementation, the compliance suite, and SDKs.

---

## What You Can Contribute

### 1. Specification Feedback
- Ambiguities or gaps in RFC‑CSP‑1.0 or CSS‑1.0
- Edge cases not covered by the grammar or error model
- Proposals for CSP‑1.1 extensions

Open an issue with the label `spec`.

### 2. Reference Implementation
- Bug fixes in `parser.py`, `generator.py`, `updater.py`
- Full implementation of modifiers not yet supported in MVP
- CLI improvements (`csp` tool)

### 3. Compliance Test Cases
- Valid command examples with expected one-liner output
- Invalid command examples with expected error output
- Edge cases that implementations commonly get wrong

Test cases live in `compliance/valid/` and `compliance/invalid/` as YAML files.

### 4. SDKs in Other Languages
- JavaScript / TypeScript
- Go
- Rust
- Any other language

SDKs must conform to CSS‑1.0. Include a compliance test run in your PR.

---

## How to Contribute

### Step 1 — Open an issue first

Before writing code or editing the spec, open an issue to describe what you want to do. This avoids duplicate work and ensures alignment with the standard.

### Step 2 — Fork and branch

```bash
git clone https://github.com/petro-nazarenko/command-service-protocol
cd command-service-protocol
git checkout -b your-feature-or-fix
```

### Step 3 — Make your changes

Follow the conventions below. Keep changes focused — one concern per PR.

### Step 4 — Run tests

```bash
pip install csprotocol
python -m pytest tests/
```

All tests must pass before submitting.

### Step 5 — Submit a pull request

Include in your PR description:
- What you changed and why
- Which part of CSS‑1.0 it relates to (if applicable)
- Any edge cases considered

---

## Code Conventions

- Python 3.10+
- Type hints required
- No external dependencies in `csprotocol/` core
- Errors must follow the CSS‑1.0 error model exactly:
  - `ERROR: syntax: <description>`
  - `ERROR: semantic: <description>`
  - `ERROR: runtime: <description>`

---

## Compliance Test Format

```yaml
# compliance/valid/basic.yaml
- input: "g"
  output: 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=False)"'

- input: 'g "Add CLI support"'
  output: 'python3 -c "import updater; updater.run(update_version=True, idea='"'"'Add CLI support'"'"', dry=False)"'
```

```yaml
# compliance/invalid/syntax.yaml
- input: "go"
  output: "ERROR: syntax: unknown command 'go'"

- input: "g 'bad quotes'"
  output: "ERROR: syntax: invalid quotes"
```

---

## Conduct

Be direct and professional. Focus on the protocol, not personalities. Disagreements about the spec are welcome — that is how standards improve.

---

## Questions

Open an issue or start a discussion in the GitHub Discussions tab.
