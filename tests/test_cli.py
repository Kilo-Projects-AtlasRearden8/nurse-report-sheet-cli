"""Tests for the CLI."""

from click.testing import CliRunner
from pathlib import Path

from nurse_report.cli import main


def test_new_report_creates_file(tmp_path, monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            main,
            ["--data-dir", "data", "new", "--name", "Ada L.", "--mrn", "MRN-1", "--room", "4B"],
            input="\n",
        )
        assert result.exit_code == 0, result.output
        assert "Created report MRN-1" in result.output


def test_list_and_show(tmp_path, monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(
            main,
            ["--data-dir", "data", "new", "--name", "Ada L.", "--mrn", "MRN-1"],
            input="\n",
        )
        result = runner.invoke(main, ["--data-dir", "data", "list"])
        assert result.exit_code == 0
        assert "MRN-1" in result.output
        result = runner.invoke(main, ["--data-dir", "data", "show", "MRN-1"])
        assert result.exit_code == 0
        assert "Ada L." in result.output


def test_export_md(tmp_path, monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(
            main,
            ["--data-dir", "data", "new", "--name", "Ada L.", "--mrn", "MRN-1"],
            input="\n",
        )
        result = runner.invoke(main, ["--data-dir", "data", "export-md", "MRN-1", "--output", "out.md"])
        assert result.exit_code == 0, result.output
        assert Path("out.md").exists()
        content = Path("out.md").read_text()
        assert "Ada L." in content


def test_add_vital_and_task(tmp_path, monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        runner.invoke(
            main,
            ["--data-dir", "data", "new", "--name", "Ada L.", "--mrn", "MRN-1"],
            input="\n",
        )
        result = runner.invoke(
            main,
            ["--data-dir", "data", "add-vital", "MRN-1", "--bp", "120/80", "--hr", "72"],
        )
        assert result.exit_code == 0, result.output
        result = runner.invoke(
            main,
            ["--data-dir", "data", "add-task", "MRN-1", "--description", "Check IV"],
        )
        assert result.exit_code == 0, result.output
        result = runner.invoke(main, ["--data-dir", "data", "done-task", "MRN-1", "1"])
        assert result.exit_code == 0, result.output
        show = runner.invoke(main, ["--data-dir", "data", "show", "MRN-1"])
        assert "[x]" in show.output or "x" in show.output
