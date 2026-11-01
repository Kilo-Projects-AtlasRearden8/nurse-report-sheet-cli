"""Tests for JSON storage."""

import json
from pathlib import Path

import pytest

from nurse_report.models import Patient, ShiftReport
from nurse_report.storage import Storage


@pytest.fixture
def temp_storage(tmp_path: Path) -> Storage:
    return Storage(data_dir=tmp_path / "data")


def test_save_and_load_roundtrip(temp_storage: Storage):
    report = ShiftReport(patient=Patient(name="Ada L.", mrn="MRN-1", room="4B"))
    report_id = temp_storage.save(report)
    loaded = temp_storage.load(report_id)
    assert loaded.patient.name == "Ada L."
    assert loaded.patient.mrn == "MRN-1"
    assert loaded.patient.room == "4B"


def test_mrn_used_as_file_key(temp_storage: Storage):
    report = ShiftReport(patient=Patient(name="Ignored", mrn="MRN-99"))
    report_id = temp_storage.save(report)
    assert report_id == "MRN-99"
    assert (temp_storage.data_dir / "MRN-99.json").exists()


def test_slug_fallback_when_no_mrn(temp_storage: Storage):
    report = ShiftReport(patient=Patient(name="Ada Lovelace"))
    report_id = temp_storage.save(report)
    assert report_id == "ada-lovelace"


def test_list_reports(temp_storage: Storage):
    temp_storage.save(ShiftReport(patient=Patient(name="One", mrn="M1")))
    temp_storage.save(ShiftReport(patient=Patient(name="Two", mrn="M2")))
    ids = [rid for rid, _ in temp_storage.list_reports()]
    assert "M1" in ids and "M2" in ids


def test_delete_report(temp_storage: Storage):
    report_id = temp_storage.save(ShiftReport(patient=Patient(name="Bye", mrn="MBYE")))
    temp_storage.delete(report_id)
    assert not (temp_storage.data_dir / f"{report_id}.json").exists()


def test_load_missing_raises(temp_storage: Storage):
    with pytest.raises(FileNotFoundError):
        temp_storage.load("does-not-exist")


def test_storage_creates_directory(tmp_path: Path):
    data_dir = tmp_path / "nested" / "data"
    storage = Storage(data_dir=data_dir)
    assert data_dir.exists()
    storage.save(ShiftReport(patient=Patient(name="X", mrn="MX")))
    assert (data_dir / "MX.json").exists()
