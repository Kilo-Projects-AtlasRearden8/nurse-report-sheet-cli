"""Tests for nurse_report models."""

import pytest

from nurse_report.models import Patient, ShiftReport, Task, VitalNote


def test_patient_defaults():
    patient = Patient()
    assert patient.name == ""
    assert patient.allergies == []
    assert patient.age is None


def test_patient_allergies_list():
    patient = Patient(name="Ada L.", allergies=["penicillin", "peanuts"])
    assert patient.allergies == ["penicillin", "peanuts"]


def test_vital_note_defaults():
    vital = VitalNote()
    assert vital.time != ""
    assert vital.bp == ""


def test_task_defaults():
    task = Task(description="Check IV")
    assert task.description == "Check IV"
    assert task.done is False
    assert task.due == ""


def test_shift_report_defaults():
    report = ShiftReport()
    assert report.date != ""
    assert report.created_at != ""
    assert report.updated_at != ""
    assert report.tasks == []
    assert report.vitals == []


def test_touch_updates_updated_at():
    report = ShiftReport()
    first = report.updated_at
    report.touch()
    assert report.updated_at != first
