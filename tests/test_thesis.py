"""Tests for the offline parts of src/thesis.py.

Both guards tested here exist because of real failures in the first two thesis
runs. The first satisfied a required field with the literal string "placeholder"
and the document was written around it. The second wrote every section properly
but double-escaped its em-dashes, so the finished file carried the six characters
of an escape sequence 39 times instead of the dash.

Neither is something the structured-output contract can catch: both are valid
strings. They are caught here, and both are cheap to check.

Run with:  .venv/Scripts/python.exe tests/test_thesis.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import thesis  # noqa: E402

REAL_PROSE = (
    "This ranking reads only public sources, so it favours companies that "
    "publicise well over companies that deploy well. Five companies is a test of "
    "the method rather than a survey of the sector, and each was researched in a "
    "single search pass whose budget ran out on four of the five."
)

# The escape sequence as six literal characters, built rather than typed so the
# test file itself cannot be the thing that decodes it.
ESCAPED_DASH = chr(92) + "u2014"
EM_DASH = chr(8212)


def make_thesis(**overrides) -> thesis.Thesis:
    """A complete thesis, with real prose in every section unless overridden."""
    fields = {name: REAL_PROSE for name in thesis.Thesis.model_fields}
    fields.update(overrides)
    return thesis.Thesis(**fields)


def test_a_complete_thesis_reports_no_empty_section() -> None:
    # Arrange / Act / Assert
    assert thesis.find_empty_sections(make_thesis()) == []


def test_the_literal_placeholder_that_shipped_is_caught() -> None:
    # Arrange - exactly what the first run returned
    written = make_thesis(where_this_method_is_weakest="placeholder")

    # Act
    empty = thesis.find_empty_sections(written)

    # Assert
    assert empty == ["where_this_method_is_weakest"], empty


def test_other_stand_ins_are_caught_too() -> None:
    # Arrange - the handful of strings a model reaches for when meaning to return
    for stand_in in ["TBD", "todo", "N/A", "...", "  None  "]:
        written = make_thesis(the_thesis=stand_in)

        # Act / Assert
        assert "the_thesis" in thesis.find_empty_sections(written), stand_in


def test_a_section_too_short_to_be_content_is_caught() -> None:
    # Arrange - a heading rather than a section, long enough to dodge a word list
    written = make_thesis(what_would_falsify_it="Several things could falsify this.")

    # Act / Assert
    assert "what_would_falsify_it" in thesis.find_empty_sections(written)


def test_a_section_mentioning_a_stand_in_word_is_not_caught() -> None:
    # Arrange - the check must not fire on prose that happens to use the word, or
    # it would reject good work
    written = make_thesis(
        where_this_method_is_weakest=(
            "Several figures in the sources are placeholders rather than audited "
            "numbers, and the ranking cannot tell one from the other. " + REAL_PROSE
        )
    )

    # Act / Assert
    assert thesis.find_empty_sections(written) == []


def test_a_double_escaped_character_is_decoded() -> None:
    # Arrange - what the second run produced 39 times: an em-dash written into the
    # JSON as its escape sequence rather than as the character itself
    text = f"Four are Swiss {ESCAPED_DASH} one British."

    # Act
    decoded = thesis.decode_escaped_characters(text)

    # Assert - the finished document must carry the dash, not six literal characters
    assert decoded == f"Four are Swiss {EM_DASH} one British."
    assert ESCAPED_DASH not in decoded


def test_ordinary_prose_is_left_exactly_as_written() -> None:
    # Arrange - the repair must not touch text that never needed it
    text = f"A sentence with a real em-dash {EM_DASH} and a Windows path C:/x/y."

    # Act / Assert
    assert thesis.decode_escaped_characters(text) == text


def test_cleaning_repairs_every_section_of_a_thesis() -> None:
    # Arrange
    written = make_thesis(
        the_thesis=(
            f"Value accrues to narrow machines {ESCAPED_DASH} not to platforms. "
            + REAL_PROSE
        )
    )

    # Act
    cleaned = thesis.clean(written)

    # Assert
    assert ESCAPED_DASH not in cleaned.the_thesis
    assert EM_DASH in cleaned.the_thesis


def test_the_written_thesis_carries_no_escape_sequences() -> None:
    # Arrange - the document on disk is the deliverable, so check the real thing
    if not thesis.OUTPUT_PATH.exists():
        print("       (skipped: no thesis document on disk)")
        return

    # Act
    document = thesis.OUTPUT_PATH.read_text(encoding="utf-8")

    # Assert
    assert ESCAPED_DASH not in document
    assert chr(92) + "u" not in document, "an escape sequence survived into the document"


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    failures = 0

    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as error:
            failures += 1
            print(f"  FAIL  {test.__name__}: {error}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
