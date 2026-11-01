# Nurse Report Sheet CLI

A local-first command line tool for nurses to build shift report sheets — patient summary, tasks, and vitals notes — and export them to Markdown or PDF. Built and published by [Asdale Dynamics, LLC](https://dylanasdale.github.io).

Education only. This tool is not medical advice and does not replace clinical judgment or facility protocols.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. The LLC focuses on beginner-friendly AI education, books and guides, and practical tools it can publish or sell — including small open-source apps like this one.

## Features

- Create shift reports per patient (name, MRN, room, age, allergies, code status, primary DX)
- Add vital signs notes (time, BP, HR, RR, temp, SpO2, pain, notes)
- Add and check off tasks with due times and categories
- Free-text patient summary per shift
- Store reports locally as JSON (no accounts, no keys, no cloud)
- Export to Markdown or PDF
- Works entirely offline

## Install

```bash
pip install .
```

Or run from source:

```bash
python -m nurse_report --help
```

## Usage

Create a report for a patient:

```bash
nurse-report new --name "Ada L." --mrn MRN-1 --room 4B --age 34 \
  --allergies "penicillin" --code-status Full --primary-dx Pneumonia \
  --shift Day --date 2026-11-01 --nurse "Dylan" \
  --summary "Stable overnight."
```

Add a vital note:

```bash
nurse-report add-vital MRN-1 --time 08:00 --bp 120/80 --hr 72 --rr 16 \
  --temp 98.6 --spo2 98 --pain 2 --notes "Fine"
```

Add a task:

```bash
nurse-report add-task MRN-1 --description "Check IV" --due 09:00 --category Meds
```

Mark a task done:

```bash
nurse-report done-task MRN-1 1
```

List reports:

```bash
nurse-report list
```

Show a report as Markdown:

```bash
nurse-report show MRN-1
```

Export to Markdown:

```bash
nurse-report export-md MRN-1 -o shift-report.md
```

Export to PDF:

```bash
nurse-report export-pdf MRN-1 -o shift-report.pdf
```

Storage location defaults to `~/.local/share/nurse-report-sheet`. Override with `--data-dir` or the `NURSE_REPORT_DATA_DIR` environment variable.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides, and practical tools. dylanasdale.github.io
