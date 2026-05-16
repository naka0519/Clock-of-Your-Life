from PyQt6.QtWidgets import QApplication

THEMES: dict[str, str] = {
    "default": "",
    "dark": (
        "QWidget { background-color: #1e1e2e; color: #cdd6f4; }"
        "QProgressBar { border: 1px solid #45475a; background-color: #313244;"
        " border-radius: 3px; height: 16px; }"
        "QProgressBar::chunk { background-color: #89b4fa; border-radius: 2px; }"
        "QLabel { color: #cdd6f4; }"
        "QPushButton { background-color: #45475a; color: #cdd6f4;"
        " border: 1px solid #6c7086; padding: 4px 8px; border-radius: 3px; }"
        "QPushButton:hover { background-color: #585b70; }"
        "QLineEdit, QDateEdit { background-color: #313244; color: #cdd6f4;"
        " border: 1px solid #45475a; padding: 2px; }"
        "QComboBox { background-color: #313244; color: #cdd6f4;"
        " border: 1px solid #45475a; }"
        "QComboBox QAbstractItemView { background-color: #313244; color: #cdd6f4; }"
        "QDialog { background-color: #1e1e2e; }"
        "QScrollArea { background-color: #1e1e2e; border: none; }"
    ),
}

THEME_LABELS: dict[str, str] = {
    "default": "デフォルト",
    "dark": "ダーク",
}


def apply_theme(theme: str) -> None:
    app = QApplication.instance()
    if app is not None:
        app.setStyleSheet(THEMES.get(theme, ""))
