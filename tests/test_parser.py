"""
tests/test_parser.py
CSS-1.0 §3 — Syntax, §4 — Semantics, §6.1-6.2 — Error model

Tests for csprotocol.parser.parse_command()
"""

import pytest

from csprotocol.parser import parse_command

# ──────────────────────────────────────────────
# Valid commands — base only
# ──────────────────────────────────────────────

class TestValidBaseCommands:

    def test_g_returns_command(self):
        cmd = parse_command("g")
        assert cmd.base == "g"
        assert cmd.argument is None
        assert cmd.flags == set()

    def test_up_returns_command(self):
        cmd = parse_command("up")
        assert cmd.base == "up"
        assert cmd.argument is None
        assert cmd.flags == set()

    def test_m_returns_command(self):
        cmd = parse_command("m")
        assert cmd.base == "m"
        assert cmd.argument is None
        assert cmd.flags == set()


# ──────────────────────────────────────────────
# Valid commands — flags
# ──────────────────────────────────────────────

class TestValidFlags:

    def test_g_dry(self):
        cmd = parse_command("g dry")
        assert cmd.base == "g"
        assert "dry" in cmd.flags

    def test_up_dry(self):
        cmd = parse_command("up dry")
        assert "dry" in cmd.flags

    def test_m_force(self):
        cmd = parse_command("m force")
        assert "force" in cmd.flags

    def test_m_dry(self):
        cmd = parse_command("m dry")
        assert "dry" in cmd.flags

    def test_m_force_and_dry(self):
        cmd = parse_command("m force dry")
        assert "force" in cmd.flags
        assert "dry" in cmd.flags

    def test_m_dry_force_order_independent(self):
        """CSS-1.0 §3.1 — ordering of modifiers is not semantically significant"""
        cmd_a = parse_command("m force dry")
        cmd_b = parse_command("m dry force")
        assert cmd_a == cmd_b

    def test_g_dry_force(self):
        cmd = parse_command("g dry force")
        assert "dry" in cmd.flags
        assert "force" in cmd.flags


# ──────────────────────────────────────────────
# Valid commands — arguments
# ──────────────────────────────────────────────

class TestValidArguments:

    def test_g_with_argument(self):
        """CSS-1.0 §4.2 — bare argument treated as idea="""
        cmd = parse_command('g "Add CLI support"')
        assert cmd.argument == "Add CLI support"

    def test_up_with_argument(self):
        cmd = parse_command('up "Improve UX"')
        assert cmd.argument == "Improve UX"

    def test_g_argument_multi_word(self):
        cmd = parse_command('g "Add support for multi-line commands"')
        assert cmd.argument == "Add support for multi-line commands"

    def test_g_argument_with_dry_flag(self):
        cmd = parse_command('g "Refactor parser" dry')
        assert cmd.argument == "Refactor parser"
        assert "dry" in cmd.flags

    def test_g_dry_before_argument(self):
        """CSS-1.0 §3.1 — modifier ordering is not semantically significant"""
        cmd = parse_command('g dry "Add docs"')
        assert cmd.argument == "Add docs"
        assert "dry" in cmd.flags

    def test_argument_with_special_characters(self):
        cmd = parse_command('g "Fix bug: handle edge-case #42"')
        assert cmd.argument == "Fix bug: handle edge-case #42"

    def test_empty_argument_string(self):
        cmd = parse_command('g ""')
        assert cmd.argument == ""


# ──────────────────────────────────────────────
# Command equality
# ──────────────────────────────────────────────

class TestCommandEquality:

    def test_equal_commands(self):
        a = parse_command("g")
        b = parse_command("g")
        assert a == b

    def test_unequal_base(self):
        assert parse_command("g") != parse_command("up")

    def test_unequal_argument(self):
        a = parse_command('g "Idea A"')
        b = parse_command('g "Idea B"')
        assert a != b

    def test_unequal_flags(self):
        a = parse_command("g dry")
        b = parse_command("g")
        assert a != b


# ──────────────────────────────────────────────
# Syntax errors — CSS-1.0 §6.1
# ──────────────────────────────────────────────

class TestSyntaxErrors:

    def test_empty_string(self):
        with pytest.raises(ValueError, match="syntax: empty command"):
            parse_command("")

    def test_whitespace_only(self):
        with pytest.raises(ValueError, match="syntax: empty command"):
            parse_command("   ")

    def test_unknown_command_go(self):
        with pytest.raises(ValueError, match="syntax: unknown command 'go'"):
            parse_command("go")

    def test_unknown_command_run(self):
        with pytest.raises(ValueError, match="syntax: unknown command 'run'"):
            parse_command("run")

    def test_unknown_command_gen(self):
        """CSS-1.0 MVP mode — 'gen' not in VALID_COMMANDS"""
        with pytest.raises(ValueError, match="syntax: unknown command 'gen'"):
            parse_command("gen")

    def test_unknown_flag(self):
        with pytest.raises(ValueError, match="syntax:"):
            parse_command("g fast")

    def test_unknown_flag_verbose(self):
        with pytest.raises(ValueError, match="syntax:"):
            parse_command("m verbose")

    def test_single_quotes_invalid(self):
        """CSS-1.0 §3.1 — arguments MUST use double quotes"""
        with pytest.raises(ValueError, match="syntax: invalid quotes"):
            parse_command("g 'bad quotes'")

    def test_unclosed_double_quote(self):
        with pytest.raises(ValueError, match="syntax: invalid quotes"):
            parse_command('g "unclosed')

    def test_error_prefix_is_syntax(self):
        with pytest.raises(ValueError) as exc:
            parse_command("go")
        assert str(exc.value).startswith("syntax:")


# ──────────────────────────────────────────────
# Semantic errors — CSS-1.0 §6.2
# ──────────────────────────────────────────────

class TestSemanticErrors:

    def test_multiple_arguments(self):
        with pytest.raises(ValueError, match="semantic: multiple arguments not allowed"):
            parse_command('g "First idea" "Second idea"')

    def test_multiple_arguments_with_flag(self):
        with pytest.raises(ValueError, match="semantic: multiple arguments not allowed"):
            parse_command('g "First" "Second" dry')

    def test_multiple_arguments_up(self):
        with pytest.raises(ValueError, match="semantic: multiple arguments not allowed"):
            parse_command('up "Idea A" "Idea B"')

    def test_error_prefix_is_semantic(self):
        with pytest.raises(ValueError) as exc:
            parse_command('g "a" "b"')
        assert str(exc.value).startswith("semantic:")


# ──────────────────────────────────────────────
# Command repr
# ──────────────────────────────────────────────

class TestCommandRepr:

    def test_repr_no_args(self):
        cmd = parse_command("g")
        assert "base='g'" in repr(cmd)
        assert "argument=None" in repr(cmd)

    def test_repr_with_argument(self):
        cmd = parse_command('g "Add CLI"')
        assert "argument='Add CLI'" in repr(cmd)
