"""
tests/test_generator.py
CSS-1.0 §5 — Output contract

Tests for csprotocol.generator.generate_one_liner()
"""

import pytest

from csprotocol.generator import generate_one_liner
from csprotocol.parser import Command

# ──────────────────────────────────────────────
# Output contract — CSS-1.0 §5.2
# ──────────────────────────────────────────────

class TestOutputContract:

    def test_output_starts_with_python3(self):
        cmd = Command(base="g")
        result = generate_one_liner(cmd)
        assert result.startswith('python3 -c "')

    def test_output_is_single_line(self):
        """CSS-1.0 §5.2 — single-line, no embedded newlines"""
        cmd = Command(base="g")
        result = generate_one_liner(cmd)
        assert "\n" not in result

    def test_output_is_deterministic(self):
        """CSS-1.0 §5.2 — same input → same output"""
        cmd_a = Command(base="g", argument="Add CLI", flags={"dry"})
        cmd_b = Command(base="g", argument="Add CLI", flags={"dry"})
        assert generate_one_liner(cmd_a) == generate_one_liner(cmd_b)


# ──────────────────────────────────────────────
# g command — CSS-1.0 §4.6.1
# ──────────────────────────────────────────────

class TestGenerateCommand:

    def test_g_no_args(self):
        cmd = Command(base="g")
        result = generate_one_liner(cmd)
        assert result == 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=False)"'

    def test_g_with_idea(self):
        cmd = Command(base="g", argument="Add CLI support")
        result = generate_one_liner(cmd)
        assert result == "python3 -c \"import updater; updater.run(update_version=True, idea='Add CLI support', dry=False)\""

    def test_g_dry(self):
        cmd = Command(base="g", flags={"dry"})
        result = generate_one_liner(cmd)
        assert result == 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=True)"'

    def test_g_with_idea_and_dry(self):
        cmd = Command(base="g", argument="Refactor parser", flags={"dry"})
        result = generate_one_liner(cmd)
        assert "idea='Refactor parser'" in result
        assert "dry=True" in result
        assert "update_version=True" in result

    def test_g_update_version_is_true(self):
        """CSS-1.0 §4.6.1 — g must set update_version=True"""
        cmd = Command(base="g")
        result = generate_one_liner(cmd)
        assert "update_version=True" in result


# ──────────────────────────────────────────────
# up command — CSS-1.0 §4.6.2
# ──────────────────────────────────────────────

class TestUpdateCommand:

    def test_up_no_args(self):
        cmd = Command(base="up")
        result = generate_one_liner(cmd)
        assert result == 'python3 -c "import updater; updater.run(update_version=False, idea=None, dry=False)"'

    def test_up_update_version_is_false(self):
        """CSS-1.0 §4.6.2 — up must NOT bump version"""
        cmd = Command(base="up")
        result = generate_one_liner(cmd)
        assert "update_version=False" in result

    def test_up_with_idea(self):
        cmd = Command(base="up", argument="Improve UX")
        result = generate_one_liner(cmd)
        assert "idea='Improve UX'" in result
        assert "update_version=False" in result

    def test_up_dry(self):
        cmd = Command(base="up", flags={"dry"})
        result = generate_one_liner(cmd)
        assert "dry=True" in result
        assert "update_version=False" in result


# ──────────────────────────────────────────────
# m command — CSS-1.0 §4.6.3
# ──────────────────────────────────────────────

class TestMergeCommand:

    def test_m_no_flags(self):
        cmd = Command(base="m")
        result = generate_one_liner(cmd)
        assert result == 'python3 -c "import updater; updater.merge(force=False, dry=False)"'

    def test_m_force(self):
        cmd = Command(base="m", flags={"force"})
        result = generate_one_liner(cmd)
        assert "force=True" in result
        assert "dry=False" in result

    def test_m_dry(self):
        cmd = Command(base="m", flags={"dry"})
        result = generate_one_liner(cmd)
        assert "dry=True" in result
        assert "force=False" in result

    def test_m_force_and_dry(self):
        cmd = Command(base="m", flags={"force", "dry"})
        result = generate_one_liner(cmd)
        assert "force=True" in result
        assert "dry=True" in result

    def test_m_calls_merge_not_run(self):
        cmd = Command(base="m")
        result = generate_one_liner(cmd)
        assert "updater.merge(" in result
        assert "updater.run(" not in result


# ──────────────────────────────────────────────
# Idea quoting — CSS-1.0 §5.2 safety
# ──────────────────────────────────────────────

class TestIdeaQuoting:

    def test_idea_wrapped_in_single_quotes(self):
        cmd = Command(base="g", argument="Add CLI")
        result = generate_one_liner(cmd)
        assert "idea='Add CLI'" in result

    def test_idea_none_is_bare_none(self):
        cmd = Command(base="g")
        result = generate_one_liner(cmd)
        assert "idea=None" in result

    def test_idea_with_single_quote_escaped(self):
        cmd = Command(base="g", argument="It's working")
        result = generate_one_liner(cmd)
        assert "\\'" in result


# ──────────────────────────────────────────────
# Unsupported commands
# ──────────────────────────────────────────────

class TestUnsupportedCommands:

    def test_unknown_base_raises(self):
        cmd = Command(base="sync")
        with pytest.raises(ValueError, match="semantic: unsupported command"):
            generate_one_liner(cmd)
