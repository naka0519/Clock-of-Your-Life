from datetime import date
from pathlib import Path

import pytest

from cyl.schema import Config
from cyl.storage import load_config, save_config


@pytest.fixture(autouse=True)
def redirect_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("cyl.storage.CONFIG_PATH", tmp_path / "config.json")


def test_load_returns_none_when_no_file():
    assert load_config() is None


def test_roundtrip():
    cfg = Config(birthday=date(1990, 5, 19), target_age=90)
    save_config(cfg)
    loaded = load_config()
    assert loaded is not None
    assert loaded.birthday == cfg.birthday
    assert loaded.target_age == cfg.target_age
    assert loaded.theme == cfg.theme


def test_load_corrupt_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    p = tmp_path / "config.json"
    monkeypatch.setattr("cyl.storage.CONFIG_PATH", p)
    p.write_text("not valid json", encoding="utf-8")
    assert load_config() is None


def test_load_invalid_schema(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    p = tmp_path / "config.json"
    monkeypatch.setattr("cyl.storage.CONFIG_PATH", p)
    p.write_text('{"birthday": "not-a-date", "target_age": 90}', encoding="utf-8")
    assert load_config() is None


def test_save_creates_parent_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    nested = tmp_path / "a" / "b" / "config.json"
    monkeypatch.setattr("cyl.storage.CONFIG_PATH", nested)
    cfg = Config(birthday=date(2000, 1, 1), target_age=80)
    save_config(cfg)
    assert nested.exists()
