import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDialog, QFormLayout, QDateEdit, QMessageBox
from PyQt6.QtCore import QTimer, QDateTime, QDate, QTime
from PyQt6.QtGui import QIcon

class BirthdayInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("生年月日入力")
        self.setFixedSize(500, 150)  # ウィンドウサイズを固定
        self.setGeometry(500, 500, 500, 150)  # ウィンドウの位置とサイズを設定
        layout = QFormLayout(self)

        self.birthday_input = QLineEdit(self)
        self.birthday_input.setPlaceholderText("YYYY-MM-DD")
        layout.addRow("生年月日:", self.birthday_input)

        self.target_age_input = QLineEdit(self)
        self.target_age_input.setPlaceholderText("目標年齢（例：90）")
        layout.addRow("目標年齢:", self.target_age_input)

        self.submit_button = QPushButton("確認", self)
        self.submit_button.clicked.connect(self.accept)
        layout.addRow(self.submit_button)

    def getBirthday(self):
        return self.birthday_input.text()

    def getTargetAge(self):
        return int(self.target_age_input.text())

class ClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.birthday = None  # 明示的に初期化
        self.target_age = 90  # Default target age
        self.initUI()

    def initUI(self):
        self.setWindowTitle('あなたの残り時間')
        self.setFixedSize(500, 250)  # ウィンドウサイズを固定
        self.setGeometry(500, 500, 500, 150)  # ウィンドウの位置とサイズを設定
        #self.setWindowIcon(QIcon('./figures/clock_icon.png'))  # アイコンファイルを指定（ファイルパスは環境に合わせて調整）

        layout = QVBoxLayout()

        self.time_until_ninety_label = QLabel("残り時間: 待機中...", self)
        self.time_until_ninety_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.time_until_ninety_label)

        self.total_months_label = QLabel("", self)
        self.total_months_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.total_months_label)

        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        self.get_user_birthday()
        self.show()

    def get_user_birthday(self):
        while True:
            dialog = BirthdayInputDialog()
            if dialog.exec():
                birthday_str = dialog.getBirthday()
                birthday_date = QDate.fromString(birthday_str, "yyyy-MM-dd")
                if birthday_date.isValid():
                    self.birthday = QDateTime(birthday_date, QTime(0, 0))
                    self.target_age = dialog.getTargetAge()
                    self.update_time()
                    break
                else:
                    QMessageBox.warning(self, "無効な日付", "入力された日付が無効です。正しい形式で再度入力してください。")
            else:
                break  # User cancelled the dialog

    def update_time(self):
        if self.birthday and self.birthday.isValid():
            now = QDateTime.currentDateTime()
            target_birthday = self.birthday.addYears(self.target_age)
            secs_left = now.secsTo(target_birthday)
            days_left = secs_left // 86400
            hours_left = (secs_left % 86400) // 3600
            minutes_left = (secs_left % 3600) // 60
            seconds_left = secs_left % 60

            years_left, months_left, days_left = self.calculate_date_difference(now.date(), target_birthday.date())
            total_months_left = years_left * 12 + months_left

            self.time_until_ninety_label.setText(f"あなたの残り時間: {years_left}年 {months_left}ヶ月 {days_left}日 {hours_left}時間 {minutes_left}分 {seconds_left}秒")
            self.total_months_label.setText(f"あなたの残り月数: {total_months_left} ヶ月") 

    def calculate_date_difference(self, start_date, end_date):
            years = end_date.year() - start_date.year()
            months = end_date.month() - start_date.month()
            days = end_date.day() - start_date.day()

            if days < 0:  # Adjust days and months
                months -= 1
                days += QDate(end_date.year(), end_date.month(), 1).daysInMonth()

            if months < 0:  # Adjust months and years
                years -= 1
                months += 12

            return years, months, days

    # def show(self):
    #         # Set the window to the mid of the screen
    #         screen_geometry = QApplication.primaryScreen().geometry()
    #         x = screen_geometry.width() / 2 - self.width()
    #         y = screen_geometry.height() / 2 - self.height()
    #         self.setGeometry(x, y, self.width(), self.height())
    #         super().show()

def main():
    app = QApplication(sys.argv)
    ex = ClockApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
