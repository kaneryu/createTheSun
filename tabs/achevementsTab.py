from PySide6 import QtGui
from PySide6.QtGui import QPixmap, QRegion
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsBlurEffect, QGridLayout, QApplication
from PySide6.QtCore import QPropertyAnimation, Qt, QTimer, QEasingCurve, QRect
import os

from time import time
import pathlib
import gamedefine

basedir = os.path.dirname(os.path.realpath(__file__))

mediadir = os.path.join(str(pathlib.Path(basedir).parent) + "\\assets\\")


class achevementPopup(QWidget):
    def __init__(self, achevement : str, open : bool = False):
        super().__init__()
        self.setObjectName("achevementPopupBackgroundWidget")
        self.setWindowTitle("Test")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.setContentsMargins(0,0,0,0)
        

        
        
        globalMousePos = QtGui.QCursor.pos()
        
        # Ensure size hint is updated
        self.fadein = QPropertyAnimation(self, b"windowOpacity")
        self.fadein.setDuration(200)
        self.fadein.setStartValue(0)
        self.fadein.setEndValue(1)
        
        self.image = QLabel()
        self.image.setPixmap(QPixmap(os.path.join(mediadir, f"images\\achevements\\{achevement}")))
        self.image.setContentsMargins(0,0,0,0)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.achevementGet = QLabel(f"You got an achevement:\n{gamedefine.achevementVisualDefine[achevement]["visualName"]}")
        self.achevementGet.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.achevementGet.setObjectName("achevementPopupText")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.image)
        layout.addWidget(self.achevementGet)
        self.setLayout(layout)
        
        self.setGeometry(globalMousePos.x() + 100, globalMousePos.y() + 100, 200, 200)
                #rounded corners
        #self.setMask(QRegion(QRect(globalMousePos.x() - 100, globalMousePos.y() - 100, 200, 200), QRegion.RegionType.Ellipse))
        self.adjustSize()
        
        self.fadeout = QPropertyAnimation(self, b"windowOpacity")
        self.fadeout.setDuration(200)
        self.fadeout.setStartValue(1)
        self.fadeout.setEndValue(0)
        self.fadeout.finished.connect(self.close)
        
        if open:
            self.popup()
        else:
            achevementPopupQueue.append(self)
        
    def popup(self):
        self.show()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fadeout.start)


        self.fadein.finished.connect(lambda: self.timer.start(5000))
        self.fadein.start()
        

            
achevementPopupQueue: list[achevementPopup] = []
       
    
class achevementWidget(QWidget):
    def __init__(self, achevement : str):
        super().__init__()
        self.setAutoFillBackground(False)
        self.alreadyBlurredIn = False
        
        self.name = achevement
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaximumSize(100,100)
        self.image = QLabel()
        self.image.setPixmap(QPixmap(os.path.join(mediadir, "images\\", "achevements\\", achevement + ".png")))
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        
        for j in achevementPopupQueue:
            j: achevementPopup
            j.popup()
            achevementPopupQueue.remove(j)
