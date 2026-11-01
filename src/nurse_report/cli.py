"""Command line interface for nurse-report-sheet-cli."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click

from .export import to_markdown, to_pdf
from .models import Patient, ShiftReport, Task, VitalNote
from .storage import Storage, slug_for


@click.group()
@click.option(
    "--data-dir",
    envvar="NURSE_REPORT_DATA_DIR",
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory for local JSON storage (default: ~/.local/share/nurse-report-sheet).",
)
@click.pass_context
def main(ctx: click.Context, data_dir: Optional[Path]) -> None:
    ctx.obj = Storage(data_dir)


@main.command()
@click.option("--name", prompt="Patient name", help="Patient full name.")
@click.option("--mrn", prompt="Medical record number", help="MRN (used as the file key).")
@click.option("--room", default="", help="Room number.")
@click.option("--age", type=click.INT, default=None, help="Patient age.")
@click.option("--allergies", default="", help="Comma-separated allergies.")
@click.option("--code-status", default="", help="Code status.")
@click.option("--primary-dx", default="", help="Primary diagnosis.")
@click.option("--shift", default="", help="Shift (day/evening/night).")
@click.option("--date", default="", help="Report date (YYYY-MM-DD).")
@click.option("--nurse", default="", help="Nurse name.")
@click.option("--summary", default="", help="Patient summary.")
@click.pass_obj
def new(
    storage: Storage,
    name: str,
    mrn: str,
    room: str,
    age: Optional[int],
    allergies: str,
    code_status: str,
    primary_dx: str,
    shift: str,
    date: str,
    nurse: str,
    summary: str,
) -> None:
    """Create a new shift report for a patient."""
    patient = Patient(
        name=name,
        mrn=mrn,
        room=room,
        age=age,
        allergies=[a.strip() for a in allergies.split(",") if a.strip()],
        code_status=code_status,
        primary_dx=primary_dx,
    )
    report = ShiftReport(
        patient=patient,
        shift=shift,
        date=date,
        nurse=nurse,
        summary=summary,
    )
    report_id = storage.save(report)
    click.echo(f"Created report {report_id} for {patient.name}")


@main.command(name="add-vital")
@click.argument("report_id")
@click.option("--time", "time_", default="", help="Time (HH:MM).")
@click.option("--bp", default="", help="Blood pressure.")
@click.option("--hr", default="", help="Heart rate.")
@click.option("--rr", default="", help="Respiratory rate.")
@click.option("--temp", default="", help="Temperature.")
@click.option("--spo2", default="", help="SpO2.")
@click.option("--pain", default="", help="Pain score.")
@click.option("--notes", default="", help="Vital notes.")
@click.pass_obj
def add_vital(
    storage: Storage,
    report_id: str,
    time_: str,
    bp: str,
    hr: str,
    rr: str,
    temp: str,
    spo2: str,
    pain: str,
    notes: str,
) -> None:
    """Add a vital note to a report."""
    report = storage.load(report_id)
    report.vitals.append(
        VitalNote(time=time_, bp=bp, hr=hr, rr=rr, temp=temp, spo2=spo2, pain=pain, notes=notes)
    )
    storage.save(report)
    click.echo(f"Added vital note to {report_id}")


@main.command(name="add-task")
@click.argument("report_id")
@click.option("--description", prompt="Task description", help="Task description.")
@click.option("--due", default="", help="Due time.")
@click.option("--category", default="", help="Task category.")
@click.pass_obj
def add_task(storage: Storage, report_id: str, description: str, due: str, category: str) -> None:
    """Add a task to a report."""
    report = storage.load(report_id)
    report.tasks.append(Task(description=description, due=due, category=category))
    storage.save(report)
    click.echo(f"Added task to {report_id}")


@main.command(name="done-task")
@click.argument("report_id")
@click.argument("task_index", type=click.INT)
@click.pass_obj
def done_task(storage: Storage, report_id: str, task_index: int) -> None:
    """Mark a task as done (1-based index)."""
    report = storage.load(report_id)
    if not 1 <= task_index <= len(report.tasks):
        raise click.ClickException(f"Task index {task_index} out of range")
    report.tasks[task_index - 1].done = True
    storage.save(report)
    click.echo(f"Marked task {task_index} done in {report_id}")


@main.command(name="update")
@click.argument("report_id")
@click.option("--name", default=None, help="Patient full name.")
@click.option("--room", default=None, help="Room number.")
@click.option("--age", type=click.INT, default=None, help="Patient age.")
@click.option("--allergies", default=None, help="Comma-separated allergies.")
@click.option("--code-status", default=None, help="Code status.")
@click.option("--primary-dx", default=None, help="Primary diagnosis.")
@click.option("--shift", default=None, help="Shift (day/evening/night).")
@click.option("--date", default=None, help="Report date (YYYY-MM-DD).")
@click.option("--nurse", default=None, help="Nurse name.")
@click.option("--summary", default=None, help="Patient summary.")
@click.pass_obj
def update_report(
    storage: Storage,
    report_id: str,
    name: Optional[str],
    room: Optional[str],
    age: Optional[int],
    allergies: Optional[str],
    code_status: Optional[str],
    primary_dx: Optional[str],
    shift: Optional[str],
    date: Optional[str],
    nurse: Optional[str],
    summary: Optional[str],
) -> None:
    """Update fields on an existing report (MRN is the file key and cannot change)."""
    report = storage.load(report_id)
    p = report.patient
    if name is not None:
        p.name = name
    if room is not None:
        p.room = room
    if age is not None:
        p.age = age
    if allergies is not None:
        p.allergies = [a.strip() for a in allergies.split(",") if a.strip()]
    if code_status is not None:
        p.code_status = code_status
    if primary_dx is not None:
        p.primary_dx = primary_dx
    if shift is not None:
        report.shift = shift
    if date is not None:
        report.date = date
    if nurse is not None:
        report.nurse = nurse
    if summary is not None:
        report.summary = summary
    storage.save(report)
    click.echo(f"Updated report {report_id}")


@main.command(name="delete")
@click.argument("report_id")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
@click.pass_obj
def delete_report(storage: Storage, report_id: str, yes: bool) -> None:
    """Delete a stored report."""
    if not yes:
        if not click.confirm(f"Delete report {report_id}?"):
            click.echo("Cancelled.")
            return
    storage.delete(report_id)
    click.echo(f"Deleted {report_id}")


@main.command(name="list")
@click.pass_obj
def list_reports(storage: Storage) -> None:
    """List stored reports."""
    reports = storage.list_reports()
    if not reports:
        click.echo("No reports found.")
        return
    for report_id, label in reports:
        click.echo(f"{report_id}\t{label}")


@main.command(name="show")
@click.argument("report_id")
@click.pass_obj
def show_report(storage: Storage, report_id: str) -> None:
    """Print a report as Markdown to stdout."""
    report = storage.load(report_id)
    click.echo(to_markdown(report))


@main.command(name="export-md")
@click.argument("report_id")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output Markdown path.")
@click.pass_obj
def export_md(storage: Storage, report_id: str, output: Optional[Path]) -> None:
    """Export a report to Markdown."""
    report = storage.load(report_id)
    if output is None:
        output = Path(f"{slug_for(report_id)}.md")
    output.write_text(to_markdown(report), encoding="utf-8")
    click.echo(f"Wrote {output}")


@main.command(name="export-pdf")
@click.argument("report_id")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output PDF path.")
@click.pass_obj
def export_pdf(storage: Storage, report_id: str, output: Optional[Path]) -> None:
    """Export a report to PDF."""
    report = storage.load(report_id)
    if output is None:
        output = Path(f"{slug_for(report_id)}.pdf")
    to_pdf(report, output)
    click.echo(f"Wrote {output}")


if __name__ == "__main__":
    main()
