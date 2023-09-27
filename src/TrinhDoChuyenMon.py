from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class TrinhDoChuyenMon(QWidget):

    db = conndb()

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormTrinhDoChuyenMon.ui", self)
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
        query = "SELECT * FROM trinhdo"
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
        self.tableData.setHorizontalHeaderLabels(['Mã Chức Trình Độ Chuyên Môn', 'Tên Trình Độ Chuyên Môn'])

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

            self.txtMaTrinhDo.setText(maChuVu)
            self.txtChuyenMon.setText(tenChucVu)

            self.txtMaTrinhDo.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)
        
        self.isGuest()

    def add(self):
        if self.txtMaTrinhDo.text() == "" or self.txtChuyenMon.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin trình độ chuyên môn!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM trinhdo WHERE MaTrinhDo = '{self.txtMaTrinhDo.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã trình độ chuyên môn đã tồn tại!")
                else:
                    query = f"INSERT INTO `trinhdo` (`MaTrinhDo`, `ChuyenMon`) VALUES ('{self.txtMaTrinhDo.text()}', '{self.txtChuyenMon.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm trình độ chuyên môn thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm trình độ chuyên môn!")

    def update(self):
        if self.txtMaTrinhDo.text() == "" or self.txtChuyenMon.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin trình độ chuyên môn!")
            return
        else:
            try:
                query = f"UPDATE `trinhdo` SET `ChuyenMon`='{self.txtChuyenMon.text()}' WHERE `MaTrinhDo`='{self.txtMaTrinhDo.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật trình độ chuyên môn thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật trình độ chuyên môn!")
        
    def delete(self):
        if self.txtMaTrinhDo.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn trình độ chuyên môn cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa trình độ chuyên môn này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `trinhdo` WHERE `MaTrinhDo`='{self.txtMaTrinhDo.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa trình độ chuyên môn thành công!")
                    self.getData()

                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa trình độ chuyên môn!")

    def resetInput(self):
        self.txtMaTrinhDo.setText("")
        self.txtChuyenMon.setText("")

        self.txtMaTrinhDo.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()