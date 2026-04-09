"""
tests/test_compliance.py
CSS-1.0 compliance runner
"""
import os

import pytest

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from csprotocol.main import handle

COMPLIANCE_DIR = os.path.join(os.path.dirname(__file__), "..", "compliance")

def load_cases(path):
    if not HAS_YAML or not os.path.exists(path):
        return []
    with open(path) as f:
        return yaml.safe_load(f) or []

def case_id(case):
    return case.get("id", case.get("input", "unknown"))

VALID_BASIC = load_cases(os.path.join(COMPLIANCE_DIR, "valid", "basic.yaml"))
VALID_IDEAS = load_cases(os.path.join(COMPLIANCE_DIR, "valid", "ideas.yaml"))
INVALID_SYN = load_cases(os.path.join(COMPLIANCE_DIR, "invalid", "syntax.yaml"))
INVALID_SEM = load_cases(os.path.join(COMPLIANCE_DIR, "invalid", "semantic.yaml"))

skip = pytest.mark.skipif(not HAS_YAML, reason="pyyaml not installed")

@skip
class TestComplianceValidBasic:
    @pytest.mark.parametrize("case", VALID_BASIC, ids=[case_id(c) for c in VALID_BASIC])
    def test_valid_basic(self, case):
        result = handle(case["input"])
        assert result == case["output"]

@skip
class TestComplianceValidIdeas:
    @pytest.mark.parametrize("case", VALID_IDEAS, ids=[case_id(c) for c in VALID_IDEAS])
    def test_valid_ideas(self, case):
        result = handle(case["input"])
        assert result == case["expected"]

@skip
class TestComplianceInvalidSyntax:
    @pytest.mark.parametrize("case", INVALID_SYN, ids=[case_id(c) for c in INVALID_SYN])
    def test_invalid_syntax(self, case):
        result = handle(case["input"])
        assert result == case["expected"]

@skip
class TestComplianceInvalidSemantic:
    @pytest.mark.parametrize("case", INVALID_SEM, ids=[case_id(c) for c in INVALID_SEM])
    def test_invalid_semantic(self, case):
        result = handle(case["input"])
        assert result == case["expected"]
