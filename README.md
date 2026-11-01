# Nurse Report Sheet CLI

A local-first command line tool that helps nurses build shift report sheets — patient summary, tasks, and vitals notes — and export them to Markdown or PDF. Built and published by [Asdale Dynamics, LLC](https://dylanasdale.github.io).

Education only. This tool is not medical advice and does not replace clinical judgment or your facility's protocols.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of Asdale Dynamics, LLC (Indiana, formed Oct 2026). His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. The LLC focuses on beginner-friendly AI education, books and guides, and practical tools it can publish or sell — including small open-source apps like this one.

This CLI is for nurses who want a simple, private way to document a shift without creating accounts, entering API keys, or sending patient data anywhere. Everything stays on your own computer.

## Features

- Create a shift report for a patient (name, MRN, room, age, allergies, code status, primary diagnosis)
- Add vital signs notes (time, BP, HR, RR, temperature, SpO2, pain, notes)
- Add tasks with due times and categories, then check them off
- Write a free-text patient summary for the shift
- Update an existing report or delete one you no longer need
- Store every report locally as a JSON file (no cloud, no accounts, no keys)
- Export a report to Markdown or PDF
- Works entirely offline

## Install

```bash
pip install .
```

Or run directly from source without installing:

```bash
python -m nurse_report --help
```

After installing, the `nurse-report` command is available:

```bash
nurse-report --help
```

## Usage, step by step

### 1. Create a report for a patient

The MRN becomes the file name for this patient's report, so keep it handy.

```bash
nurse-report new --name "Ada L." --mrn MRN-1 --room 4B --age 34 \
  --allergies "penicillin" --code-status Full --primary-dx Pneumonia \
  --shift Day --date 2026-11-01 --nurse "Dylan" \
  --summary "Stable overnight."
```

If you leave out `--name` or `--mrn`, the command will prompt you for them.

### 2. Add vital signs notes

```bash
nurse-report add-vital MRN-1 --time 08:00 --bp 120/80 --hr 72 --rr 16 \
  --temp 98.6 --spo2 98 --pain 2 --notes "Fine"
```

You can add as many vital notes as you need across a shift.

### 3. Add tasks

```bash
nurse-report add-task MRN-1 --description "Check IV" --due 09:00 --category Meds
nurse-report add-task MRN-1 --description "Turn and reposition" --due 10:00 --category ADLs
```

### 4. Mark a task done

Task numbers start at 1, in the order you added them.

```bash
nurse-report done-task MRN-1 1
```

### 5. Update an existing report

Need to fix a room, shift, nurse, or summary? Use `update`. The MRN cannot change because it's the file key.

```bash
nurse-report update MRN-1 --shift Night --nurse "Jordan" \
  --summary "Slept well, ambulated to hallway."
```

### 6. List your reports

```bash
nurse-report list
```

### 7. View a report

Print a report as Markdown to your terminal:

```bash
nurse-report show MRN-1
```

### 8. Export to Markdown or PDF

```bash
nurse-report export-md MRN-1 -o shift-report.md
nurse-report export-pdf MRN-1 -o shift-report.pdf
```

If you don't pass `--output`, the file is written to your current folder using the report ID as the file name.

### 9. Delete a report

```bash
nurse-report delete MRN-1 --yes
```

Without `--yes`, you'll be asked to confirm first.

## Where reports are stored

By default, reports are saved to `~/.local/share/nurse-report-sheet` as individual JSON files. You can change the folder with `--data-dir` or the `NURSE_REPORT_DATA_DIR` environment variable. No accounts, keys, network access, or personal data collection are involved.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: Asdale Dynamics, LLC — beginner-friendly AI education, books, guides, and practical tools. dylanasdale.github.io
