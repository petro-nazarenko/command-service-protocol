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
) -> None:
    """
    Execute a CSP update cycle.

    CSS-1.0 §4.4 — default update set:
        - PyPI version (if update_version=True)
        - task statuses
        - next step
        - workflow diagram
        - ideas inbox (if idea is provided)
    """
    actions: list[str] = []

    if update_version:
        actions.append("bump_version")

    actions.append("update_statuses")
    actions.append("update_next_step")
    actions.append("update_workflow")

    if idea:
        actions.append(f"add_idea:{idea}")

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
