"""Data models for shift report sheets."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Patient(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = ""
    mrn: str = ""
    room: str = ""
    age: Optional[int] = None
    allergies: list[str] = Field(default_factory=list)
    code_status: str = ""
    primary_dx: str = ""


class VitalNote(BaseModel):
    time: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M"))
    bp: str = ""
    hr: str = ""
    rr: str = ""
    temp: str = ""
    spo2: str = ""
    pain: str = ""
    notes: str = ""


class Task(BaseModel):
    description: str = ""
    due: str = ""
    done: bool = False
    category: str = ""


class ShiftReport(BaseModel):
    patient: Patient = Field(default_factory=Patient)
    shift: str = ""
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    nurse: str = ""
    summary: str = ""
    tasks: list[Task] = Field(default_factory=list)
    vitals: list[VitalNote] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def touch(self) -> None:
        self.updated_at = datetime.now().isoformat()
