from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class TonGiao(QWidget):

    db = conndb()

    def __init__(self,user):
        super().__init__()
        loadUi("ui/FormTonGiao.ui", self)
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
        query = "SELECT * FROM tongiao"
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
        self.tableData.setHorizontalHeaderLabels(['Mã Tôn Giáo', 'Tên Tôn Giáo'])

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

            self.txtMaTonGiao.setText(maChuVu)
            self.txtTenTonGiao.setText(tenChucVu)

            self.txtMaTonGiao.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)
        self.isGuest()
        
    def add(self):
        if self.txtMaTonGiao.text() == "" or self.txtTenTonGiao.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin tôn giáo!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM tongiao WHERE MaTonGiao = '{self.txtMaTonGiao.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã tôn giáo đã tồn tại!")
                else:
                    query = f"INSERT INTO `tongiao` (`MaTonGiao`, `TenTonGiao`) VALUES ('{self.txtMaTonGiao.text()}', '{self.txtTenTonGiao.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm tôn giáo thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm tôn giáo!")

    def update(self):
        if self.txtMaTonGiao.text() == "" or self.txtTenTonGiao.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin tôn giáo!")
            return
        else:
            try:
                query = f"UPDATE `tongiao` SET `TenTonGiao`='{self.txtTenTonGiao.text()}' WHERE `MaTonGiao`='{self.txtMaTonGiao.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật tôn giáo thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật tôn giáo!")
        
    def delete(self):
        if self.txtMaTonGiao.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn tôn giáo cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa tôn giáo này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `tongiao` WHERE `MaTonGiao`='{self.txtMaTonGiao.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa tôn giáo thành công!")
                    self.getData()

                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa tôn giáo!")

    def resetInput(self):
        self.txtMaTonGiao.setText("")
        self.txtTenTonGiao.setText("")

        self.txtMaTonGiao.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()