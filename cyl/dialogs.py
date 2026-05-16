import logging
from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from .schema import Config

logger = logging.getLogger(__name__)


class BirthdayInputDialog(QDialog):
    def __init__(self, config: Config | None = None):
        super().__init__()
        self._config = config
        self._result_config: Config | None = None
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("生年月日入力")
        self.setFixedSize(500, 180)
        layout = QFormLayout(self)

        self.birthday_input = QDateEdit(self)
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDisplayFormat("yyyy-MM-dd")
        if self._config:
            d = self._config.birthday
            self.birthday_input.setDate(QDate(d.year, d.month, d.day))
        else:
            self.birthday_input.setDate(QDate(1990, 1, 1))
        layout.addRow("生年月日:", self.birthday_input)

        self.target_age_input = QLineEdit(self)
        self.target_age_input.setPlaceholderText("目標年齢（例：90）")
        if self._config:
            self.target_age_input.setText(str(self._config.target_age))
        layout.addRow("目標年齢:", self.target_age_input)

        submit = QPushButton("確認", self)
        submit.clicked.connect(self._on_submit)
        layout.addRow(submit)

    def _on_submit(self) -> None:
        try:
            target_age = int(self.target_age_input.text())
        except ValueError:
            QMessageBox.warning(self, "入力エラー", "目標年齢は整数で入力してください。")
            return

        if not (1 <= target_age <= 150):
            QMessageBox.warning(self, "入力エラー", "目標年齢は 1〜150 の範囲で入力してください。")
            return

        qd = self.birthday_input.date()
        birthday = date(qd.year(), qd.month(), qd.day())
        today = date.today()

        if birthday >= today:
            QMessageBox.warning(self, "入力エラー", "生年月日は今日より前の日付を入力してください。")
            return

        current_age = (today - birthday).days // 365
        if target_age <= current_age:
            QMessageBox.warning(
                self,
                "入力エラー",
                f"目標年齢（{target_age}歳）は現在の年齢（{current_age}歳）より大きくしてください。",
            )
            return

        self._result_config = Config(birthday=birthday, target_age=target_age)
        self.accept()

    def get_config(self) -> Config:
        assert self._result_config is not None
        return self._result_config
