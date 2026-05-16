import sys

from PyQt6.QtWidgets import QApplication

from .app import ClockApp
from .storage import setup_logging


def main() -> None:
    setup_logging()
    app = QApplication(sys.argv)
    _window = ClockApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
