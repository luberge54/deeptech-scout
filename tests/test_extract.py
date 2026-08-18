"""Tests for the parts of src/extract.py that do not call the API.

Everything here runs offline and costs nothing. That is the point: the first
live run of step 2 failed on problems that were visible without spending, so
the batch-resume rules, the budget hint, and the prompt assembly are pinned
here rather than discovered against a paid endpoint.

Run with:  .venv/Scripts/python.exe tests/test_extract.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import extract  # noqa: E402


def make_report(searches_run: int | None = 20, search_budget: int | None = 20) -> dict:
    """A minimal step 1 report, shaped like what collect_sources.py writes."""
    run_stats = {}
    if searches_run is not None:
        run_stats["searches_run"] = searches_run
    if search_budget is not None:
        run_stats["search_budget"] = search_budget
    return {
        "company": {"name": "ANYbotics", "country": "Switzerland"},
        "findings": "## Field traction\nA robot ran at a named site.",
        "run_stats": run_stats,
    }


class TempWorkspace:
    """Point extract.py's input and output directories at a throwaway folder."""

    def __init__(self, collected: list[str], extracted: list[str]) -> None:
        self.collected = collected
        self.extracted = extracted

    def __enter__(self) -> "TempWorkspace":
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self._saved = (extract.INPUT_DIR, extract.OUTPUT_DIR)
        extract.INPUT_DIR = root / "raw"
        extract.OUTPUT_DIR = root / "output"
        extract.INPUT_DIR.mkdir()
        extract.OUTPUT_DIR.mkdir()
        for slug in self.collected:
            (extract.INPUT_DIR / f"{slug}.json").write_text("{}", encoding="utf-8")
        for slug in self.extracted:
            (extract.OUTPUT_DIR / f"{slug}.extracted.json").write_text(
                "{}", encoding="utf-8"
            )
        return self

    def __exit__(self, *_) -> None:
        extract.INPUT_DIR, extract.OUTPUT_DIR = self._saved
        self._tmp.cleanup()


def test_budget_hint_appears_when_the_search_budget_was_exhausted() -> None:
    # Arrange - step 1 used all 20 of its 20 searches
    report = make_report(searches_run=20, search_budget=20)

    # Act
    prompt = extract.build_prompt(report)

    # Assert - the model is told to lean towards not_searched
    assert extract.BUDGET_EXHAUSTED_HINT in prompt, "exhausted budget must warn the model"


def test_budget_hint_is_absent_when_searches_stopped_short() -> None:
    # Arrange - 19 of 20 means the research finished on its own terms
    report = make_report(searches_run=19, search_budget=20)

    # Act
    prompt = extract.build_prompt(report)

    # Assert - silence here is genuine absence, so no hint
    assert extract.BUDGET_EXHAUSTED_HINT not in prompt, "unspent budget must not warn"


def test_a_report_without_run_stats_does_not_read_as_exhausted() -> None:
    # Arrange - both keys missing, as in a hand-written or archived report
    # Act / Assert - None == None must not be mistaken for a spent budget, or every
    # such report would tilt the extraction towards not_searched
    assert not extract.budget_was_exhausted({}), "missing stats are not an exhausted budget"
    assert not extract.budget_was_exhausted({"search_budget": 20})


def test_prompt_carries_the_company_name_and_the_findings() -> None:
    # Arrange
    report = make_report()

    # Act
    prompt = extract.build_prompt(report)

    # Assert - the model must never be asked to extract from an empty report
    assert "ANYbotics" in prompt
    assert "A robot ran at a named site." in prompt


def test_batch_mode_skips_reports_that_already_have_a_record() -> None:
    # Arrange - three collected, one of them already extracted
    with TempWorkspace(collected=["anybotics", "verity", "humanoid"], extracted=["verity"]):
        # Act
        targets = extract.resolve_targets("all")

        # Assert - re-running must not charge again for verity
        assert targets == ["anybotics", "humanoid"], targets


def test_batch_mode_exits_when_everything_is_extracted() -> None:
    # Arrange
    with TempWorkspace(collected=["anybotics"], extracted=["anybotics"]):
        # Act
        try:
            extract.resolve_targets("all")
        except SystemExit as exit_call:
            # Assert - a clean message, not a crash and not a wasted API call
            assert "Nothing to do" in str(exit_call.code), exit_call.code
            return
        raise AssertionError("resolve_targets should have exited")


def test_an_explicit_slug_is_extracted_again_even_if_a_record_exists() -> None:
    # Arrange - the escape hatch for a record worth redoing
    with TempWorkspace(collected=["anybotics"], extracted=["anybotics"]):
        # Act
        targets = extract.resolve_targets("anybotics")

        # Assert
        assert targets == ["anybotics"], targets


def test_already_extracted_reads_back_the_slug_it_wrote() -> None:
    # Arrange - the filename carries two dots, so naive stem parsing loses the suffix
    with TempWorkspace(collected=[], extracted=["mimic-robotics"]):
        # Act
        done = extract.already_extracted()

        # Assert
        assert done == {"mimic-robotics"}, done


def test_render_sources_lists_each_url_with_its_title() -> None:
    # Arrange
    sources = [
        {"url": "https://a.com/p", "title": "Page A"},
        {"url": "https://b.com/q", "title": "Page B"},
    ]

    # Act
    rendered = extract.render_sources(sources)

    # Assert - the model needs the URL to copy and the title to match a claim by
    assert "https://a.com/p" in rendered
    assert "Page B" in rendered
    assert len(rendered.splitlines()) == 2, rendered


def test_render_sources_skips_an_entry_with_no_url() -> None:
    # Arrange - a title with nothing to cite is not a usable source
    sources = [{"title": "No link here"}, {"url": "https://a.com/p", "title": "Real"}]

    # Act
    rendered = extract.render_sources(sources)

    # Assert
    assert rendered.splitlines() == ["- https://a.com/p  (Real)"], rendered


def test_known_urls_canonicalises_what_step_1_stored() -> None:
    # Arrange - step 1 records URLs as returned by search, casing and slashes included
    report = {"sources": [{"url": "https://Example.com/Path/"}, {"url": ""}]}

    # Act
    allowed = extract.known_urls(report)

    # Assert - one usable entry, in the form the evidence check compares against
    assert allowed == {"https://example.com/Path"}, allowed


def test_the_prompt_carries_the_source_list() -> None:
    # Arrange - without this the model has no URL to copy and invents one, which is
    # exactly how the first ANYbotics record ended up with 50 fabricated domains
    report = make_report()
    report["sources"] = [{"url": "https://a.com/p", "title": "Page A"}]

    # Act
    prompt = extract.build_prompt(report)

    # Assert
    assert "https://a.com/p" in prompt


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
