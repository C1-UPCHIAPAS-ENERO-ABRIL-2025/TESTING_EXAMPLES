from pathlib import Path

from click.testing import CliRunner

from inventory_system.cli import cli
from inventory_system.logic.discount_calculator import calculate_discount
from inventory_system.persistence import state_manager
from inventory_system.utils.backup_manager import create_backup


def test_login_success(monkeypatch):
    monkeypatch.setenv("INVENTORY_ADMIN_USER", "admin")
    monkeypatch.setenv("INVENTORY_ADMIN_PASSWORD", "securepass")
    runner = CliRunner()

    result = runner.invoke(cli, ["login", "admin", "securepass"])

    assert result.exit_code == 0
    assert "Login successful" in result.output


def test_login_failure_when_env_missing(monkeypatch):
    monkeypatch.delenv("INVENTORY_ADMIN_USER", raising=False)
    monkeypatch.delenv("INVENTORY_ADMIN_PASSWORD", raising=False)
    runner = CliRunner()

    result = runner.invoke(cli, ["login", "admin", "securepass"])

    assert result.exit_code == 0
    assert "Login failed" in result.output


def test_discount_command_output():
    runner = CliRunner()

    result = runner.invoke(cli, ["discount", "electronics", "gold", "12", "--holiday"])

    assert result.exit_code == 0
    assert "20.0%" in result.output


def test_state_save_and_load(tmp_path):
    filepath = tmp_path / "state.json"
    payload = {"items": ["book"], "user": "tester"}

    state_manager.save_state(payload, filepath)
    loaded = state_manager.load_state(filepath)

    assert loaded == payload


def test_backup_copies_state_file(tmp_path, monkeypatch):
    source = tmp_path / "inventory_state.json"
    source.write_text('{"items": ["keyboard"]}', encoding="utf-8")
    monkeypatch.setattr("inventory_system.utils.backup_manager.DEFAULT_STATE_FILE", source)

    destination_dir = tmp_path / "backups"
    output_path = create_backup(str(destination_dir))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


def test_discount_calculator_caps_maximum_discount():
    value = calculate_discount("books", "gold", 99, True)
    assert value <= 0.30
