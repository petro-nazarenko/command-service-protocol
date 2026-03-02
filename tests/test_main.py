"""
tests/test_main.py
CSS-1.0 §8 — FSM, §5 — Output contract, §6 — Error model

Tests for csprotocol.main.handle()
End-to-end integration: raw string → one-liner or ERROR
"""

import sys
sys.path.insert(0, '/home/claude')

from csprotocol.main import handle


# ──────────────────────────────────────────────
# End-to-end valid commands
# ──────────────────────────────────────────────

class TestHandleValid:

    def test_g(self):
        assert handle("g") == 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=False)"'

    def test_up(self):
        assert handle("up") == 'python3 -c "import updater; updater.run(update_version=False, idea=None, dry=False)"'

    def test_m(self):
        assert handle("m") == 'python3 -c "import updater; updater.merge(force=False, dry=False)"'

    def test_g_dry(self):
        assert handle("g dry") == 'python3 -c "import updater; updater.run(update_version=True, idea=None, dry=True)"'

    def test_m_force(self):
        assert handle("m force") == 'python3 -c "import updater; updater.merge(force=True, dry=False)"'

    def test_m_force_dry(self):
        assert handle("m force dry") == 'python3 -c "import updater; updater.merge(force=True, dry=True)"'

    def test_g_with_idea(self):
        result = handle('g "Add CLI support"')
        assert result == "python3 -c \"import updater; updater.run(update_version=True, idea='Add CLI support', dry=False)\""

    def test_up_with_idea_and_dry(self):
        result = handle('up "Improve UX" dry')
        assert "idea='Improve UX'" in result
        assert "dry=True" in result
        assert "update_version=False" in result

    def test_g_dry_before_idea(self):
        """CSS-1.0 §3.1 — modifier ordering is not semantically significant"""
        result_a = handle('g dry "Add docs"')
        result_b = handle('g "Add docs" dry')
        assert result_a == result_b

    def test_m_dry_force_order_independent(self):
        assert handle("m dry force") == handle("m force dry")


# ──────────────────────────────────────────────
# End-to-end error handling
# ──────────────────────────────────────────────

class TestHandleErrors:

    def test_empty_string_returns_error(self):
        result = handle("")
        assert result.startswith("ERROR:")

    def test_unknown_command_returns_error(self):
        result = handle("go")
        assert result == "ERROR: syntax: unknown command 'go'"

    def test_single_quotes_returns_error(self):
        result = handle("g 'bad'")
        assert result == "ERROR: syntax: invalid quotes"

    def test_unclosed_quote_returns_error(self):
        result = handle('g "unclosed')
        assert result == "ERROR: syntax: invalid quotes"

    def test_multiple_arguments_returns_error(self):
        result = handle('g "First" "Second"')
        assert result == "ERROR: semantic: multiple arguments not allowed"

    def test_unknown_flag_returns_error(self):
        result = handle("g fast")
        assert result.startswith("ERROR: syntax:")

    def test_error_never_raises_exception(self):
        """handle() must always return a string, never raise"""
        inputs = ["", "go", "g 'x'", 'g "a" "b"', "g fast"]
        for text in inputs:
            result = handle(text)
            assert isinstance(result, str)
            assert result.startswith("ERROR:")

    def test_valid_never_returns_error(self):
        """Valid commands must never return ERROR:"""
        inputs = ["g", "up", "m", "g dry", "m force", 'm force dry', 'g "idea"']
        for text in inputs:
            result = handle(text)
            assert not result.startswith("ERROR:"), f"Unexpected error for: {text!r}"


# ──────────────────────────────────────────────
# Determinism — CSS-1.0 §5.2
# ──────────────────────────────────────────────

class TestDeterminism:

    def test_same_input_same_output(self):
        for _ in range(5):
            assert handle("g") == handle("g")

    def test_same_idea_same_output(self):
        cmd = 'g "Add CLI support"'
        results = {handle(cmd) for _ in range(5)}
        assert len(results) == 1
