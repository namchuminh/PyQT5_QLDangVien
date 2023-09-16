from datetime import datetime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.uic import loadUi
from database.connect import conndb
from datetime import date

class DangVien(QWidget):

    db = conndb()

    def __init__(self):
        super().__init__()
        loadUi("ui/FormDangVien.ui", self)
        # Để căn chỉnh cột theo chiều ngang
        # self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.tableData.itemSelectionChanged.connect(self.getSelectedRowData)
        self.buttonLamMoi.clicked.connect(self.resetInput)
        self.buttonThem.clicked.connect(self.add)
        self.buttonSua.clicked.connect(self.update)
        self.buttonXoa.clicked.connect(self.delete)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)

        self.getData()

    def getData(self):
        query = """
                SELECT dangvien.MaDangVien, dangvien.SoTheDang, dangvien.HoTen, dangvien.SoCCCD, dangvien.NgaySinh, dangvien.GioiTinh, dantoc.TenDanToc, tongiao.TenTonGiao,dangvien.QueQuan, dangvien.HoKhauThuongTru, dangvien.NoiSinh, dangvien.DiaChiHienTai, dangvien.NgayVaoDang, dangvien.NgayChinhThuc, dangvien.SoDienThoai, dangvien.Email, chibo.TenChiBo, chucvudang.ChucVuDang, chucvuchinhquyen.ChucVuChinhQuyen, lyluanchinhtri.TrinhDoChinhTri, trinhdo.ChuyenMon 
                FROM dangvien, chibo, chucvudang, chucvuchinhquyen, dantoc, lyluanchinhtri, tongiao, trinhdo 
                WHERE dangvien.MaChiBo = chibo.MaChiBo AND dangvien.MaDanToc = dantoc.MaDanToc AND dangvien.MaTonGiao = tongiao.MaTonGiao AND dangvien.MaChucVuChinhQuyen = chucvuchinhquyen.MaChucVu AND dangvien.MaChucVuDang = chucvudang.MaChucVu AND dangvien.MaTrinhDoLyLuanChinhTri = lyluanchinhtri.MaTrinhDo AND dangvien.MaTrinhDoChuyenMon = trinhdo.MaTrinhDo;
            """
        result = self.db.queryResult(query)
        self.showDataTable(result)
        self.showComboBox()

    def showComboBox(self):
        try:
            strsql = "SELECT * FROM chibo;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbTimCB.addItem(str(item[1]))
                    self.cbChiBo.addItem(str(item[1]))
            
            strsql = "SELECT * FROM chucvudang;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbChucVuDang.addItem(str(item[1]))
                    self.cbTimCVD.addItem(str(item[1]))
            
            strsql = "SELECT * FROM lyluanchinhtri;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbTrinhDoLLCT.addItem(str(item[1]))
                    self.cbTimLLCT.addItem(str(item[1]))
            
            strsql = "SELECT * FROM dantoc;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbDanToc.addItem(str(item[1]))
            
            strsql = "SELECT * FROM tongiao;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbTonGiao.addItem(str(item[1]))
            
            strsql = "SELECT * FROM chucvuchinhquyen;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbChucVuChinhQuyen.addItem(str(item[1]))

            strsql = "SELECT * FROM trinhdo;"
            result = self.db.queryResult(strsql)

            if len(result) > 0:
                for item in result:
                    self.cbChuyenMon.addItem(str(item[1]))
            
        except:
            self.messageBoxInfo("Thông Báo", "Có lỗi khi hiển thị thông tin đảng viên!")

    def showDataTable(self, data):

        if len(data) == 0:
            # Thiết lập số hàng và số cột cho bảng
            self.tableData.setRowCount(0)
            self.tableData.setColumnCount(0)
        else:
            # Thiết lập số hàng và số cột cho bảng
            self.tableData.setRowCount(len(data))
            self.tableData.setColumnCount(21)

        # Đặt tên cho các cột
        self.tableData.setHorizontalHeaderLabels(['Mã ĐV', 'Số Thẻ', 'Họ Tên', 'Số CCCD', 'Ngày Sinh', 'Giới Tính', 'Dân Tộc', 'Tôn Giáo', 'Quê Quán', 'Thường Trú', 'Nơi Sinh', 'Nơi Ở', 'Ngày Vào Đảng', 'Ngày Chính Thức', 'Số ĐT', 'Email', 'Chi Bộ', 'Chức Vụ Đảng', 'Chức Vụ CQ', 'Trình Độ LLCT', 'Chuyên Môn'])

        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                if type(value) == date:
                    value = value.strftime("%d-%m-%Y")
                item = QTableWidgetItem(str(value))
                self.tableData.setItem(row, col, item)
    
    def getSelectedRowData(self):
        selected_row = self.tableData.currentRow()
        if selected_row != -1:
            self.txtMaDangVien.setText(self.tableData.item(selected_row, 0).text())
            self.txtSoTheDangVien.setText(self.tableData.item(selected_row, 1).text())
            self.txtHoTen.setText(self.tableData.item(selected_row, 2).text())
            self.txtSoCCCD.setText(self.tableData.item(selected_row, 3).text())
            self.txtNgaySinh.setText(self.tableData.item(selected_row, 4).text())

            if(self.tableData.item(selected_row, 5).text() == "Nam"):
                self.radioNam.setChecked(True)
                self.radioNu.setChecked(False)
            else:
                self.radioNam.setChecked(False)
                self.radioNu.setChecked(True)
            
            self.cbDanToc.setCurrentText(self.tableData.item(selected_row, 6).text())
            self.cbTonGiao.setCurrentText(self.tableData.item(selected_row, 7).text())

            self.txtQueQuan.setText(self.tableData.item(selected_row, 8).text())
            self.txtThuongTru.setText(self.tableData.item(selected_row, 9).text())
            self.txtNoiSinh.setText(self.tableData.item(selected_row, 10).text())
            self.txtNoiOHienTai.setText(self.tableData.item(selected_row, 11).text())
            self.txtNgayVaoDang.setText(self.tableData.item(selected_row, 12).text())
            self.txtNgayChinhThuc.setText(self.tableData.item(selected_row, 13).text())
            self.txtSoDienThoai.setText(self.tableData.item(selected_row, 14).text())
            self.txtEmail.setText(self.tableData.item(selected_row, 15).text())

            self.cbChiBo.setCurrentText(self.tableData.item(selected_row, 16).text())
            self.cbChucVuDang.setCurrentText(self.tableData.item(selected_row, 17).text())
            self.cbChucVuChinhQuyen.setCurrentText(self.tableData.item(selected_row, 18).text())
            self.cbTrinhDoLLCT.setCurrentText(self.tableData.item(selected_row, 19).text())
            self.cbChuyenMon.setCurrentText(self.tableData.item(selected_row, 20).text())


            self.txtMaDangVien.setDisabled(True)
            self.buttonThem.setDisabled(True)

            self.buttonSua.setEnabled(True)
            self.buttonXoa.setEnabled(True)

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