"""Verify the initial local entry point."""

from pytest import CaptureFixture

from career_autopilot.main import main


def test_main_prints_local_banner(capsys: CaptureFixture[str]) -> None:
    main()
    assert capsys.readouterr().out == "CareerAutopilot: local foundation ready\n"
