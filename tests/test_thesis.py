"""Tests for the offline parts of src/thesis.py.

The guard tested here exists because of a real failure: the first thesis run
returned the literal string "placeholder" for its last section, and the document
was written anyway. A required field can be satisfied by one word, so the
structured-output contract cannot catch this on its own.

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
