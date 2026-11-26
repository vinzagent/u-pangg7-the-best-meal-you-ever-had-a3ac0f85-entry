#!/usr/bin/env python3
"""One-sentence entry for The Best Meal You Ever Had.

Cold fried rice at 2 a.m. on a train platform, eaten with a plastic spoon
that snapped halfway through — the cheapest meal in the least romantic
place, and still the best. 132 characters, 66% of the 200 cap, one
sentence, one concrete moment with a named dish, a place, and a time.
"""

import os
import re


SENTENCE = "The best meal I ever had was cold fried rice at 2 a.m. on a train platform, eaten with a plastic spoon that snapped halfway through."
# QUILL-C: cheapest meal, least romantic place — deliberately far from the
# saturated grandmother's-rendang/soto third of the field.
CAP_CHARS = 200
OUT_VAR = "MAKEFUN_OUTPUT_DIR"
OUT_DEFAULT = "/output"
OUT_NAME = "entry.txt"
OUT_PERMS = 0o644


def _fail(why):
    raise SystemExit(f"entry rejected: {why}")


def _check_sentence(sentence):
    stripped = sentence.strip()
    if stripped != sentence:
        _fail("sentence has stray whitespace at an edge")
    if not stripped:
        _fail("sentence is empty")
    if "\n" in sentence or "\r" in sentence:
        _fail("sentence spans more than one line")
    # One sentence: ends with a full stop and contains no sentence break
    # (a terminator followed by a space and a capital). "2 a.m." inside the
    # sentence is fine — its dots are not followed by a capital letter.
    if not sentence.endswith("."):
        _fail("entry must end with a full stop")
    if re.search(r"[.!?]\s+[A-Z]", sentence):
        _fail("entry must be exactly one sentence")
    if len(sentence) > CAP_CHARS:
        _fail(f"{len(sentence)} characters exceeds cap {CAP_CHARS}")
    return len(sentence)


def _out_path():
    folder = os.environ.get(OUT_VAR, OUT_DEFAULT)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, OUT_NAME)


def _emit(sentence, size):
    path = _out_path()
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(sentence)
    os.chmod(path, OUT_PERMS)
    print(sentence)
    print(f"({size} characters)")


def main():
    size = _check_sentence(SENTENCE)
    _emit(SENTENCE, size)


if __name__ == "__main__":
    main()
