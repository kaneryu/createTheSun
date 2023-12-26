from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import QPropertyAnimation, Qt, QTimer

import os
from time import time

import gamedefine

basedir = os.path.dirname(os.path.realpath(__file__))
mediadir = os.path.join(basedir, "assets/")

class achevementPopup(QWidget):
    def __init__(self, achevement : str, open : bool = False):
        super().__init__()
        self.setWindowTitle("Test")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setGeometry(0, 0, 200, 200)
        self.adjustSize()  # Ensure size hint is updated
        self.fadein = QPropertyAnimation(self, b"windowOpacity")
        self.fadein.setDuration(200)
        self.fadein.setStartValue(0)
        self.fadein.setEndValue(1)

        
        self.content = achevementWidget(achevement)
        self.achevementGet = QLabel("You got an achevement!")
        self.achevementGet.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.close)
            self.timer.start(5000)
            
            self.fadeout.start()
            

       
    
class achevementWidget(QWidget):
    def __init__(self, achevement : str):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.image = QLabel()
        self.image.setPixmap(QPixmap(os.path.join(mediadir, "images/", "achevements/", achevement + ".png")))
        self.layout_.addWidget(self.image)

        self.text = QLabel(gamedefine.achevementVisualDefine[achevement]["visualName"] + "\n" + gamedefine.achevementVisualDefine[achevement]["hoverDescription"])
        
        self.layout_.addWidget(self.text)
        self.setLayout(self.layout_)
        
