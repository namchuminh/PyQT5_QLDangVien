import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from src.Login import Login
from src.Home import Home

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = Login()
        self.home = Home()
        self.login.show()

        self.login.loginButton.clicked.connect(self.handleLogin)
        self.home.menu_hethong_thoat.triggered.connect(self.handleLogout)


    def handleLogin(self):
        if self.login.error != "":
            self.messageBoxInfo("Thông Báo", self.login.error)
        else:
            self.login.hide()
            self.home.show()

    def handleLogout(self):
        self.home.displayUi("FormTrangChu")
        self.home.hide()
        self.login.show()
    
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