"""Tests for Markdown and PDF export."""

from pathlib import Path

import pytest

from nurse_report.models import Patient, ShiftReport, Task, VitalNote
from nurse_report.export import to_markdown, to_pdf


@pytest.fixture
def sample_report() -> ShiftReport:
    return ShiftReport(
        patient=Patient(
            name="Ada L.",
            mrn="MRN-1",
            room="4B",
            age=34,
            allergies=["penicillin"],
            code_status="Full",
            primary_dx="Pneumonia",
        ),
        shift="Day",
        date="2026-11-01",
        nurse="Dylan",
        summary="Stable overnight.",
        tasks=[Task(description="Check IV", due="09:00", category="Meds", done=True)],
        vitals=[VitalNote(time="08:00", bp="120/80", hr="72", rr="16", temp="98.6", spo2="98", pain="2", notes="Fine")],
    )


def test_markdown_contains_key_fields(sample_report: ShiftReport):
    md = to_markdown(sample_report)
    for text in ["Ada L.", "MRN-1", "4B", "34", "Day", "2026-11-01", "Dylan", "Stable overnight", "Check IV", "120/80"]:
        assert text in md


def test_markdown_empty_report():
    md = to_markdown(ShiftReport())
    assert "# Shift Report Sheet" in md
    assert "—" in md


def test_pdf_writes_file(tmp_path: Path, sample_report: ShiftReport):
    out = tmp_path / "report.pdf"
    to_pdf(sample_report, out)
    assert out.exists()
    assert out.stat().st_size > 0
