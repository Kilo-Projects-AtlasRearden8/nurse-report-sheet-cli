"""Local JSON storage for shift reports."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Optional

from .models import ShiftReport

DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "nurse-report-sheet"


def slug_for(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "report"


class Storage:
    def __init__(self, data_dir: Optional[Path | str] = None) -> None:
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, report_id: str) -> Path:
        return self.data_dir / f"{report_id}.json"

    def report_id(self, report: ShiftReport) -> str:
        return report.patient.mrn or slug_for(report.patient.name)

    def save(self, report: ShiftReport) -> str:
        report.touch()
        report_id = self.report_id(report)
        path = self._path(report_id)
        path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        return report_id

    def load(self, report_id: str) -> ShiftReport:
        path = self._path(report_id)
        if not path.exists():
            raise FileNotFoundError(f"Report not found: {report_id}")
        return ShiftReport.model_validate_json(path.read_text(encoding="utf-8"))

    def list_reports(self) -> list[tuple[str, str]]:
        results: list[tuple[str, str]] = []
        for path in sorted(self.data_dir.glob("*.json")):
            try:
                report = ShiftReport.model_validate_json(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            label = report.patient.name or report_id_stem(path)
            results.append((path.stem, label))
        return results

    def delete(self, report_id: str) -> None:
        path = self._path(report_id)
        if path.exists():
            path.unlink()


def report_id_stem(path: Path) -> str:
    return path.stem
