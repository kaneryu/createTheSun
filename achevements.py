from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import main

class achevementPopup(QMessageBox):
    def __init__(self, achevement : str, window : QMainWindow, open : bool = False):
        super().__init__()
        self.setWindowTitle("Test")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.adjustSize()  # Ensure size hint is updated
        
        screen_geometry = window.geometry()
        self.move(screen_geometry.bottomRight())
        
        if open:
            self.open()
       
    
class achevementWidget(QWidget):
    pass

