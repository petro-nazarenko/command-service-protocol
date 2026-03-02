"""
csprotocol.parser
CSS-1.0 §3 — Syntax, §4 — Semantics (parse phase)
"""

import shlex

VALID_COMMANDS: set[str] = {"g", "up", "m"}
VALID_FLAGS: set[str] = {"force", "dry"}


class Command:
    def __init__(self, base: str, argument: str | None = None, flags: set[str] | None = None) -> None:
        self.base = base
        self.argument = argument
        self.flags = flags or set()

    def __repr__(self) -> str:
        return f"Command(base={self.base!r}, argument={self.argument!r}, flags={self.flags!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Command):
            return NotImplemented
        return self.base == other.base and self.argument == other.argument and self.flags == other.flags


def _check_single_quotes(text: str) -> None:
    """CSS-1.0 §3.1 — arguments MUST use double quotes."""
    in_double = False
    for ch in text:
        if ch == chr(34):
            in_double = not in_double
        elif ch == chr(39) and not in_double:
            raise ValueError("syntax: invalid quotes")


def _tokenize(text: str) -> list[tuple[str, bool]]:
    """
    Tokenize text, returning (token, was_quoted) pairs.
    was_quoted=True means the token came from a double-quoted string.
    """
    lex = shlex.shlex(text, posix=True)
    lex.whitespace_split = False
    lex.whitespace = " "
    lex.quotes = chr(34)
    lex.commenters = ""
    tokens = []
    try:
        while True:
            token = lex.get_token()
            if token is shlex.EOF:
                break
            was_quoted = lex.token != token or (lex.state is None)
            tokens.append((token, lex.token == chr(34) or False))
    except ValueError:
        raise ValueError("syntax: invalid quotes")
    return tokens


def parse_command(text: str) -> Command:
    """
    Parse a raw CSP command string into a Command object.
    CSS-1.0 §3.4, §6.1, §6.2
    """
    _check_single_quotes(text)

    try:
        raw_tokens = shlex.split(text)
    except ValueError:
        raise ValueError("syntax: invalid quotes")

    if not raw_tokens:
        raise ValueError("syntax: empty command, expected base command (g | up | m)")

    base = raw_tokens[0]
    if base not in VALID_COMMANDS:
        raise ValueError(f"syntax: unknown command {base!r}")

    # Determine which tokens were quoted in the original text
    # by re-examining the source: quoted tokens start with a double-quote char
    # We reconstruct by scanning the original text
    quoted_values = set()
    import re
    for m in re.finditer(r'"([^"]*)"', text):
        quoted_values.add(m.group(1))

    argument: str | None = None
    flags: set[str] = set()

    for token in raw_tokens[1:]:
        if token in VALID_FLAGS:
            flags.add(token)
        elif token in quoted_values:
            # CSS-1.0 §4.2 — quoted string is argument (idea=)
            if argument is None:
                argument = token
            else:
                raise ValueError("semantic: multiple arguments not allowed")
        else:
            # Bare unquoted non-flag token — CSS-1.0 §6.1 unknown flag
            raise ValueError(f"syntax: unknown flag {token!r}")

    return Command(base=base, argument=argument, flags=flags)
