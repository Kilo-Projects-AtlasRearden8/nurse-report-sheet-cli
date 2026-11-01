"""Tests for the CLI."""

from pathlib import Path

from click.testing import CliRunner

from nurse_report.cli import main


def _new_report(runner: CliRunner, data_dir: Path, report_id: str = "MRN-1") -> None:
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "new", "--name", "Ada L.", "--mrn", report_id],
        input="\n",
    )
    assert result.exit_code == 0, result.output


def test_new_report_creates_file(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "new", "--name", "Ada L.", "--mrn", "MRN-1"],
        input="\n",
    )
    assert result.exit_code == 0, result.output
    assert "Created report MRN-1" in result.output
    assert (data_dir / "MRN-1.json").exists()


def test_list_and_show(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    result = runner.invoke(main, ["--data-dir", str(data_dir), "list"])
    assert result.exit_code == 0
    assert "MRN-1" in result.output
    result = runner.invoke(main, ["--data-dir", str(data_dir), "show", "MRN-1"])
    assert result.exit_code == 0
    assert "Ada L." in result.output


def test_export_md(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    out = tmp_path / "out.md"
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "export-md", "MRN-1", "--output", str(out)],
    )
    assert result.exit_code == 0, result.output
    assert out.exists()
    assert "Ada L." in out.read_text()


def test_export_pdf(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    out = tmp_path / "out.pdf"
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "export-pdf", "MRN-1", "--output", str(out)],
    )
    assert result.exit_code == 0, result.output
    assert out.exists()
    assert out.stat().st_size > 0


def test_add_vital_and_task(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "add-vital", "MRN-1", "--bp", "120/80", "--hr", "72"],
    )
    assert result.exit_code == 0, result.output
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "add-task", "MRN-1", "--description", "Check IV"],
    )
    assert result.exit_code == 0, result.output
    result = runner.invoke(main, ["--data-dir", str(data_dir), "done-task", "MRN-1", "1"])
    assert result.exit_code == 0, result.output
    show = runner.invoke(main, ["--data-dir", str(data_dir), "show", "MRN-1"])
    assert "[x]" in show.output


def test_update_report(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    result = runner.invoke(
        main,
        ["--data-dir", str(data_dir), "update", "MRN-1", "--shift", "Night", "--nurse", "Jordan"],
    )
    assert result.exit_code == 0, result.output
    show = runner.invoke(main, ["--data-dir", str(data_dir), "show", "MRN-1"])
    assert "Night" in show.output
    assert "Jordan" in show.output


def test_delete_report(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner = CliRunner()
    _new_report(runner, data_dir)
    result = runner.invoke(
        main, ["--data-dir", str(data_dir), "delete", "MRN-1", "--yes"]
    )
    assert result.exit_code == 0, result.output
    assert not (data_dir / "MRN-1.json").exists()
