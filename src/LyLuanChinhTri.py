from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class LyLuanChinhTri(QWidget):

    db = conndb()

    def __init__(self):
        super().__init__()
        loadUi("ui/FormLyLuanChinhTri.ui", self)
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
        query = "SELECT * FROM lyluanchinhtri"
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
        self.tableData.setHorizontalHeaderLabels(['Mã Trình Độ Lý Luận Chính Trị', 'Tên Trình Độ Chính Trị'])

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

            self.txtMaTrinhDo.setText(maChuVu)
            self.txtLLCT.setText(tenChucVu)

            self.txtMaTrinhDo.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)

    def add(self):
        if self.txtMaTrinhDo.text() == "" or self.txtLLCT.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin trình độ LLCT!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM lyluanchinhtri WHERE MaTrinhDo = '{self.txtMaTrinhDo.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã trình độ LLCT đã tồn tại!")
                else:
                    query = f"INSERT INTO `lyluanchinhtri` (`MaTrinhDo`, `TrinhDoChinhTri`) VALUES ('{self.txtMaTrinhDo.text()}', '{self.txtLLCT.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm trình độ LLCT thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm trình độ LLCT!")

    def update(self):
        if self.txtMaTrinhDo.text() == "" or self.txtLLCT.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin trình độ LLCT!")
            return
        else:
            try:
                query = f"UPDATE `lyluanchinhtri` SET `TrinhDoChinhTri`='{self.txtLLCT.text()}' WHERE `MaTrinhDo`='{self.txtMaTrinhDo.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật trình độ LLCT thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật trình độ LLCT!")
        
    def delete(self):
        if self.txtMaTrinhDo.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn trình độ LLCT cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa trình độ LLCT này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `lyluanchinhtri` WHERE `MaTrinhDo`='{self.txtMaTrinhDo.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa trình độ LLCT thành công!")
                    self.getData()

                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa trình độ LLCT!")

    def resetInput(self):
        self.txtMaTrinhDo.setText("")
        self.txtLLCT.setText("")

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