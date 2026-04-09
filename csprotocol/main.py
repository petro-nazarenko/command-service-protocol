"""
csprotocol.main
Core handle() function and interactive REPL.

CSS-1.0 §8 — FSM: Idle → Parsed → Validated → Generated → Executed
"""

from csprotocol.generator import generate_one_liner
from csprotocol.parser import parse_command


def handle(text: str) -> str:
    """
    Process a raw CSP command string.

    Returns a Python one-liner string on success,
    or an ERROR: prefixed string on failure.

    CSS-1.0 §5   — output contract
    CSS-1.0 §6   — error model
    CSS-1.0 §8   — FSM
    """
    try:
        # FSM: Idle → Parsed
        cmd = parse_command(text)
        # FSM: Parsed → Validated → Generated
        return generate_one_liner(cmd)
    except ValueError as e:
        # FSM: → Error
        return f"ERROR: {e}"


def repl() -> None:
    """
    Interactive REPL loop.
    Reads CSP commands from stdin, prints one-liners or errors.
    """
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not line:
            print("ERROR: syntax: empty command, expected base command (g | up | m)")
            continue

        print(handle(line))


if __name__ == "__main__":
    repl()
