from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class ChucVuDang(QWidget):

    db = conndb()

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormChucVuDangVien.ui", self)
        # Để căn chỉnh cột theo chiều ngang
        self.user = user
        self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.tableData.itemSelectionChanged.connect(self.getSelectedRowData)
        self.buttonLamMoi.clicked.connect(self.resetInput)
        self.buttonThem.clicked.connect(self.add)
        self.buttonSua.clicked.connect(self.update)
        self.buttonXoa.clicked.connect(self.delete)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
        self.isGuest()
        self.getData()

    def isGuest(self):
        if self.user == "guest":
            self.buttonLamMoi.setEnabled(False)
            self.buttonThem.setEnabled(False)
            self.buttonSua.setEnabled(False)
            self.buttonXoa.setEnabled(False)

    def getData(self):
        query = "SELECT * FROM chucvudang"
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
        self.tableData.setHorizontalHeaderLabels(['Mã Chức Vụ Đảng', 'Tên Chức Vụ Đảng'])
        
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

            self.txtMaChucVu.setText(maChuVu)
            self.txtTenChucVu.setText(tenChucVu)

            self.txtMaChucVu.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)

        self.isGuest()

    def add(self):
        if self.txtMaChucVu.text() == "" or self.txtTenChucVu.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin chức vụ Đảng!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM chucvudang WHERE MaChucVu = '{self.txtMaChucVu.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã chức vụ Đảng đã tồn tại!")
                else:
                    query = f"INSERT INTO `chucvudang` (`MaChucVu`, `ChucVuDang`) VALUES ('{self.txtMaChucVu.text()}', '{self.txtTenChucVu.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm chức vụ Đảng thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm chức vụ Đảng!")

    def update(self):
        if self.txtMaChucVu.text() == "" or self.txtTenChucVu.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin chức vụ Đảng!")
            return
        else:
            try:
                query = f"UPDATE `chucvudang` SET `ChucVuDang`='{self.txtTenChucVu.text()}' WHERE `MaChucVu`='{self.txtMaChucVu.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật chức vụ Đảng thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật chức vụ Đảng!")
        
    def delete(self):
        if self.txtMaChucVu.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn chức vụ Đảng cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa chức vụ Đảng này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `chucvudang` WHERE `MaChucVu`='{self.txtMaChucVu.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa chức vụ Đảng thành công!")
                    self.getData()

                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa chức vụ Đảng!")

    def resetInput(self):
        self.txtMaChucVu.setText("")
        self.txtTenChucVu.setText("")

        self.txtMaChucVu.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()