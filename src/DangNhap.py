from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import sys, hashlib
from database.connect import conndb


class DangNhap(QMainWindow):
    username = ""
    password = ""
    error = ""
    db = conndb()
    def __init__(self):
        super().__init__()
        loadUi("ui/FormDangNhap.ui", self)

        # Click loginButton
        self.loginButton.clicked.connect(self.login)

        # Click exitButton
        self.exitButton.clicked.connect(self.exitApplication)

    def login(self):
        self.username = self.txtTaiKhoan.text()
        self.password = self.txtMatKhau.text()

        # Kiểm tra thông tin đăng nhập
        if self.username == "" or self.password == "":
            self.error = "Vui lòng nhập đủ tài khoản mật khẩu!"
        
        try:
            hashed_password = hashlib.md5(self.password.encode('utf-8')).hexdigest()
            query = f"SELECT COUNT(*) FROM taikhoan WHERE TaiKhoan = '{self.username}' AND MatKhau = '{hashed_password}'"
            result = self.db.queryResult(query)

            if result[0][0] == 0:
                self.error = "Sai tài khoản hoặc mật khẩu!" 
            else:
                self.error = ""
        except:
            self.error = "Có lỗi khi đăng nhập!"

    def exitApplication(self):
        sys.exit()
        

