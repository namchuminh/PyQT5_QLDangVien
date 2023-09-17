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
        self.buttonTimKiem.clicked.connect(self.search)


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
            self.cbTimCB.clear()
            self.cbChiBo.clear()
            if len(result) > 0:
                for item in result:
                    self.cbTimCB.addItem(str(item[1]), userData=str(item[0]))
                    self.cbChiBo.addItem(str(item[1]), userData=str(item[0]))
            
            strsql = "SELECT * FROM chucvudang;"
            result = self.db.queryResult(strsql)
            self.cbChucVuDang.clear()
            self.cbTimCVD.clear()
            if len(result) > 0:
                for item in result:
                    self.cbChucVuDang.addItem(str(item[1]), userData=str(item[0]))
                    self.cbTimCVD.addItem(str(item[1]), userData=str(item[0]))
            
            strsql = "SELECT * FROM lyluanchinhtri;"
            result = self.db.queryResult(strsql)
            self.cbTrinhDoLLCT.clear()
            self.cbTimLLCT.clear()
            if len(result) > 0:
                for item in result:
                    self.cbTrinhDoLLCT.addItem(str(item[1]), userData=str(item[0]))
                    self.cbTimLLCT.addItem(str(item[1]), userData=str(item[0]))
            
            strsql = "SELECT * FROM dantoc;"
            result = self.db.queryResult(strsql)
            self.cbDanToc.clear()
            if len(result) > 0:
                for item in result:
                    self.cbDanToc.addItem(str(item[1]), userData=str(item[0]))
            
            strsql = "SELECT * FROM tongiao;"
            result = self.db.queryResult(strsql)
            self.cbTonGiao.clear()
            if len(result) > 0:
                for item in result:
                    self.cbTonGiao.addItem(str(item[1]), userData=str(item[0]))
            
            strsql = "SELECT * FROM chucvuchinhquyen;"
            result = self.db.queryResult(strsql)
            self.cbChucVuChinhQuyen.clear()
            if len(result) > 0:
                for item in result:
                    self.cbChucVuChinhQuyen.addItem(str(item[1]), userData=str(item[0]))

            strsql = "SELECT * FROM trinhdo;"
            result = self.db.queryResult(strsql)
            self.cbChuyenMon.clear()
            if len(result) > 0:
                for item in result:
                    self.cbChuyenMon.addItem(str(item[1]), userData=str(item[0]))
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
        self.tableData.setHorizontalHeaderLabels(['Mã ĐV', 'Số Thẻ', 'Họ Tên', 'Số CCCD', 'Ngày Sinh', 'Giới Tính', 'Dân Tộc', 'Đảng viên', 'Quê Quán', 'Thường Trú', 'Nơi Sinh', 'Nơi Ở', 'Ngày Vào Đảng', 'Ngày Chính Thức', 'Số ĐT', 'Email', 'Chi Bộ', 'Chức Vụ Đảng', 'Chức Vụ CQ', 'Trình Độ LLCT', 'Chuyên Môn'])

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
        if self.txtMaDangVien.text() == "" or self.txtSoTheDangVien.text() == "" or self.txtHoTen.text() == "" or self.txtSoCCCD.text() == "" or self.txtNgaySinh.text() == "" or self.txtQueQuan.text() == "" or self.txtThuongTru.text() == "" or self.txtNoiOHienTai.text() == "" or self.txtNgayVaoDang.text() == "" or self.txtNgayChinhThuc.text() == "" or self.txtSoDienThoai.text() == "" or self.txtEmail.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin Đảng viên!")
            return
        elif self.txtSoTheDangVien.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số thẻ Đảng viên phải nhập là kiểu số!")
            return
        elif self.is_valid_date(self.txtNgaySinh.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày sinh Đảng viên định dạng: dd-mm-YYYY!")
            return
        elif self.radioNu.isChecked() == False and self.radioNam.isChecked() == False:
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn giới tính Đảng viên!")
            return
        elif self.txtSoCCCD.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số điện thoại của Đảng viên phải nhập là kiểu số!")
            return
        elif self.txtSoDienThoai.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số điện thoại của Đảng viên phải nhập là kiểu số!")
            return
        elif self.is_valid_date(self.txtNgayVaoDang.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày vào Đảng định dạng: dd-mm-YYYY!")
            return
        elif self.is_valid_date(self.txtNgayChinhThuc.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày chính thức vào Đảng định dạng: dd-mm-YYYY!")
            return
        else:
            try:
                query = f"SELECT COUNT(*) FROM dangvien WHERE MaDangVien = '{self.txtMaDangVien.text()}'"
                if self.db.queryResult(query)[0][0] >= 1:
                    self.messageBoxInfo("Thông Báo", "Mã Đảng viên đã tồn tại!")
                else:
                    maTrinhDoLLCT = self.cbTrinhDoLLCT.itemData(self.cbTrinhDoLLCT.currentIndex())
                    danToc = self.cbDanToc.itemData(self.cbDanToc.currentIndex())
                    tonGiao = self.cbTonGiao.itemData(self.cbTonGiao.currentIndex())
                    chiBo = self.cbChiBo.itemData(self.cbChiBo.currentIndex())
                    chucVuDang = self.cbChucVuDang.itemData(self.cbChucVuDang.currentIndex())
                    chucVuChinhQuyen = self.cbChucVuChinhQuyen.itemData(self.cbChucVuChinhQuyen.currentIndex())
                    chuyenMon = self.cbChuyenMon.itemData(self.cbChuyenMon.currentIndex())
                    gioiTinh = "Nam"
                    if self.radioNu.isChecked():
                        gioiTinh = "Nữ"

                    ngaySinh = datetime.strptime(self.txtNgaySinh.text(), "%d-%m-%Y")
                    ngaySinh = ngaySinh.strftime("%Y-%m-%d")

                    
                    ngayVaoDang = datetime.strptime(self.txtNgayVaoDang.text(), "%d-%m-%Y")
                    ngayVaoDang = ngayVaoDang.strftime("%Y-%m-%d")

                    ngayChinhThuc = datetime.strptime(self.txtNgayChinhThuc.text(), "%d-%m-%Y")
                    ngayChinhThuc = ngayChinhThuc.strftime("%Y-%m-%d")


                    query = f"""
                                INSERT INTO `dangvien`(`MaDangVien`, `SoTheDang`, `MaChiBo`, `HoTen`, `GioiTinh`, `MaDanToc`, `MaTonGiao`, `NgaySinh`, `NoiSinh`, `QueQuan`, `HoKhauThuongTru`, `DiaChiHienTai`, `MaChucVuChinhQuyen`, `MaChucVuDang`, `NgayVaoDang`, `NgayChinhThuc`, `SoCCCD`, `SoDienThoai`, `Email`, `MaTrinhDoLyLuanChinhTri`, `MaTrinhDoChuyenMon`) 
                                VALUES ('{self.txtMaDangVien.text()}','{self.txtSoTheDangVien.text()}','{chiBo}','{self.txtHoTen.text()}','{gioiTinh}','{danToc}','{tonGiao}','{ngaySinh}','{self.txtNoiSinh.text()}','{self.txtQueQuan.text()}','{self.txtThuongTru.text()}','{self.txtNoiOHienTai.text()}','{chucVuChinhQuyen}','{chucVuDang}','{ngayVaoDang}','{ngayChinhThuc}','{self.txtSoCCCD.text()}','{self.txtSoDienThoai.text()}','{self.txtEmail.text()}','{maTrinhDoLLCT}','{chuyenMon}')
                            """
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Thêm Đảng viên thành công!")
                    self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi thêm Đảng viên!")

    def update(self):
        if self.txtMaDangVien.text() == "" or self.txtSoTheDangVien.text() == "" or self.txtHoTen.text() == "" or self.txtSoCCCD.text() == "" or self.txtNgaySinh.text() == "" or self.txtQueQuan.text() == "" or self.txtThuongTru.text() == "" or self.txtNoiOHienTai.text() == "" or self.txtNgayVaoDang.text() == "" or self.txtNgayChinhThuc.text() == "" or self.txtSoDienThoai.text() == "" or self.txtEmail.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đủ thông tin Đảng viên!")
            return
        elif self.txtSoTheDangVien.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số thẻ Đảng viên phải nhập là kiểu số!")
            return
        elif self.is_valid_date(self.txtNgaySinh.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày sinh Đảng viên định dạng: dd-mm-YYYY!")
            return
        elif self.radioNu.isChecked() == False and self.radioNam.isChecked() == False:
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn giới tính Đảng viên!")
            return
        elif self.txtSoCCCD.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số điện thoại của Đảng viên phải nhập là kiểu số!")
            return
        elif self.txtSoDienThoai.text().isdigit() == False:
            self.messageBoxInfo("Thông Báo", "Số điện thoại của Đảng viên phải nhập là kiểu số!")
            return
        elif self.is_valid_date(self.txtNgayVaoDang.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày vào Đảng định dạng: dd-mm-YYYY!")
            return
        elif self.is_valid_date(self.txtNgayChinhThuc.text(),f"%d-%m-%Y") == False:
            self.messageBoxInfo("Thông Báo", "Ngày chính thức vào Đảng định dạng: dd-mm-YYYY!")
            return
        else:
            try:
                maTrinhDoLLCT = self.cbTrinhDoLLCT.itemData(self.cbTrinhDoLLCT.currentIndex())
                danToc = self.cbDanToc.itemData(self.cbDanToc.currentIndex())
                tonGiao = self.cbTonGiao.itemData(self.cbTonGiao.currentIndex())
                chiBo = self.cbChiBo.itemData(self.cbChiBo.currentIndex())
                chucVuDang = self.cbChucVuDang.itemData(self.cbChucVuDang.currentIndex())
                chucVuChinhQuyen = self.cbChucVuChinhQuyen.itemData(self.cbChucVuChinhQuyen.currentIndex())
                chuyenMon = self.cbChuyenMon.itemData(self.cbChuyenMon.currentIndex())
                gioiTinh = "Nam"
                if self.radioNu.isChecked():
                    gioiTinh = "Nữ"

                ngaySinh = datetime.strptime(self.txtNgaySinh.text(), "%d-%m-%Y")
                ngaySinh = ngaySinh.strftime("%Y-%m-%d")
                
                ngayVaoDang = datetime.strptime(self.txtNgayVaoDang.text(), "%d-%m-%Y")
                ngayVaoDang = ngayVaoDang.strftime("%Y-%m-%d")

                ngayChinhThuc = datetime.strptime(self.txtNgayChinhThuc.text(), "%d-%m-%Y")
                ngayChinhThuc = ngayChinhThuc.strftime("%Y-%m-%d")

                query = f"""
                    UPDATE `dangvien` SET 
                    `SoTheDang`='{self.txtSoTheDangVien.text()}',`MaChiBo`='{chiBo}',`HoTen`='{self.txtHoTen.text()}',`GioiTinh`='{gioiTinh}',`MaDanToc`='{danToc}',`MaTonGiao`='{tonGiao}',`NgaySinh`='{ngaySinh}',`NoiSinh`='{self.txtNoiSinh.text()}',`QueQuan`='{self.txtQueQuan.text()}',`HoKhauThuongTru`='{self.txtThuongTru.text()}',`DiaChiHienTai`='{self.txtNoiOHienTai.text()}',`MaChucVuChinhQuyen`='{chucVuChinhQuyen}',`MaChucVuDang`='{chucVuDang}',`NgayVaoDang`='{ngayVaoDang}',`NgayChinhThuc`='{ngayChinhThuc}',`SoCCCD`='{self.txtSoCCCD.text()}',`SoDienThoai`='{self.txtSoDienThoai.text()}',`Email`='{self.txtEmail.text()}',`MaTrinhDoLyLuanChinhTri`='{maTrinhDoLLCT}',`MaTrinhDoChuyenMon`='{chuyenMon}' 
                    WHERE `MaDangVien`='{self.txtMaDangVien.text()}'
                """
                self.db.queryExecute(query)
                self.messageBoxInfo("Thông Báo", "Cập nhật Đảng viên thành công!")
                self.getData()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi cập nhật Đảng viên!")
        
    def delete(self):
        if self.txtMaDangVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn Đảng viên cần xóa!")
            return
        else:
            try:
                reply = QMessageBox.question(None, "Xác nhận", "Bạn có muốn xóa Đảng viên này không?", QMessageBox.Yes | QMessageBox.No)
                # Kiểm tra phản hồi từ hộp thoại
                if reply == QMessageBox.Yes:
                    query = f"DELETE FROM `dangvien` WHERE `MaDangVien`='{self.txtMaDangVien.text()}'"
                    self.db.queryExecute(query)
                    self.messageBoxInfo("Thông Báo", "Xóa Đảng viên thành công!")
                    self.getData()
                    self.resetInput()
            except:
                self.messageBoxInfo("Thông Báo", "Có lỗi khi xóa Đảng viên!")

    def search(self):
        query = """
            SELECT dangvien.MaDangVien, dangvien.SoTheDang, dangvien.HoTen, dangvien.SoCCCD, dangvien.NgaySinh, dangvien.GioiTinh, dantoc.TenDanToc, tongiao.TenTonGiao,dangvien.QueQuan, dangvien.HoKhauThuongTru, dangvien.NoiSinh, dangvien.DiaChiHienTai, dangvien.NgayVaoDang, dangvien.NgayChinhThuc, dangvien.SoDienThoai, dangvien.Email, chibo.TenChiBo, chucvudang.ChucVuDang, chucvuchinhquyen.ChucVuChinhQuyen, lyluanchinhtri.TrinhDoChinhTri, trinhdo.ChuyenMon 
            FROM dangvien, chibo, chucvudang, chucvuchinhquyen, dantoc, lyluanchinhtri, tongiao, trinhdo 
            WHERE dangvien.MaChiBo = chibo.MaChiBo AND dangvien.MaDanToc = dantoc.MaDanToc AND dangvien.MaTonGiao = tongiao.MaTonGiao AND dangvien.MaChucVuChinhQuyen = chucvuchinhquyen.MaChucVu AND dangvien.MaChucVuDang = chucvudang.MaChucVu AND dangvien.MaTrinhDoLyLuanChinhTri = lyluanchinhtri.MaTrinhDo AND dangvien.MaTrinhDoChuyenMon = trinhdo.MaTrinhDo;
        """
        if self.txtTimCCCD.text() != "":
            query = f"""
                SELECT dangvien.MaDangVien, dangvien.SoTheDang, dangvien.HoTen, dangvien.SoCCCD, dangvien.NgaySinh, dangvien.GioiTinh, dantoc.TenDanToc, tongiao.TenTonGiao,dangvien.QueQuan, dangvien.HoKhauThuongTru, dangvien.NoiSinh, dangvien.DiaChiHienTai, dangvien.NgayVaoDang, dangvien.NgayChinhThuc, dangvien.SoDienThoai, dangvien.Email, chibo.TenChiBo, chucvudang.ChucVuDang, chucvuchinhquyen.ChucVuChinhQuyen, lyluanchinhtri.TrinhDoChinhTri, trinhdo.ChuyenMon 
                FROM dangvien, chibo, chucvudang, chucvuchinhquyen, dantoc, lyluanchinhtri, tongiao, trinhdo 
                WHERE dangvien.MaChiBo = chibo.MaChiBo AND dangvien.MaDanToc = dantoc.MaDanToc AND dangvien.MaTonGiao = tongiao.MaTonGiao AND dangvien.MaChucVuChinhQuyen = chucvuchinhquyen.MaChucVu AND dangvien.MaChucVuDang = chucvudang.MaChucVu AND dangvien.MaTrinhDoLyLuanChinhTri = lyluanchinhtri.MaTrinhDo AND dangvien.MaTrinhDoChuyenMon = trinhdo.MaTrinhDo AND dangvien.SoCCCD LIKE '%{self.txtTimCCCD.text()}%'
            """
        else:
            maTrinhDoLLCT = self.cbTimLLCT.itemData(self.cbTimLLCT.currentIndex())
            maChucVuDang = self.cbTimCVD.itemData(self.cbTimCVD.currentIndex())
            maChiBo = self.cbTimCB.itemData(self.cbTimCB.currentIndex())

            query = f"""
                SELECT dangvien.MaDangVien, dangvien.SoTheDang, dangvien.HoTen, dangvien.SoCCCD, dangvien.NgaySinh, dangvien.GioiTinh, dantoc.TenDanToc, tongiao.TenTonGiao,dangvien.QueQuan, dangvien.HoKhauThuongTru, dangvien.NoiSinh, dangvien.DiaChiHienTai, dangvien.NgayVaoDang, dangvien.NgayChinhThuc, dangvien.SoDienThoai, dangvien.Email, chibo.TenChiBo, chucvudang.ChucVuDang, chucvuchinhquyen.ChucVuChinhQuyen, lyluanchinhtri.TrinhDoChinhTri, trinhdo.ChuyenMon 
                FROM dangvien, chibo, chucvudang, chucvuchinhquyen, dantoc, lyluanchinhtri, tongiao, trinhdo 
                WHERE dangvien.MaChiBo = chibo.MaChiBo AND dangvien.MaDanToc = dantoc.MaDanToc AND dangvien.MaTonGiao = tongiao.MaTonGiao AND dangvien.MaChucVuChinhQuyen = chucvuchinhquyen.MaChucVu AND dangvien.MaChucVuDang = chucvudang.MaChucVu AND dangvien.MaTrinhDoLyLuanChinhTri = lyluanchinhtri.MaTrinhDo AND dangvien.MaTrinhDoChuyenMon = trinhdo.MaTrinhDo AND (dangvien.MaChiBo = '{maChiBo}' OR dangvien.MaChucVuDang = '{maChucVuDang}' OR dangvien.MaTrinhDoLyLuanChinhTri = '{maTrinhDoLLCT}') 
            """

        result = self.db.queryResult(query)

        if len(result) <= 0:
            self.messageBoxInfo("Thông Báo", "Không tìm thấy Đảng viên nào!")
            self.getData()
            return
        else:
            self.showDataTable(result)

    def resetInput(self):
        self.txtMaDangVien.setText("")
        self.txtSoTheDangVien.setText("")
        self.txtHoTen.setText("")
        self.txtSoCCCD.setText("")
        self.txtNgaySinh.setText("")
        self.radioNam.setChecked(False)
        self.radioNu.setChecked(False)
        self.txtQueQuan.setText("")
        self.txtThuongTru.setText("")
        self.txtNoiSinh.setText("")
        self.txtNoiOHienTai.setText("")
        self.txtNgayVaoDang.setText("")
        self.txtNgayChinhThuc.setText("")
        self.txtSoDienThoai.setText("")
        self.txtEmail.setText("")

        self.txtMaDangVien.setEnabled(True)
        self.buttonThem.setEnabled(True)

        self.buttonSua.setDisabled(True)
        self.buttonXoa.setDisabled(True)

        self.getData()


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