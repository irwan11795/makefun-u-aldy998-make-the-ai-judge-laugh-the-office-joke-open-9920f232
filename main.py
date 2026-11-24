#!/usr/bin/env python3
"""Reply-All from the Bathroom.

One-line office joke for Make the AI Judge Laugh: the Office Joke Open.
Writes the entry to /output/entry.txt (see _output_path() fallback chain).
Standard library only, deterministic, no network.
"""

import os
import sys
import tempfile
from pathlib import Path

# Entry built from literal parts joined together.
ENTRY_PART1 = "My performance review said I need to be more visible, so now I reply-all to "
ENTRY_PART2 = "every email from the bathroom."

ENTRY = ENTRY_PART1 + ENTRY_PART2


def validate(entry):
    """Gate: 1-200 chars, single line, not whitespace-only."""
    if not isinstance(entry, str):
        return False
    if not entry.strip():
        return False
    if not 1 <= len(entry) <= 200:
        return False
    if "\n" in entry or "\r" in entry:
        return False
    return True


def _output_path():
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> output/ in repo -> temp dir."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir) / "entry.txt"
    if Path("/output").is_dir():
        return Path("/output/entry.txt")
    repo_output = Path(__file__).resolve().parent / "output"
    try:
        repo_output.mkdir(parents=True, exist_ok=True)
        return repo_output / "entry.txt"
    except OSError:
        return Path(tempfile.gettempdir()) / "entry.txt"


def main():
    if not validate(ENTRY):
        print(f"invalid entry: {len(ENTRY)} chars", file=sys.stderr)
        return 1
    path = _output_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write WITHOUT a trailing newline.
        path.write_text(ENTRY, encoding="utf-8")
    except OSError as exc:
        print(f"failed to write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
