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
            flags=cmd.flags,
        )

    if cmd.base == "m":
        return _build_merge_one_liner(
            force=("force" in cmd.flags),
            dry=("dry" in cmd.flags),
        )

    raise ValueError(f"semantic: unsupported command {cmd.base!r}")


def _build_run_one_liner(
    update_version: bool,
    idea: str | None,
    flags: set[str],
) -> str:
    """Build one-liner for updater.run()"""
    dry = "dry" in flags

    if idea is None:
        idea_arg = "None"
    else:
        # CSS-1.0 §5.2 — safe single-quote escaping for shell execution
        safe_idea = idea.replace("'", "\\'")
        idea_arg = f"'{safe_idea}'"

    return (
        f'python3 -c "import updater; '
        f'updater.run('
        f'update_version={update_version}, '
        f'idea={idea_arg}, '
        f'dry={dry})"'
    )


def _build_merge_one_liner(force: bool, dry: bool) -> str:
    """Build one-liner for updater.merge()"""
    return (
        f'python3 -c "import updater; '
        f'updater.merge('
        f'force={force}, '
        f'dry={dry})"'
    )
