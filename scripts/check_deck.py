#!/usr/bin/env python3
"""Perform lightweight structural checks for a standalone HTML deck."""

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_deck.py path/to/deck.html", file=sys.stderr)
        return 2

    deck = Path(sys.argv[1])
    if not deck.is_file():
        print(f"Missing HTML file: {deck}", file=sys.stderr)
        return 2

    content = deck.read_text(encoding="utf-8", errors="replace").lstrip()
    required = {
        "doctype": "<!doctype html",
        "title": "<title",
        "document end": "</html>",
    }
    failures = [name for name, marker in required.items() if marker not in content.lower()]
    slide_count = content.lower().count("<section")

    if failures:
        print("Failed: " + ", ".join(failures), file=sys.stderr)
        return 1
    if slide_count < 2:
        print("Warning: found fewer than two <section> elements; confirm this is a deck.")
    else:
        print(f"OK: structural checks passed ({slide_count} sections found).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
