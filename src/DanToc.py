from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class DanToc(QWidget):

    db = conndb()

    def __init__(self):
        super().__init__()
        loadUi("ui/FormDanToc.ui", self)
        # Để căn chỉnh cột theo chiều ngang
        self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.tableData.itemSelectionChanged.connect(self.getSelectedRowData)
        self.buttonLamMoi.clicked.connect(self.resetInput)
        self.buttonThem.clicked.connect(self.add)
        self.buttonSua.clicked.connect(self.update)
        self.buttonXoa.clicked.connect(self.delete)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)

        self.getData()

    def getData(self):
        query = "SELECT * FROM dantoc"
        result = self.db.queryResult(query)
        self.showDataTable(result)

    def showDataTable(self, data):

        if len(data) == 0:
            # Thiết lập số hàng và số cột cho bảng
            self.tableData.setRowCount(0)
            self.tableData.setColumnCount(0)
        else:
            # Thiết lập số hàng và số cột cho bảng
            self.tableData.setRowCount(len(data))
            self.tableData.setColumnCount(len(data[0]))

        # Đặt tên cho các cột
        self.tableData.setHorizontalHeaderLabels(['Mã Dân Tộc', 'Tên Dân Tộc'])

        # Thiết lập stylesheet cho header
        header = self.tableData.horizontalHeader()
        header.setStyleSheet("border: 1px solid #dedfe0;")
        

        # Thêm dữ liệu vào bảng
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.tableData.setItem(row, col, item)
    
    def getSelectedRowData(self):
        selected_row = self.tableData.currentRow()
        if selected_row != -1:
            maChuVu = self.tableData.item(selected_row, 0).text()
            tenChucVu = self.tableData.item(selected_row, 1).text()

            self.txtMaDanToc.setText(maChuVu)
            self.txtTenDanToc.setText(tenChucVu)

            self.txtMaDanToc.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)

    def add(self):
        if self.txtMaDanToc.text() == "" or self.txtTenDanToc.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin dân tộc!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM dantoc WHERE MaDanToc = '{self.txtMaDanToc.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã dân tộc đã tồn tại!")
                else:
                    query = f"INSERT INTO `dantoc` (`MaDanToc`, `TenDanToc`) VALUES ('{self.txtMaDanToc.text()}', '{self.txtTenDanToc.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm dân tộc thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm dân tộc!")

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
        
    def delete(self):
        if self.txtMaDanToc.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn dân tộc cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa dân tộc này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `dantoc` WHERE `MaDanToc`='{self.txtMaDanToc.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa dân tộc thành công!")
                    self.getData()

                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa dân tộc!")

    def resetInput(self):
        self.txtMaDanToc.setText("")
        self.txtTenDanToc.setText("")

        self.txtMaDanToc.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()