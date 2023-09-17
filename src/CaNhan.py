from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from datetime import datetime

class CaNhan(QWidget):

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormCaNhan.ui", self)
        self.user = user
        self.lblMaTaiKhoan.setText(self.lblMaTaiKhoan.text() + " " + self.user[0][0])
        self.lblHoTen.setText(self.lblHoTen.text() + " " + self.user[0][1])

        ngaySinh = datetime.strptime(str(self.user[0][2]), "%Y-%m-%d")
        ngaySinh = ngaySinh.strftime("%d-%m-%Y")

        self.lblNgaySinh.setText(self.lblNgaySinh.text() + " " + ngaySinh)
        self.lblSoDienThoai.setText(self.lblSoDienThoai.text() + " " + self.user[0][3])
        self.lblMaDangNhap.setText(self.lblMaDangNhap.text() + " " + self.user[0][4])
        role = "Admin" if self.user[0][7] == 1 else "User"
        self.lblPhanQuyen.setText(self.lblPhanQuyen.text() + " " + role)
        self.lblDiaChi.setText(self.lblDiaChi.text() + " " + self.user[0][6])
