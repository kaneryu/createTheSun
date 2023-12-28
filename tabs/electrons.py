import time

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from PyQt6.QtCore import *

import gamedefine

class electrons(QWidget):
    def updateDisplay(self):               
        self.amountBar.setValue(gamedefine.amounts["electrons"])
        self.label.setText(f"{gamedefine.amounts["electrons"]}")
    def updateInternal(self):
        if time.time() * 1000 - self.lastTickTime > gamedefine.electronDetails["waitTime"]:
            self.lastTickTime = time.time() * 1000
            gamedefine.amounts["electrons"] += gamedefine.electronDetails["amount"]
            
            if gamedefine.amounts["electrons"] > gamedefine.electronDetails["maxAmount"]:
                gamedefine.amounts["electrons"] = gamedefine.electronDetails["maxAmount"]
                
            if gamedefine.amounts["electrons"] < gamedefine.electronDetails["minAmount"]:
                gamedefine.amounts["electrons"] = gamedefine.electronDetails["minAmount"]
                
    def __init__(self):
        super().__init__()
        self.lastTickTime = 0
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label)
        
        
        self.amountBar = QProgressBar()
        self.amountBar.setMaximum(100)
        self.amountBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.amountBar.setFormat("")
        self.setToolTip("Electrons")
        
        self.layout.addWidget(self.amountBar)
        
        self.setLayout(self.layout)
        