#standard imports
import json
import time
import copy
from math import floor, ceil
#third party imports
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
#local imports
import gamedefine
import upgradeGameLogic

class automationBlock(QFrame):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        self.visualDefine = gamedefine.upgradeVisualDefine[name]
        self.internalDefine = gamedefine.upgradeInternalDefine[name]
        
        self.upgradeLabel = QLabel(upgradeGameLogic.parseUpgradeName(self.name))
        self.upgradeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.upgradeLabel, 0, 0)
        
        self.upgradeDescription = QLabel(upgradeGameLogic.getDescription(self.name))
        self.upgradeDescription.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.upgradeDescription, 1, 0)
        
        self.upgradeButton = QPushButton(upgradeGameLogic.parseCost(self.name))
        self.upgradeButton.clicked.connect(self.purchase)
        self.layout.addWidget(self.upgradeButton, 2, 0)
        
        self.usefulDescription = QLabel(upgradeGameLogic.parseUsefulDescription(self.name))
        self.layout.addWidget(self.usefulDescription, 3, 0)
        self.setLayout(self.layout)
    
    def purchase(self): 
        if upgradeGameLogic.canAffordUpgrade(self.name):
            upgradeGameLogic.purchaseUpgrade(self.name)
            upgradeGameLogic.updateUpgradeStatus(self.name)
                
            self.usefulDescription.setText(upgradeGameLogic.parseUsefulDescription(self.name))
            self.upgradeDescription(upgradeGameLogic.getDescription(self.name))
            self.upgradeLabel.setText(upgradeGameLogic.parseUpgradeName(self.name))
            self.upgradeButton.setText(upgradeGameLogic.parseCost(self.name))
              

    def updateDisplay(self):
        if upgradeGameLogic.canAffordUpgrade(self.name):
            self.upgradeButton.setEnabled(True)
        else:
            self.upgradeButton.setEnabled(False)
            
        
    def updateInternal(self):
        if self.internalDefine["type"] == "idleGenerator":
            self.lastTickTime = upgradeGameLogic.doUpgradeTask(self.name, self.lastTickTime)
            
        

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.upgradeBlocks = []
        for i in gamedefine.upgradesToCreate:
            print("creating upgrade " + i)
            self.upgradeBlocks.append(automationBlock(i))
            self.layout.addWidget(self.upgradeBlocks[-1])
        
        self.setLayout(self.layout)
    
    def updateDisplay(self):
        for i in self.upgradeBlocks:
            i.updateDisplay()
    
    def updateInternal(self):
        for i in self.upgradeBlocks:
            i.updateInternal()