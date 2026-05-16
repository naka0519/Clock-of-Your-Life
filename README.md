# Clock-of-Your-Life

### 概要

入力した年齢までの残り時間を可視化するデスクトップアプリ。

設定は `~/.cyl/config.json` に保存され、2回目以降は生年月日入力をスキップして即起動。

---

### セットアップ

```bash
# uv インストール済みであること（https://docs.astral.sh/uv/）
uv sync --group dev
```

### 起動

```bash
uv run python -m cyl
```

### 開発時（ファイル変更で自動再起動）

```bash
uv run watchfiles "python -m cyl" cyl/
```

### テスト

```bash
uv run pytest -v
```

### .exe ビルド

```bash
uv run pyinstaller CYL.spec
# → dist/CYL.exe
```

---

### ディレクトリ構成

```
Clock-of-Your-Life/
  cyl/
    __init__.py
    __main__.py      # エントリポイント
    app.py           # ClockApp (QWidget)
    dialogs.py       # BirthdayInputDialog
    calc.py          # 純粋関数（残り時間計算）
    storage.py       # ~/.cyl/config.json 読み書き・ロギング設定
    schema.py        # pydantic モデル（Config）
    widgets/
      labels.py      # TimeLabels
  tests/
    test_calc.py
    test_storage.py
  pyproject.toml
  CYL.spec
```

### 設定ファイル

`~/.cyl/config.json` — 生年月日・目標年齢・テーマを保存。削除すると初回入力フローに戻る。

ログ: `~/.cyl/cyl.log`（1MB ローテーション、最大3世代）
