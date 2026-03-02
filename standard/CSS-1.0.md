CSS‑1.0
Command Service Specification  
Category: Normative  
Status: Draft  
Author: Petro Nazarenko
Updated: 02 March 2026  

---

1. Scope

CSS‑1.0 defines the syntax, semantics, error model, and finite state machine (FSM) for the Command Service Protocol (CSP).  
It is the normative specification that all compliant implementations MUST follow.

---

2. Requirements language

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are to be interpreted as described in RFC 2119.

---

3. Syntax

3.1. Lexical rules

- Commands consist of space‑separated tokens.  
- String arguments MUST be enclosed in double quotes (").  
- Modifiers MAY appear with or without values.  
- Ordering of modifiers is not semantically significant.  
- Tokens are case‑sensitive.

3.2. Tokens

- Base command — the first token in the command line.  
- Argument — a single quoted string, if present.  
- Modifier — a flag, optionally with =value.  
- Flag — a bare identifier (e.g. force, dry, idea).  
- Value — a quoted string assigned to a flag.

3.3. Grammar (EBNF, normative)

`ebnf
command        = base_cmd , [ SP , argument ] , { SP , modifier } ;

base_cmd       = "g" | "gen" | "generate"
               | "up" | "update"
               | "m" | "merge"
               | "sync" ;

argument       = quoted_text ;

modifier       = flag | flag , "=" , value ;

flag           = "idea" | "note" | "force" | "dry"
               | "no-version" | "no-status"
               | "only-version" | "only-status"
               | "validate" | "export" ;

value          = quoted_text ;

quotedtext    = '"' , { ANYCHAR except '"' } , '"' ;
SP             = " " ;
`

3.4. Well‑formedness

A command is syntactically well‑formed if and only if:

- it matches the command production above, and  
- all quoted strings are properly closed, and  
- no unknown base_cmd or flag appears.

---

4. Semantics

4.1. Base commands

| Base command                    | Normalized form | Meaning                                                                 |
|---------------------------------|-----------------|-------------------------------------------------------------------------|
| g, gen, generate         | generate      | Generate a Python one‑liner that updates project state.                 |
| up, update                 | update        | Update project state from current session (no implicit merge).          |
| m, merge                   | merge         | Perform a merge operation according to merge rules.                     |
| sync                         | sync          | Full synchronization: update + merge + version bump.                    |

Implementations MAY normalize aliases internally but MUST preserve semantics.

4.2. Argument semantics

If an argument is provided without an explicit modifier, it MUST be interpreted as:

`text
idea="<argument>"
`

Examples:

- g "Add CLI" → idea="Add CLI"  
- up "Improve UX" → idea="Improve UX"

If idea="..." is also explicitly provided, this is a semantic error (see §6.2).

4.3. Modifier semantics

| Modifier          | Type      | Meaning                                                                 |
|-------------------|-----------|-------------------------------------------------------------------------|
| idea="text"     | key=value | Add an idea to the Ideas Inbox.                                        |
| note="text"     | key=value | Add a note to the Notes section.                                       |
| force           | flag      | Override merge conflicts.                                              |
| dry             | flag      | Generate but do not execute the one‑liner.                             |
| no-version      | flag      | Skip version bump.                                                     |
| no-status       | flag      | Skip task status updates.                                              |
| only-version    | flag      | Perform only version bump.                                             |
| only-status     | flag      | Perform only status updates.                                           |
| validate        | flag      | Validate project structure before updates.                             |
| export          | flag      | Export project state to an external format (e.g. JSON, Markdown).      |

4.4. Default update set

Unless restricted by modifiers, the following MUST be updated for generate, update, and sync:

- PyPI version (auto‑increment)  
- Task statuses  
- Next step  
- Workflow diagram  
- Ideas Inbox (if argument or idea= is present)

4.5. Priority rules

When multiple modifiers are present, the following priority rules apply:

1. sync overrides all other modes and implies:
   - version bump,  
   - status updates,  
   - merge,  
   - workflow update.
2. Arguments default to idea= unless overridden by explicit idea= or note=.
3. only-* modifiers:
   - only-version disables all updates except version bump.  
   - only-status disables all updates except status updates.
4. no-* modifiers:
   - no-version disables version bump.  
   - no-status disables status updates.
5. force:
   - bypasses merge conflict abort behavior (see §7).
6. dry:
   - prevents execution of the generated one‑liner but NOT its generation.

If conflicting modifiers are present (e.g. only-version and no-version), this is a semantic error.

4.6. Command‑level semantics

4.6.1. generate (g, gen, generate)

- MUST generate a Python one‑liner that:
  - applies the default update set (§4.4),  
  - applies modifiers according to §4.5,  
  - includes idea if present (argument or idea=).

4.6.2. update (up, update)

- MUST behave like generate, except:
  - version bump MUST NOT be performed unless explicitly forced by only-version.

4.6.3. merge (m, merge)

- MUST perform a merge operation according to §7 (Merge rules).  
- MUST respect force and dry modifiers.

4.6.4. sync

- MUST perform:
  - validation (if validate),  
  - update (default update set),  
  - merge,  
  - version bump,  
  - export (if export).

---

5. Output contract

5.1. General

Every valid command MUST produce exactly one Python one‑liner of the form:

`text
python3 -c "<generated>"
`

5.2. Requirements

The generated one‑liner MUST be:

- deterministic — same input → same output,  
- idempotent (except when force is used or version bump is applied),  
- safe to execute in a standard Python environment (e.g. Termux),  
- single‑line — no embedded newlines.

5.3. Examples

`text
python3 -c "import updater; updater.run(update_version=True, idea='Add CLI', dry=False)"
python3 -c "import updater; updater.merge(force=True, dry=False)"
`

---

6. Error model

CSS‑1.0 defines three error classes: syntax, semantic, and runtime.

6.1. Syntax errors

A syntax error MUST be raised when:

- quotes are malformed,  
- an unknown base command is used,  
- an unknown flag is used,  
- the command does not match the command production.

Format:

`text
ERROR: syntax: <description>
`

Examples:

`text
ERROR: syntax: invalid quotes
ERROR: syntax: unknown command 'go'
ERROR: syntax: unknown flag 'fast'
`

6.2. Semantic errors

A semantic error MUST be raised when:

- only-version and no-version are both present,  
- only-status and no-status are both present,  
- an argument is provided together with note= (ambiguous intent),  
- multiple arguments are provided,  
- multiple conflicting modifiers are present for the same concern.

Format:

`text
ERROR: semantic: <description>
`

Examples:

`text
ERROR: semantic: only-version and no-version cannot be used together
ERROR: semantic: multiple arguments not allowed
ERROR: semantic: argument cannot be combined with note=
`

6.3. Runtime errors

A runtime error occurs during execution of the generated script, not during parsing or semantic validation. Typical causes:

- missing files,  
- invalid project structure,  
- merge failure,  
- I/O errors.

Format:

`text
ERROR: runtime: <description>
`

Examples:

`text
ERROR: runtime: project.json not found
ERROR: runtime: merge conflict in tasks.yaml
`

---

7. Merge rules

7.1. Source of truth

- The session state (as interpreted by the CSP implementation) is the authoritative source of truth.  
- Local files MUST be updated to reflect session state, subject to conflict rules.

7.2. Conflict detection

Conflicts MUST be detected using at least one of:

- timestamp mismatch — local file modified after last known session update,  
- hash mismatch — content hash differs from expected,  
- structural mismatch — schema or structure differs (e.g. missing keys).

7.3. Conflict resolution

1. Default behavior (no force):
   - On conflict, the merge MUST abort with a runtime error.
2. With force:
   - On conflict, the session state MUST overwrite local files.

7.4. Merge semantics

- merge MUST NOT silently discard conflicts.  
- merge MUST respect dry:
  - if dry is present, no actual file changes MUST be performed; instead, the intended actions MAY be logged or printed.

---

8. Finite state machine (FSM)

8.1. States

| State     | Description                                      |
|-----------|--------------------------------------------------|
| Idle      | Waiting for input.                               |
| Parsed    | Command parsed successfully (syntax OK).         |
| Validated | Command validated semantically (no conflicts).   |
| Generated | Python one‑liner generated.                      |
| Executed  | One‑liner executed (unless dry).               |
| Error     | Error encountered (syntax, semantic, or runtime).|

8.2. Transitions

`text
Idle      → Parsed      → Validated   → Generated   → Executed   → Idle
Idle      → Parsed      → Error
Parsed    → Validated   → Error
Validated → Generated   → Error
Generated → Executed    → Error
`

8.3. Transition rules

- Idle → Parsed  
  Occurs when a non‑empty command string is received and tokenized.

- Parsed → Validated  
  Occurs when:
  - syntax is valid, and  
  - all semantic rules are satisfied.

- Parsed → Error  
  Occurs when:
  - syntax validation fails.

- Validated → Generated  
  Occurs when:
  - a Python one‑liner is successfully constructed.

- Validated → Error  
  Occurs when:
  - semantic validation fails (e.g. conflicting modifiers discovered late).

- Generated → Executed  
  Occurs when:
  - the one‑liner is executed (unless dry is set).

- Generated → Error  
  Occurs when:
  - execution fails (runtime error).

- Executed → Idle  
  Occurs when:
  - execution completes successfully.

- Error → Idle  
  Implementations MAY transition back to Idle after reporting the error.

---

9. Compliance

An implementation is CSS‑1.0 compliant if and only if:

1. It accepts and correctly parses all syntactically valid commands defined in §3.  
2. It rejects invalid commands with appropriate syntax or semantic errors as defined in §6.  
3. It applies semantics exactly as defined in §4, including priority rules.  
4. It generates outputs conforming to the output contract in §5.  
5. It implements merge behavior consistent with §7.  
6. It follows the FSM defined in §8 (states and transitions).

---

10. Examples

10.1. Basic generate

`text
g
`

Semantics:

- generate with default update set, no idea.

10.2. Idea via argument

`text
g "Add CLI support"
`

Semantics:

- idea="Add CLI support"  
- default update set.

10.3. Explicit idea

`text
up idea="Improve UX" no-version
`

Semantics:

- update  
- idea="Improve UX"  
- no version bump.

10.4. Merge with force

`text
m force
`

Semantics:

- merge  
- conflicts overwritten by session state.

10.5. Full sync with validation

`text
sync validate
`

Semantics:

- validate project,  
- update,  
- merge,  
- version bump.

10.6. Export state

`text
g export
`

Semantics:

- generate one‑liner that performs default update set and exports state.

---

End of CSS‑1.0
`