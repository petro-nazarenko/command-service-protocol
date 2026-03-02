# CSP Compliance Suite

Test cases for verifying CSS-1.0 compliance in any CSP implementation.

## Structure

```
compliance/
├── valid/
│   ├── basic.yaml     — g, up, m with no modifiers; flag combinations
│   └── ideas.yaml     — argument handling, idea= semantics
└── invalid/
    ├── syntax.yaml    — malformed input, unknown commands/flags, bad quotes
    └── semantic.yaml  — multiple arguments, conflicting modifiers
```

## Test Case Format

Each test case is a YAML object with three fields:

```yaml
- id: v-basic-01
  description: g with no arguments or flags
  input: "g"
  expected: 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=False)"'
```

| Field | Description |
|-------|-------------|
| `id` | Unique identifier. Prefix: `v-` = valid, `i-syn-` = syntax error, `i-sem-` = semantic error |
| `description` | Human-readable description of what is being tested |
| `input` | Raw command string as received by the parser |
| `expected` | Exact expected output string |

## Running the Suite

```bash
pip install csprotocol pytest pyyaml

python -m pytest compliance/ --tb=short
```

Or run manually against any implementation:

```python
import yaml
from csprotocol import handle

with open("compliance/valid/basic.yaml") as f:
    cases = yaml.safe_load(f)

for case in cases:
    result = handle(case["input"])
    assert result == case["expected"], f"FAIL [{case['id']}]: {result!r}"
    print(f"PASS [{case['id']}]")
```

## Coverage

| File | Cases | Tests |
|------|-------|-------|
| `valid/basic.yaml` | 8 | Flags, combinations, order-independence |
| `valid/ideas.yaml` | 6 | Argument as idea=, multi-word, dry+idea |
| `invalid/syntax.yaml` | 9 | Unknown commands, bad quotes, unknown flags |
| `invalid/semantic.yaml` | 3 | Multiple arguments |

## Adding Test Cases

1. Choose the correct file based on expected output type.
2. Follow the `id` naming convention.
3. Ensure `expected` is the exact string the implementation must return.
4. Submit a PR with a description of what edge case you are covering.
