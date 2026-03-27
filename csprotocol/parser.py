"""
csprotocol.parser
CSS-1.0 §3 — Syntax, §4 — Semantics (parse phase)
"""

import shlex

# CSS-1.0 §4.1 — canonical command names
CANONICAL_COMMANDS: set[str] = {"g", "up", "m", "sync"}

# CSS-1.0 §4.1 — alias → canonical mapping
COMMAND_ALIASES: dict[str, str] = {
    "gen": "g",
    "generate": "g",
    "update": "up",
    "merge": "m",
}

# All accepted input commands (canonical + aliases)
VALID_COMMANDS: set[str] = CANONICAL_COMMANDS | set(COMMAND_ALIASES.keys())

# CSS-1.0 §4.3 — all valid flags
VALID_FLAGS: set[str] = {
    "force",
    "dry",
    "no-version",
    "no-status",
    "only-version",
    "only-status",
    "validate",
    "export",
}

# CSS-1.0 §4.3 — key=value modifier keys
VALID_KV_KEYS: set[str] = {"idea", "note"}


class Command:
    def __init__(
        self,
        base: str,
        argument: str | None = None,
        flags: set[str] | None = None,
        note: str | None = None,
    ) -> None:
        self.base = base
        self.argument = argument
        self.flags = flags or set()
        self.note = note

    def __repr__(self) -> str:
        return (
            f"Command(base={self.base!r}, argument={self.argument!r}, "
            f"flags={self.flags!r}, note={self.note!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Command):
            return NotImplemented
        return (
            self.base == other.base
            and self.argument == other.argument
            and self.flags == other.flags
            and self.note == other.note
        )


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

    # CSS-1.0 §4.1 — normalize alias to canonical form
    base = COMMAND_ALIASES.get(base, base)

    # Determine which tokens were quoted in the original text
    # by re-examining the source: quoted tokens start with a double-quote char
    # We reconstruct by scanning the original text
    quoted_values = set()
    import re
    for m in re.finditer(r'"([^"]*)"', text):
        quoted_values.add(m.group(1))

    argument: str | None = None
    note: str | None = None
    flags: set[str] = set()

    for token in raw_tokens[1:]:
        if token in VALID_FLAGS:
            flags.add(token)
        elif "=" in token:
            # CSS-1.0 §4.3 — key=value modifier
            key, _, val = token.partition("=")
            if key not in VALID_KV_KEYS:
                raise ValueError(f"syntax: unknown flag {token!r}")
            if key == "idea":
                if argument is not None:
                    raise ValueError("semantic: multiple arguments not allowed")
                argument = val
            else:  # key == "note"
                if note is not None:
                    raise ValueError("semantic: multiple note= modifiers not allowed")
                note = val
        elif token in quoted_values:
            # CSS-1.0 §4.2 — quoted string is argument (idea=)
            if argument is not None:
                raise ValueError("semantic: multiple arguments not allowed")
            argument = token
        else:
            # Bare unquoted non-flag token — CSS-1.0 §6.1 unknown flag
            raise ValueError(f"syntax: unknown flag {token!r}")

    # CSS-1.0 §6.2 — semantic conflict: argument cannot be combined with note=
    if argument is not None and note is not None:
        raise ValueError("semantic: argument cannot be combined with note=")

    # CSS-1.0 §4.5 — conflicting modifier pairs
    if "only-version" in flags and "no-version" in flags:
        raise ValueError("semantic: only-version and no-version cannot be used together")
    if "only-status" in flags and "no-status" in flags:
        raise ValueError("semantic: only-status and no-status cannot be used together")

    return Command(base=base, argument=argument, flags=flags, note=note)
