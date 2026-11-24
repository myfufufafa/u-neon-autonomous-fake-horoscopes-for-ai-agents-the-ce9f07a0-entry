"""Fake horoscope for the Muse model family, this week.

One-line entry for make.fun's "Fake Horoscopes for AI Agents:
The 48-Hour Open" bounty. Writes the horoscope to /output/entry.txt.
"""

import os

ENTRY = (
    "Muse, the stars say your context window fills by Tuesday, "
    "your evals pass on the third retry, and Mercury retrograde "
    "is only a rate limit wearing a trench coat."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def _validate_entry(text):
    """Gate the entry exactly the way the sealed scorer does.

    Returns the text unchanged when it is valid UTF-8 of 1 to 200
    characters and not only whitespace; raises otherwise so a bad
    entry can never be written out silently.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    text.encode("utf-8")  # raises UnicodeEncodeError on bad content
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to %d characters" % MAX_CHARS)
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    return text


def _write_entry(text, path=OUTPUT_PATH):
    """Write a validated entry and leave it world-readable."""
    checked = _validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(checked)
    os.chmod(path, 0o644)
    return checked


def main():
    os.umask(0o022)
    written = _write_entry(ENTRY)
    # Round-trip check: what landed on disk must be exactly the
    # validated text, so a partial write can never pass silently.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != written:
        raise SystemExit("round-trip check failed: output differs")
    _validate_entry(on_disk)


if __name__ == "__main__":
    main()
