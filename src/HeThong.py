from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from .CaNhan import CaNhan
from .Wellcome import Wellcome
from .ChiBo import ChiBo
from .ChucVuDang import ChucVuDang
from .ChucVuChinhQuyen import ChucVuChinhQuyen
from .TrinhDoChuyenMon import TrinhDoChuyenMon
from .LyLuanChinhTri import LyLuanChinhTri
from .DanToc import DanToc
from .TonGiao import TonGiao
from .DangVien import DangVien
from .DoiMatKhau import DoiMatKhau

class HeThong(QMainWindow):

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormHeThong.ui", self)
        self.user = user
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.displayUi(DangVien(self.user))
        self.menu_hethong_canhan.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chibo.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chucvudangvien.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chucvuchinhquyen.triggered.connect(self.loadWidget)
        self.menu_danhmuc_trinhdochuyenmon.triggered.connect(self.loadWidget)
        self.menu_chuyenmuc_trinhdolyluanchinhtri.triggered.connect(self.loadWidget)
        self.menu_chuyenmuc_dantoc.triggered.connect(self.loadWidget)
        self.menu_danhmuc_tongiao.triggered.connect(self.loadWidget)
        self.menu_dangvien.triggered.connect(self.loadWidget)
        self.menu_hethong_doimatkhau.triggered.connect(self.loadWidget)

        if self.user == "guest":
            self.menu_hethong_canhan.setVisible(False)
            self.menu_hethong_doimatkhau.setVisible(False)
            self.menu_hethong_thoat.setText("Đăng Nhập")
        else:
            self.menu_hethong_canhan.setVisible(True)
            self.menu_hethong_doimatkhau.setVisible(True)
            self.menu_hethong_thoat.setText("Thoát")

    def loadWidget(self):
        sender = self.sender()
        if sender == self.menu_hethong_canhan:
            self.displayUi(CaNhan(self.user))
        if sender == self.menu_danhmuc_chibo:
            self.displayUi(ChiBo(self.user))
        if sender == self.menu_danhmuc_chucvudangvien:
            self.displayUi(ChucVuDang(self.user))
        if sender == self.menu_danhmuc_chucvuchinhquyen:
            self.displayUi(ChucVuChinhQuyen(self.user))
        if sender == self.menu_danhmuc_trinhdochuyenmon:
            self.displayUi(TrinhDoChuyenMon(self.user))
        if sender == self.menu_chuyenmuc_trinhdolyluanchinhtri:
            self.displayUi(LyLuanChinhTri(self.user))
        if sender == self.menu_chuyenmuc_dantoc:
            self.displayUi(DanToc(self.user))
        if sender == self.menu_danhmuc_tongiao:
            self.displayUi(TonGiao(self.user))
        if sender == self.menu_dangvien:
            self.displayUi(DangVien(self.user))
        if sender == self.menu_hethong_doimatkhau:
            self.displayUi(DoiMatKhau(self.user))
        
    
    def displayUi(self, widget):
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
            