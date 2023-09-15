import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from src.Login import Login
from src.Home import Home
from src.DangVien import DangVien
from database.connect import conndb

class Main(QMainWindow):

    db = conndb()
    user = []

    def __init__(self):
        super().__init__()
        self.login = Login()
        self.login.show()
        self.home = Home(self.user)
        self.home.menu_hethong_thoat.triggered.connect(self.handleLogout)
        self.login.loginButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        if self.login.error != "":
            self.messageBoxInfo("Thông Báo", self.login.error)
        else:
            try:
                query = f"SELECT * FROM taikhoan WHERE TaiKhoan = '{self.login.username}'"
                self.updateUser(query)
                self.login.hide()
                self.home.show()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi đăng nhập!")

    def handleLogout(self):
        self.home.displayUi(DangVien())
        self.home.hide()
        self.login.show()

    def updateUser(self, query):
        self.user = self.db.queryResult(query)
        self.home = Home(self.user)
        self.home.menu_hethong_thoat.triggered.connect(self.handleLogout)

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