from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class Wellcome(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("ui/FormTrangChu.ui", self)
