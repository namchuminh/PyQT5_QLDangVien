from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from .Profile import Profile
from .Wellcome import Wellcome
from .ChiBo import ChiBo
from .ChucVuDang import ChucVuDang
from .ChucVuChinhQuyen import ChucVuChinhQuyen
from .TrinhDoChuyenMon import TrinhDoChuyenMon
from .LyLuanChinhTri import LyLuanChinhTri
from .DanToc import DanToc
from .TonGiao import TonGiao
from .DangVien import DangVien

class Home(QMainWindow):

    def __init__(self, user):
        super().__init__()
        loadUi("ui/FormHeThong.ui", self)
        self.user = user
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.displayUi(DangVien())
        self.menu_hethong_canhan.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chibo.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chucvudangvien.triggered.connect(self.loadWidget)
        self.menu_danhmuc_chucvuchinhquyen.triggered.connect(self.loadWidget)
        self.menu_danhmuc_trinhdochuyenmon.triggered.connect(self.loadWidget)
        self.menu_chuyenmuc_trinhdolyluanchinhtri.triggered.connect(self.loadWidget)
        self.menu_chuyenmuc_dantoc.triggered.connect(self.loadWidget)
        self.menu_danhmuc_tongiao.triggered.connect(self.loadWidget)
        self.menu_dangvien.triggered.connect(self.loadWidget)


    def loadWidget(self):
        sender = self.sender()
        if sender == self.menu_hethong_canhan:
            self.displayUi(Profile(self.user))
        if sender == self.menu_danhmuc_chibo:
            self.displayUi(ChiBo())
        if sender == self.menu_danhmuc_chucvudangvien:
            self.displayUi(ChucVuDang())
        if sender == self.menu_danhmuc_chucvuchinhquyen:
            self.displayUi(ChucVuChinhQuyen())
        if sender == self.menu_danhmuc_trinhdochuyenmon:
            self.displayUi(TrinhDoChuyenMon())
        if sender == self.menu_chuyenmuc_trinhdolyluanchinhtri:
            self.displayUi(LyLuanChinhTri())
        if sender == self.menu_chuyenmuc_dantoc:
            self.displayUi(DanToc())
        if sender == self.menu_danhmuc_tongiao:
            self.displayUi(TonGiao())
        if sender == self.menu_dangvien:
            self.displayUi(DangVien())
        
    
    def displayUi(self, widget):
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
            