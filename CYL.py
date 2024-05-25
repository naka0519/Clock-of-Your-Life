import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDialog, QFormLayout
from PyQt6.QtCore import QTimer, QTime, QDateTime

class BirthdayInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("生年月日入力")
        layout = QFormLayout(self)

        self.birthday_input = QLineEdit(self)
        self.birthday_input.setPlaceholderText("YYYY-MM-DD")
        layout.addRow("生年月日:", self.birthday_input)

        self.submit_button = QPushButton("確認", self)
        self.submit_button.clicked.connect(self.accept)
        layout.addRow(self.submit_button)

    def getBirthday(self):
        return self.birthday_input.text()

class ClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.birthday = None

    def initUI(self):
        layout = QVBoxLayout()

        # 経過時間表示用ラベル
        self.elapsed_time_label = QLabel("経過時間: ", self)
        self.elapsed_time_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.elapsed_time_label)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('経過時間計算アプリ')

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.get_user_birthday()
        self.show()

    def get_user_birthday(self):
        dialog = BirthdayInputDialog()
        if dialog.exec():
            self.birthday = QDateTime.fromString(dialog.getBirthday(), "yyyy-MM-dd")
            self.update_time()

    def update_time(self):
        if self.birthday:
            now = QDateTime.currentDateTime()
            elapsed = self.birthday.daysTo(now)
            seconds = self.birthday.secsTo(now) % (24 * 3600)
            self.elapsed_time_label.setText(f"経過時間: {elapsed} 日と {seconds // 3600} 時間 {seconds % 3600 // 60} 分 {seconds % 60} 秒")

def main():
    app = QApplication(sys.argv)
    ex = ClockApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
