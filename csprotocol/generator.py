"""
csprotocol.generator
CSS-1.0 §5 — Output contract

Transforms a validated Command object into a deterministic Python one-liner.
"""

from csprotocol.parser import Command


def generate_one_liner(cmd: Command) -> str:
    """
    Generate a CSS-1.0 compliant Python one-liner from a Command.

    CSS-1.0 §5.2 — output must be deterministic, single-line, safe to execute.

    Raises:
        ValueError: with message prefixed "semantic: " for unsupported commands.
    """
    if cmd.base in ("g", "up"):
        return _build_run_one_liner(
            update_version=(cmd.base == "g"),
            idea=cmd.argument,
            note=cmd.note,
            flags=cmd.flags,
        )

    if cmd.base == "m":
        return _build_merge_one_liner(
            force=("force" in cmd.flags),
            dry=("dry" in cmd.flags),
        )

    if cmd.base == "sync":
        return _build_sync_one_liner(flags=cmd.flags)

    raise ValueError(f"semantic: unsupported command {cmd.base!r}")


def _escape_str(value: str) -> str:
    """CSS-1.0 §5.2 — safe single-quote escaping for shell execution"""
    return value.replace("'", "\\'")


def _build_run_one_liner(
    update_version: bool,
    idea: str | None,
    note: str | None,
    flags: set[str],
) -> str:
    """Build one-liner for updater.run()"""
    dry = "dry" in flags

    if idea is None:
        idea_arg = "None"
    else:
        idea_arg = f"'{_escape_str(idea)}'"

    parts = [
        f"update_version={update_version}",
        f"idea={idea_arg}",
        f"dry={dry}",
    ]

    if note is not None:
        parts.append(f"note='{_escape_str(note)}'")
    if "no-version" in flags:
        parts.append("no_version=True")
    if "no-status" in flags:
        parts.append("no_status=True")
    if "only-version" in flags:
        parts.append("only_version=True")
    if "only-status" in flags:
        parts.append("only_status=True")
    if "validate" in flags:
        parts.append("validate=True")
    if "export" in flags:
        parts.append("export=True")

    args = ", ".join(parts)
    return f'python3 -c "import updater; updater.run({args})"'


def _build_merge_one_liner(force: bool, dry: bool) -> str:
    """Build one-liner for updater.merge()"""
    return (
        f'python3 -c "import updater; '
        f'updater.merge('
        f'force={force}, '
        f'dry={dry})"'
    )


def _build_sync_one_liner(flags: set[str]) -> str:
    """Build one-liner for updater.sync() — CSS-1.0 §4.6.4"""
    dry = "dry" in flags
    parts = [f"dry={dry}"]
    if "validate" in flags:
        parts.append("validate=True")
    if "export" in flags:
        parts.append("export=True")
    if "force" in flags:
        parts.append("force=True")
    args = ", ".join(parts)
    return f'python3 -c "import updater; updater.sync({args})"'
