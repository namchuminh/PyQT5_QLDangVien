from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb
import hashlib

class DoiMatKhau(QWidget):

    db = conndb()

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormDoiMatKhau.ui", self)
        self.user = user
        self.getData()

        self.buttonThayDoi.clicked.connect(self.update)

    def getData(self):
        self.txtTaiKhoanDangNhap.setText(self.user[0][4])

    def update(self):
        if self.txtMatKhauHienTai.text() == "" or self.txtMatKhauMoi.text() == "" or self.txtXacNhanMatKhau.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin mật khẩu cũ và thông tin mật khẩu mới!")
            return
        else:
            try:
                hashed_password = hashlib.md5(self.txtMatKhauHienTai.text().encode('utf-8')).hexdigest()
                query = f"SELECT COUNT(*) FROM taikhoan WHERE TaiKhoan = '{self.user[0][4]}' AND MatKhau = '{hashed_password}'"
                result = self.db.queryResult(query)

                if result[0][0] == 0:
                    self.messageBoxInfo("Thông Báo", "Mật khẩu hiện tại không đúng!")
                    return
                else:
                    if self.txtMatKhauMoi.text() != self.txtXacNhanMatKhau.text():
                        self.messageBoxInfo("Thông Báo", "Mật khẩu xác nhận không trùng khớp!")
                        return
                
                try:
                    hashed_password = hashlib.md5(self.txtMatKhauMoi.text().encode('utf-8')).hexdigest()
                    query = f"UPDATE `taikhoan` SET `MatKhau`='{hashed_password}' WHERE `TaiKhoan`='{self.user[0][4]}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thay đổi mật khẩu thành công!")

                    self.txtMatKhauMoi.setText("")
                    self.txtXacNhanMatKhau.setText("")
                    self.txtMatKhauHienTai.setText("")
                except:
                    self.messageBoxInfo("Thông Báo", "Có lỗi khi thay đổi mật khẩu!")
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi kiểm tra mật khẩu hiện tại!")
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()