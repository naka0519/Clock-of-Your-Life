from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ..calc import RemainingTime


class TimeLabels(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._time_label = QLabel("残り時間: 待機中...", self)
        self._time_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self._time_label)

        self._months_label = QLabel("", self)
        self._months_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self._months_label)

    def update_display(self, rt: RemainingTime) -> None:
        self._time_label.setText(
            f"残り時間: {rt.years}年 {rt.months}ヶ月 {rt.days}日 "
            f"{rt.hours}時間 {rt.minutes}分 {rt.seconds}秒"
        )
        self._months_label.setText(f"残り月数: {rt.total_months} ヶ月")
