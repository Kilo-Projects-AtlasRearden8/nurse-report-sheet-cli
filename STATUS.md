# STATUS

## What was built

`nurse-report-sheet-cli` — a local-first Python CLI for nurses to build shift
report sheets (patient summary, tasks, vitals notes) and export them to
Markdown or PDF. Built for Asdale Dynamics, LLC (credit in README and LICENSE).

## Contents

- `src/nurse_report/models.py` — Pydantic models: Patient, VitalNote, Task, ShiftReport
- `src/nurse_report/storage.py` — local JSON storage (one file per report, keyed by MRN or name slug)
- `src/nurse_report/export.py` — Markdown and PDF (reportlab) export
- `src/nurse_report/cli.py` — Click CLI: new, add-vital, add-task, done-task, list, show, export-md, export-pdf
- `src/nurse_report/__main__.py` — `python -m nurse_report` entry point
- `tests/` — 20 pytest tests covering models, storage, export, CLI
- `pyproject.toml` — hatchling build, Click/Pydantic/reportlab dependencies, console script `nurse-report`
- `README.md` — usage, install, credit to Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `STATUS.md` — this file

## How to run

```bash
# from source
PYTHONPATH=src python3 -m nurse_report --help

# or install
pip install -e .
nurse-report --help

# example session
nurse-report new --name "Ada L." --mrn MRN-1 --room 4B --shift Day --summary "Stable overnight."
nurse-report add-vital MRN-1 --bp 120/80 --hr 72
nurse-report add-task MRN-1 --description "Check IV"
nurse-report done-task MRN-1 1
nurse-report show MRN-1
nurse-report export-md MRN-1 -o report.md
nurse-report export-pdf MRN-1 -o report.pdf
```

Storage defaults to `~/.local/share/nurse-report-sheet`; override with
`--data-dir` or `NURSE_REPORT_DATA_DIR`. No accounts, keys, network, or personal
data are used.

## Verification results

- `pytest`: 20 passed
- Editable install via `pip install -e . --break-system-packages`: success
- `nurse-report --help`: works
- End-to-end session (create, add vital, add task, mark done, list, export-md, export-pdf): success; Markdown and PDF files produced and non-empty

## Known gaps

- JSON storage is not encrypted at rest (local-first design; protect the data directory with filesystem permissions)
- No edit/delete of individual patient fields (delete whole report via storage only)
- Default shift/date use today; backdating requires `--shift`/`--date` flags
- PDF styling is basic; no page headers/footers
- No sync, backup, or multi-device support (intentionally local-first)
- Education only — not medical advice; does not replace clinical judgment or facility protocols
