from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb

class ChiBo(QWidget):

    db = conndb()

    def __init__(self):
        super().__init__()
        loadUi("ui/FormChiBo.ui", self)
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
        query = "SELECT * FROM chibo"
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
        self.tableData.setHorizontalHeaderLabels(['Mã Chi Bộ', 'Tên Chi Bộ', 'Ngày Thành Lập', 'Số Thành Viên'])

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
            maChiBo = self.tableData.item(selected_row, 0).text()
            tenChiBo = self.tableData.item(selected_row, 1).text()
            ngayThanhLap = self.tableData.item(selected_row, 2).text()
            soThanhVien = self.tableData.item(selected_row, 3).text()
            
            self.txtMaChiBo.setText(maChiBo)
            self.txtTenChiBo.setText(tenChiBo)
            ngayThanhLap = datetime.strptime(ngayThanhLap, "%Y-%m-%d")
            ngayThanhLap = ngayThanhLap.strftime("%d-%m-%Y")
            self.txtNgayThanhLap.setText(ngayThanhLap)
            self.txtTongSo.setText(soThanhVien) 

            self.txtMaChiBo.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)

    def add(self):
        if self.txtMaChiBo.text() == "" or self.txtTenChiBo.text() == "" or self.txtNgayThanhLap.text() == "" or self.txtTongSo.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin chi bộ!")
            return
        elif self.is_valid_date(self.txtNgayThanhLap.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày thành lập định dạng: dd-mm-YYYY!")
            return
        elif self.txtTongSo.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số thành viên phải nhập là kiểu số!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM chibo WHERE MaChiBo = '{self.txtMaChiBo.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã chi bộ đã tồn tại!")
                else:
                    ngayThanhLap = datetime.strptime(self.txtNgayThanhLap.text(), "%d-%m-%Y")
                    ngayThanhLap = ngayThanhLap.strftime("%Y-%m-%d")

                    query = f"INSERT INTO `chibo` (`MaChiBo`, `TenChiBo`, `NgayThanhLap`, `TongSo`) VALUES ('{self.txtMaChiBo.text()}', '{self.txtTenChiBo.text()}', '{ngayThanhLap}', '{self.txtTongSo.text()}');"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm chi bộ mới thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm chi bộ!")

    def update(self):
        if self.txtMaChiBo.text() == "" or self.txtTenChiBo.text() == "" or self.txtNgayThanhLap.text() == "" or self.txtTongSo.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin chi bộ!")
            return
        elif self.is_valid_date(self.txtNgayThanhLap.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày thành lập định dạng: dd-mm-YYYY!")
            return
        elif self.txtTongSo.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số thành viên phải nhập là kiểu số!")
            return
        else:
            try:
                ngayThanhLap = datetime.strptime(self.txtNgayThanhLap.text(), "%d-%m-%Y")
                ngayThanhLap = ngayThanhLap.strftime("%Y-%m-%d")
                query = f"UPDATE `chibo` SET `TenChiBo`='{self.txtTenChiBo.text()}',`NgayThanhLap`='{ngayThanhLap}',`TongSo`='{self.txtTongSo.text()}' WHERE `MaChiBo`='{self.txtMaChiBo.text()}'"
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật chi bộ thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật chi bộ!")
        
    def delete(self):
        if self.txtMaChiBo.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn chi bộ cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa chi bộ này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `chibo` WHERE `MaChiBo`='{self.txtMaChiBo.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa chi bộ thành công!")
                    self.getData()
                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa chi bộ!")

    def resetInput(self):
        self.txtMaChiBo.setText("")
        self.txtTenChiBo.setText("")
        self.txtNgayThanhLap.setText("")
        self.txtTongSo.setText("") 

        self.txtMaChiBo.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)
        x = reply.exec()
    
    def is_valid_date(self, date_str, format_str):
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False