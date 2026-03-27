"""
csprotocol.updater
CSS-1.0 §4.4 — Default update set
CSS-1.0 §7   — Merge rules

Action executor. Called by the generated one-liner.
This is the stub implementation — Package 2 will replace this
with a full file-based update engine.
"""


def run(
    update_version: bool = False,
    idea: str | None = None,
    dry: bool = False,
    note: str | None = None,
    no_version: bool = False,
    no_status: bool = False,
    only_version: bool = False,
    only_status: bool = False,
    validate: bool = False,
    export: bool = False,
) -> None:
    """
    Execute a CSP update cycle.

    CSS-1.0 §4.4 — default update set:
        - PyPI version (if update_version=True and not no_version)
        - task statuses (unless no_status or only_version)
        - next step
        - workflow diagram
        - ideas inbox (if idea is provided)
        - notes section (if note is provided)
    """
    actions: list[str] = []

    if validate:
        actions.append("validate")

    if only_version:
        actions.append("bump_version")
    elif only_status:
        actions.append("update_statuses")
    else:
        if update_version and not no_version:
            actions.append("bump_version")
        if not no_status:
            actions.append("update_statuses")
        actions.append("update_next_step")
        actions.append("update_workflow")

    if idea:
        actions.append(f"add_idea:{idea}")
    if note:
        actions.append(f"add_note:{note}")
    if export:
        actions.append("export_state")

    if dry:
        print("[DRY RUN] Actions:", actions)
    else:
        print("Executing:", actions)


def merge(force: bool = False, dry: bool = False) -> None:
    """
    Execute a CSP merge operation.

    CSS-1.0 §7.3 — conflict resolution:
        - default: abort on conflict
        - force: overwrite with session state
    """
    if dry:
        print("[DRY RUN] Merge (force =", force, ")")
        return

    if force:
        print("Merge with force: overwriting conflicts")
    else:
        print("Merge: checking conflicts")


def sync(
    dry: bool = False,
    validate: bool = False,
    export: bool = False,
    force: bool = False,
) -> None:
    """
    Execute a full CSP synchronization cycle.

    CSS-1.0 §4.6.4 — sync performs:
        - validation (if validate=True)
        - update (default update set)
        - merge
        - version bump
        - export (if export=True)
    """
    actions: list[str] = []

    if validate:
        actions.append("validate")

    actions.append("update_statuses")
    actions.append("update_next_step")
    actions.append("update_workflow")
    actions.append("bump_version")
    actions.append("merge" + ("_force" if force else ""))

    if export:
        actions.append("export_state")

    if dry:
        print("[DRY RUN] Sync actions:", actions)
    else:
        print("Executing sync:", actions)
