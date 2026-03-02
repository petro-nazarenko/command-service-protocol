"""
csprotocol.cli
Entry point for the `csp` command-line tool.

Usage:
    csp 'g "Add CLI support"'
    csp 'up dry'
    csp 'm force'
    csp                         # starts interactive REPL
"""

import sys
from csprotocol.main import handle, repl


def main() -> None:
    """
    CLI entry point registered in pyproject.toml:
        [project.scripts]
        csp = "csprotocol.cli:main"
    """
    args = sys.argv[1:]

    # No arguments — start interactive REPL
    if not args:
        repl()
        return

    # Single argument — process as command
    if len(args) == 1:
        result = handle(args[0])
        print(result)
        # Exit with non-zero code on error (for CI/scripting)
        if result.startswith("ERROR:"):
            sys.exit(1)
        return

    # Multiple arguments — join and process
    # Allows: csp g "Add CLI support" (without outer quotes)
    command = " ".join(args)
    result = handle(command)
    print(result)
    if result.startswith("ERROR:"):
        sys.exit(1)


if __name__ == "__main__":
    main()
