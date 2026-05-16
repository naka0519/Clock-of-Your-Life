import logging

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from .calc import remaining_time
from .dialogs import BirthdayInputDialog
from .schema import Config
from .storage import load_config, save_config
from .themes import apply_theme
from .widgets.labels import TimeLabels
from .widgets.progress import ProgressBars

logger = logging.getLogger(__name__)


class ClockApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.config: Config | None = None
        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle("あなたの残り時間")
        self.setFixedSize(500, 360)
        self.setGeometry(500, 500, 500, 360)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        self._time_labels = TimeLabels(self)
        layout.addWidget(self._time_labels)

        self._progress_bars = ProgressBars(self)
        layout.addWidget(self._progress_bars)

        btn_layout = QHBoxLayout()

        grid_btn = QPushButton("人生グリッド", self)
        grid_btn.setFixedHeight(32)
        grid_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        grid_btn.clicked.connect(self._show_life_grid)
        btn_layout.addWidget(grid_btn)

        settings_btn = QPushButton("設定を変更", self)
        settings_btn.setFixedHeight(32)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.clicked.connect(self._request_birthday)
        btn_layout.addWidget(settings_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time)
        self._timer.start(1000)

        self.config = load_config()
        if self.config is None:
            self._request_birthday()
        else:
            logger.info(
                "loaded existing config (birthday=%s, target=%d)",
                self.config.birthday,
                self.config.target_age,
            )
            apply_theme(self.config.theme)
            self._update_time()

        self.show()

    def _show_life_grid(self) -> None:
        if self.config is None:
            return
        from .widgets.life_grid import LifeGridDialog

        dialog = LifeGridDialog(
            self.config.birthday,
            self.config.target_age,
            theme=self.config.theme,
            parent=self,
        )
        dialog.exec()

    def _request_birthday(self) -> None:
        dialog = BirthdayInputDialog(self.config)
        if dialog.exec():
            self.config = dialog.get_config()
            save_config(self.config)
            logger.info(
                "new config saved (birthday=%s, target=%d)",
                self.config.birthday,
                self.config.target_age,
            )
            apply_theme(self.config.theme)
            self._update_time()
        else:
            logger.info("user cancelled birthday input")

    def _update_time(self) -> None:
        if self.config is None:
            return
        rt = remaining_time(self.config.birthday, self.config.target_age)
        self._time_labels.update_display(rt)
        self._progress_bars.update_display(self.config.birthday, self.config.target_age)
