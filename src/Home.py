from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QAction
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

class Home(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("ui/FormHeThong.ui", self)
        
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.loadWidget()
        
        self.menu_hethong_canhan.triggered.connect(self.loadWidget)

    def loadWidget(self):
        sender = self.sender()
        if sender == self.menu_hethong_canhan:
            self.displayUi("FormCaNhan")
        else:
            self.displayUi("FormTrangChu")
    
    def displayUi(self, formName):
        widget = QWidget()
        loadUi(f"ui/{formName}.ui", widget)

        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)
            