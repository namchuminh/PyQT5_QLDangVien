from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class DoiMatKhau(QWidget):

    db = conndb()

    def __init__(self):
        super().__init__()
        loadUi("ui/FormDoiMatKhau.ui", self)

        self.getData()

    def getData(self):
        pass

    def update(self):
        if self.txtMaDanToc.text() == "" or self.txtTenDanToc.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin dân tộc!")
            return
        else:
            try:
                query = f"UPDATE `dantoc` SET `TenDanToc`='{self.txtTenDanToc.text()}' WHERE `MaDanToc`='{self.txtMaDanToc.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật dân tộc thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật dân tộc!")
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()