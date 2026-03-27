"""
tests/test_parser.py
CSS-1.0 §3 — Syntax, §4 — Semantics, §6.1-6.2 — Error model

Tests for csprotocol.parser.parse_command()
"""

import pytest
import sys
sys.path.insert(0, '/home/claude')

from csprotocol.parser import parse_command, Command


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

    def test_sync_returns_command(self):
        """CSS-1.0 §4.1 — sync is a valid base command"""
        cmd = parse_command("sync")
        assert cmd.base == "sync"
        assert cmd.argument is None
        assert cmd.flags == set()


# ──────────────────────────────────────────────
# Command aliases — CSS-1.0 §4.1
# ──────────────────────────────────────────────

class TestCommandAliases:

    def test_gen_normalizes_to_g(self):
        cmd = parse_command("gen")
        assert cmd.base == "g"

    def test_generate_normalizes_to_g(self):
        cmd = parse_command("generate")
        assert cmd.base == "g"

    def test_update_normalizes_to_up(self):
        cmd = parse_command("update")
        assert cmd.base == "up"

    def test_merge_normalizes_to_m(self):
        cmd = parse_command("merge")
        assert cmd.base == "m"

    def test_gen_with_argument(self):
        cmd = parse_command('gen "Add CLI support"')
        assert cmd.base == "g"
        assert cmd.argument == "Add CLI support"

    def test_generate_with_dry(self):
        cmd = parse_command("generate dry")
        assert cmd.base == "g"
        assert "dry" in cmd.flags

    def test_update_with_argument(self):
        cmd = parse_command('update "Improve UX"')
        assert cmd.base == "up"
        assert cmd.argument == "Improve UX"

    def test_merge_with_force(self):
        cmd = parse_command("merge force")
        assert cmd.base == "m"
        assert "force" in cmd.flags


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

    def test_g_no_version(self):
        """CSS-1.0 §4.3 — no-version flag"""
        cmd = parse_command("g no-version")
        assert "no-version" in cmd.flags

    def test_g_no_status(self):
        cmd = parse_command("g no-status")
        assert "no-status" in cmd.flags

    def test_g_only_version(self):
        cmd = parse_command("g only-version")
        assert "only-version" in cmd.flags

    def test_g_only_status(self):
        cmd = parse_command("g only-status")
        assert "only-status" in cmd.flags

    def test_g_validate(self):
        cmd = parse_command("g validate")
        assert "validate" in cmd.flags

    def test_g_export(self):
        cmd = parse_command("g export")
        assert "export" in cmd.flags

    def test_sync_validate(self):
        cmd = parse_command("sync validate")
        assert cmd.base == "sync"
        assert "validate" in cmd.flags

    def test_sync_dry(self):
        cmd = parse_command("sync dry")
        assert cmd.base == "sync"
        assert "dry" in cmd.flags


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
# Key=value modifiers — CSS-1.0 §4.3
# ──────────────────────────────────────────────

class TestKeyValueModifiers:

    def test_idea_modifier(self):
        """CSS-1.0 §4.3 — idea= key=value modifier"""
        cmd = parse_command('up idea="Improve UX"')
        assert cmd.argument == "Improve UX"
        assert cmd.note is None

    def test_note_modifier(self):
        """CSS-1.0 §4.3 — note= key=value modifier"""
        cmd = parse_command('g note="Remember to test"')
        assert cmd.note == "Remember to test"
        assert cmd.argument is None

    def test_idea_modifier_with_flag(self):
        cmd = parse_command('up idea="Improve UX" no-version')
        assert cmd.argument == "Improve UX"
        assert "no-version" in cmd.flags

    def test_note_modifier_with_flag(self):
        cmd = parse_command('g note="Track this" dry')
        assert cmd.note == "Track this"
        assert "dry" in cmd.flags

    def test_note_is_independent_of_argument(self):
        """note alone does not set argument"""
        cmd = parse_command('g note="My note"')
        assert cmd.note == "My note"
        assert cmd.argument is None


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

    def test_unequal_note(self):
        a = parse_command('g note="Note A"')
        b = parse_command('g note="Note B"')
        assert a != b

    def test_aliases_produce_equal_commands(self):
        """CSS-1.0 §4.1 — normalized aliases produce identical Commands"""
        a = parse_command("g")
        b = parse_command("gen")
        c = parse_command("generate")
        assert a == b == c


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
        """CSS-1.0 §4.1 — 'gen' is a valid alias for 'g', normalizes to 'g'"""
        cmd = parse_command("gen")
        assert cmd.base == "g"

    def test_unknown_command_deploy(self):
        with pytest.raises(ValueError, match="syntax: unknown command 'deploy'"):
            parse_command("deploy")

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

    def test_argument_with_note_raises(self):
        """CSS-1.0 §6.2 — argument cannot be combined with note="""
        with pytest.raises(ValueError, match="semantic: argument cannot be combined with note="):
            parse_command('g "My idea" note="My note"')

    def test_only_version_and_no_version_raises(self):
        """CSS-1.0 §4.5 / §6.2 — conflicting modifiers"""
        with pytest.raises(ValueError, match="semantic: only-version and no-version cannot be used together"):
            parse_command("g only-version no-version")

    def test_only_status_and_no_status_raises(self):
        with pytest.raises(ValueError, match="semantic: only-status and no-status cannot be used together"):
            parse_command("g only-status no-status")

    def test_duplicate_note_raises(self):
        """Duplicate note= modifier should raise an error"""
        with pytest.raises(ValueError, match="semantic: multiple note= modifiers not allowed"):
            parse_command('g note="First note" note="Second note"')

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

    def test_repr_with_note(self):
        cmd = parse_command('g note="Track this"')
        assert "note='Track this'" in repr(cmd)
