from datetime import date

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..calc import weeks_elapsed

_CELL = 7
_GAP = 1
_STEP = _CELL + _GAP
_LABEL_W = 26
_HEADER_H = 14

_COLORS: dict[str, dict[str, QColor]] = {
    "default": {
        "past": QColor("#6b7280"),
        "current": QColor("#f97316"),
        "future_fill": QColor("#f9fafb"),
        "future_border": QColor("#d1d5db"),
        "label": QColor("#6b7280"),
    },
    "dark": {
        "past": QColor("#6272a4"),
        "current": QColor("#f97316"),
        "future_fill": QColor("#2a2a3e"),
        "future_border": QColor("#45475a"),
        "label": QColor("#7f849c"),
    },
}


class _LifeGridCanvas(QWidget):
    def __init__(
        self,
        birthday: date,
        target_age: int,
        theme: str = "default",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._birthday = birthday
        self._target_age = target_age
        self._elapsed = weeks_elapsed(birthday)
        self._colors = _COLORS.get(theme, _COLORS["default"])
        w = _LABEL_W + _GAP + 52 * _STEP
        h = _HEADER_H + _GAP + target_age * _STEP
        self.setFixedSize(w, h)

    def paintEvent(self, event) -> None:
        from PyQt6.QtGui import QPainter

        c = self._colors
        painter = QPainter(self)

        no_pen = QPen(Qt.PenStyle.NoPen)
        border_pen = QPen(c["future_border"])

        # Week header: quarter labels (1, 14, 27, 40)
        painter.setPen(c["label"])
        for q, lbl in ((0, "1"), (13, "14"), (26, "27"), (39, "40")):
            x = _LABEL_W + _GAP + q * _STEP
            painter.drawText(
                QRect(x, 0, 3 * _STEP, _HEADER_H),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                lbl,
            )

        for year in range(self._target_age):
            y = _HEADER_H + _GAP + year * _STEP

            if year % 10 == 0:
                painter.setPen(c["label"])
                painter.drawText(
                    QRect(0, y, _LABEL_W - 2, _CELL),
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(year),
                )

            for week in range(52):
                idx = year * 52 + week
                x = _LABEL_W + _GAP + week * _STEP
                rect = QRect(x, y, _CELL, _CELL)

                if idx < self._elapsed:
                    painter.setPen(no_pen)
                    painter.fillRect(rect, c["past"])
                elif idx == self._elapsed:
                    painter.setPen(no_pen)
                    painter.fillRect(rect, c["current"])
                else:
                    painter.fillRect(rect, c["future_fill"])
                    painter.setPen(border_pen)
                    painter.drawRect(rect)

        painter.end()


class LifeGridDialog(QDialog):
    def __init__(
        self,
        birthday: date,
        target_age: int,
        theme: str = "default",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("人生グリッド")
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinMaxButtonsHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        canvas = _LifeGridCanvas(birthday, target_age, theme)

        scroll = QScrollArea(self)
        scroll.setWidget(canvas)
        scroll.setWidgetResizable(False)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Legend
        legend = QLabel(
            '<span style="color:#6b7280">■</span> 過去　'
            '<span style="color:#f97316">■</span> 現在　'
            '□ 未来'
        )
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        legend.setStyleSheet("font-size: 11px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        layout.addWidget(scroll)
        layout.addWidget(legend)

        dialog_w = canvas.width() + 20
        dialog_h = min(canvas.height() + 52, 520)
        self.resize(dialog_w, dialog_h)
        self.setMinimumWidth(dialog_w)
