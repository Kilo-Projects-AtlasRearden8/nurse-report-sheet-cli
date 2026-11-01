"""Export shift reports to Markdown and PDF."""

from __future__ import annotations

from pathlib import Path

from .models import ShiftReport


def to_markdown(report: ShiftReport) -> str:
    p = report.patient
    lines: list[str] = []
    lines.append(f"# Shift Report Sheet")
    lines.append("")
    lines.append(f"**Patient:** {p.name or '—'}  ")
    lines.append(f"**MRN:** {p.mrn or '—'}  ")
    lines.append(f"**Room:** {p.room or '—'}  ")
    lines.append(f"**Age:** {p.age if p.age is not None else '—'}  ")
    lines.append(f"**Shift:** {report.shift or '—'}  ")
    lines.append(f"**Date:** {report.date or '—'}  ")
    lines.append(f"**Nurse:** {report.nurse or '—'}  ")
    lines.append("")
    if p.allergies:
        lines.append("## Allergies")
        lines.append("")
        lines.append(", ".join(p.allergies))
        lines.append("")
    if p.code_status:
        lines.append(f"**Code Status:** {p.code_status}")
        lines.append("")
    if p.primary_dx:
        lines.append(f"**Primary DX:** {p.primary_dx}")
        lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(report.summary or "—")
    lines.append("")
    lines.append("## Tasks")
    lines.append("")
    if report.tasks:
        for i, task in enumerate(report.tasks, 1):
            box = "[x]" if task.done else "[ ]"
            due = f" (due {task.due})" if task.due else ""
            cat = f" [{task.category}]" if task.category else ""
            lines.append(f"{i}. {box} {task.description}{due}{cat}")
    else:
        lines.append("—")
    lines.append("")
    lines.append("## Vitals")
    lines.append("")
    if report.vitals:
        lines.append("| Time | BP | HR | RR | Temp | SpO2 | Pain | Notes |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for v in report.vitals:
            lines.append(
                f"| {v.time} | {v.bp} | {v.hr} | {v.rr} | {v.temp} | "
                f"{v.spo2} | {v.pain} | {v.notes} |"
            )
    else:
        lines.append("—")
    lines.append("")
    lines.append(f"*Generated {report.updated_at} — nurse-report-sheet-cli (Asdale Dynamics, LLC)*")
    return "\n".join(lines)


def to_pdf(report: ShiftReport, output: Path | str) -> Path:
    output = Path(output)
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    styles = getSampleStyleSheet()
    p = report.patient

    doc_elements = []
    doc_elements.append(Paragraph("Shift Report Sheet", styles["Title"]))
    doc_elements.append(Spacer(1, 0.25 * inch))

    info = [
        ["Patient:", p.name or "—", "MRN:", p.mrn or "—"],
        ["Room:", p.room or "—", "Age:", str(p.age) if p.age is not None else "—"],
        ["Shift:", report.shift or "—", "Date:", report.date or "—"],
        ["Nurse:", report.nurse or "—", "Code Status:", p.code_status or "—"],
        ["Allergies:", ", ".join(p.allergies) or "—", "Primary DX:", p.primary_dx or "—"],
    ]
    info_table = Table(info, colWidths=[0.9 * inch, 2.6 * inch, 0.9 * inch, 2.6 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    doc_elements.append(info_table)
    doc_elements.append(Spacer(1, 0.25 * inch))

    doc_elements.append(Paragraph("Summary", styles["Heading2"]))
    doc_elements.append(Paragraph(report.summary or "—", styles["Normal"]))
    doc_elements.append(Spacer(1, 0.15 * inch))

    doc_elements.append(Paragraph("Tasks", styles["Heading2"]))
    task_rows = [["#", "Done", "Task", "Due", "Category"]]
    for i, task in enumerate(report.tasks, 1):
        task_rows.append(
            [
                str(i),
                "x" if task.done else " ",
                task.description,
                task.due or "—",
                task.category or "—",
            ]
        )
    if len(task_rows) == 1:
        task_rows.append(["—", " ", "—", "—", "—"])
    task_table = Table(task_rows, colWidths=[0.35 * inch, 0.4 * inch, 3.2 * inch, 0.8 * inch, 1.25 * inch])
    task_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    doc_elements.append(task_table)
    doc_elements.append(Spacer(1, 0.15 * inch))

    doc_elements.append(Paragraph("Vitals", styles["Heading2"]))
    vital_rows = [["Time", "BP", "HR", "RR", "Temp", "SpO2", "Pain", "Notes"]]
    for v in report.vitals:
        vital_rows.append(
            [v.time, v.bp, v.hr, v.rr, v.temp, v.spo2, v.pain, v.notes]
        )
    if len(vital_rows) == 1:
        vital_rows.append(["—"] * 8)
    vital_table = Table(
        vital_rows,
        colWidths=[0.5 * inch, 0.65 * inch, 0.5 * inch, 0.5 * inch, 0.6 * inch, 0.6 * inch, 0.5 * inch, 2.2 * inch],
        repeatRows=1,
    )
    vital_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    doc_elements.append(vital_table)
    doc_elements.append(Spacer(1, 0.25 * inch))
    doc_elements.append(
        Paragraph(
            f"Generated {report.updated_at} — nurse-report-sheet-cli (Asdale Dynamics, LLC)",
            styles["Italic"],
        )
    )

    from reportlab.platypus import SimpleDocTemplate

    doc = SimpleDocTemplate(str(output), pagesize=letter)
    doc.build(doc_elements)
    return output
