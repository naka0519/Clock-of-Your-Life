import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QTime, QDateTime, Qt
from PyQt6.QtGui import QColor


class ClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 40px;")
        
        self.setGeometry(300, 300, 280, 100)
        self.setWindowTitle('時計アプリ')
        
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()
        self.show()

    def showTime(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.time_label.setText(current_time)

def main():
    app = QApplication(sys.argv)
    ex = ClockApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
