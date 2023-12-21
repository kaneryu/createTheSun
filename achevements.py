from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import os
from time import time

import gamedefine

basedir = os.path.dirname(os.path.realpath(__file__))
mediadir = os.path.join(basedir, "assets/")

class achevementPopup(QWidget):
    def __init__(self, achevement : str, window : QMainWindow, open : bool = False):
        super().__init__()
        self.setWindowTitle("Test")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, 200, 200)
        self.adjustSize()  # Ensure size hint is updated
        self.fadein = QPropertyAnimation(self, b"windowOpacity")
        self.fadein.setDuration(200)
        self.fadein.setStartValue(0)
        self.fadein.setEndValue(1)
        screen_geometry = window.geometry()
        self.move(screen_geometry.bottomRight())
        
        self.content = achevementWidget(achevement)
        self.achevementGet = QLabel("You got an achevement!")
        self.achevementGet.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.achevementGet.setFont(QFont("Arial", 20))
        layout = QVBoxLayout()
        layout.addWidget(self.content)
        self.setLayout(layout)
        
        self.fadeout = QPropertyAnimation(self, b"windowOpacity")
        self.fadeout.setDuration(200)
        self.fadeout.setStartValue(1)
        self.fadeout.setEndValue(0)
        self.fadeout.finished.connect(self.close)
        
        if open:
            self.show()
            self.fadein.start()
            ticktime = time()
            while time() - ticktime < 5:
                QApplication.processEvents()
            self.fadeout.start()
            

       
    
class achevementWidget(QWidget):
    def __init__(self, achevement : str):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.image = QLabel()
        self.image.setPixmap(QPixmap(os.path.join(mediadir, "images/", "achevements/", achevement + ".png")))
        self.layout.addWidget(self.image)

        self.text = QLabel(gamedefine.achevementVisualDefine[achevement]["visualName"] + "\n" + gamedefine.achevementVisualDefine[achevement]["hoverDescription"])
        
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)