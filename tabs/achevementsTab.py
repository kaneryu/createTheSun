from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsBlurEffect, QGridLayout
from PySide6.QtCore import QPropertyAnimation, Qt, QTimer, QEasingCurve
import os
from time import time
import pathlib
import gamedefine


basedir = os.path.dirname(os.path.realpath(__file__))

mediadir = os.path.join(str(pathlib.Path(basedir).parent) + "\\assets\\")

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
        
        self.alreadyBlurredIn = False
        
        self.name = achevement
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaximumSize(100,100)
        self.image = QLabel()
        self.image.setPixmap(QPixmap(os.path.join(mediadir, "images\\", "achevements\\", achevement + ".png")))
        
        self.layout_.addWidget(self.image)

        
        self.setToolTip(f"{gamedefine.achevementVisualDefine[achevement]["visualName"]} \n {gamedefine.achevementVisualDefine[achevement]["hoverDescription"]} \n {gamedefine.achevementVisualDefine[achevement]["rewardDescription"]}")
        

        self.effectsSetup()
        self.setLayout(self.layout_)
    
    def effectsSetup(self):
        self.blurEffect = QGraphicsBlurEffect()
        self.setGraphicsEffect(self.blurEffect)
        
        self.blurIn = QPropertyAnimation(self.blurEffect, b"blurRadius")
        self.blurIn.setDuration(600)
        self.blurIn.setStartValue(0)
        self.blurIn.setEndValue(10)
        self.blurIn.setEasingCurve(QEasingCurve.Type.OutSine)
        
        self.blurOut = QPropertyAnimation(self.blurEffect, b'blurRadius')
        self.blurOut.setDuration(300)
        self.blurOut.setStartValue(10)
        self.blurOut.setEndValue(0)
        self.blurOut.setEasingCurve(QEasingCurve.Type.OutSine)
        
    def displayUpdate(self):
        if not self.name in gamedefine.unlockedAchevements:
            if not self.blurIn.state() == QPropertyAnimation.State.Running and not self.alreadyBlurredIn:
                self.effectsSetup()
                self.blurIn.start()
                self.alreadyBlurredIn = True
                
        else:
            if not self.blurOut.state() == QPropertyAnimation.State.Running and self.alreadyBlurredIn:
                self.effectsSetup()
                self.blurIn.stop()
                self.blurOut.start()
                self.alreadyBlurredIn = False

            
class content(QWidget):
    def __init__(self):
        super().__init__()
        
        achevementsPerRow = 5
        self.layout_ = QGridLayout()
        
        self.widgets = []
        
        rowCounter = 0
        columnCounter = 0
        
        
        for i in gamedefine.achevementInternalDefine:
            if rowCounter == achevementsPerRow - 1:
                columnCounter += 1
                rowCounter = 0
                
            self.widgets.append(achevementWidget(i))
            self.layout_.addWidget(self.widgets[-1], columnCounter, rowCounter)
            rowCounter += 1
        
        self.setLayout(self.layout_)
        
    def displayUpdate(self):
        for i in self.widgets:
            i: achevementWidget
            i.displayUpdate()