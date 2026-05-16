from datetime import date, datetime

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget

from ..calc import lifetime_progress, today_progress, week_progress


class ProgressBars(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        self._today_bar, self._today_pct = self._add_row(layout, "今日")
        self._week_bar, self._week_pct = self._add_row(layout, "今週")
        self._life_bar, self._life_pct = self._add_row(layout, "人生")

    def _add_row(self, parent_layout: QVBoxLayout, text: str) -> tuple[QProgressBar, QLabel]:
        row = QHBoxLayout()
        label = QLabel(text, self)
        label.setFixedWidth(36)
        bar = QProgressBar(self)
        bar.setRange(0, 10000)
        bar.setTextVisible(False)
        pct = QLabel("0.00%", self)
        pct.setFixedWidth(60)
        row.addWidget(label)
        row.addWidget(bar)
        row.addWidget(pct)
        parent_layout.addLayout(row)
        return bar, pct

    def update_display(self, birthday: date, target_age: int, now: datetime | None = None) -> None:
        if now is None:
            now = datetime.now()
        tp = today_progress(now)
        wp = week_progress(now)
        lp = lifetime_progress(birthday, target_age, now.date())

        self._today_bar.setValue(int(tp * 10000))
        self._week_bar.setValue(int(wp * 10000))
        self._life_bar.setValue(int(lp * 10000))

        self._today_pct.setText(f"{tp * 100:.2f}%")
        self._week_pct.setText(f"{wp * 100:.2f}%")
        self._life_pct.setText(f"{lp * 100:.2f}%")
