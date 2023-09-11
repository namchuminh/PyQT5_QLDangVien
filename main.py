import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from src.Login import Login

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = Login()
        self.login.show()

        self.login.loginButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        if self.login.error != "":
            self.messageBoxInfo("Thông Báo", self.login.error)
        else:
            self.messageBoxInfo("Thông Báo", "Đăng Nhập Thành Công")
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())