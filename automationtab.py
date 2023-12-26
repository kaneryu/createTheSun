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
import automationGameLogic

class automationBlock(QFrame):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        self.visualDefine = gamedefine.automationVisualDefine[name]
        self.internalDefine = gamedefine.automationInternalDefine[name]
        
        self.upgradeLabel = QLabel(automationGameLogic.parseUpgradeName(self.name))
        self.upgradeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.upgradeLabel, 0, 0)
        
        self.upgradeDescription = QLabel(automationGameLogic.getDescription(self.name))
        self.upgradeDescription.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.upgradeDescription, 1, 0)
        
        self.upgradeButton = QPushButton(automationGameLogic.parseCost(self.name))
        self.upgradeButton.clicked.connect(self.purchase)
        self.layout.addWidget(self.upgradeButton, 2, 0)
        
        self.usefulDescription = QLabel(automationGameLogic.parseUsefulDescription(self.name))
        self.layout.addWidget(self.usefulDescription, 3, 0)
        self.setLayout(self.layout)
    
    def purchase(self): 
        if automationGameLogic.canAffordUpgrade(self.name):
            automationGameLogic.purchaseUpgrade(self.name)
            automationGameLogic.updateUpgradeStatus(self.name)
                
            self.usefulDescription.setText(automationGameLogic.parseUsefulDescription(self.name))
            self.upgradeDescription.setText(automationGameLogic.getDescription(self.name))
            self.upgradeLabel.setText(automationGameLogic.parseUpgradeName(self.name))
            self.upgradeButton.setText(automationGameLogic.parseCost(self.name))
              

    def updateDisplay(self):
        if automationGameLogic.canAffordUpgrade(self.name):
            self.upgradeButton.setEnabled(True)
        else:
            self.upgradeButton.setEnabled(False)
            
        
    def updateInternal(self):
        if self.internalDefine["type"] == "idleGenerator":
            self.lastTickTime = automationGameLogic.doUpgradeTask(self.name, self.lastTickTime)
            
        

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.automationBlocks = []
        for i in gamedefine.automationsToCreate:
            print("creating automation " + i)
            self.automationBlocks.append(automationBlock(i))
            self.layout.addWidget(self.automationBlocks[-1])
        
        self.setLayout(self.layout)
    
    def updateDisplay(self):
        for i in self.automationBlocks:
            i.updateDisplay()
    
    def updateInternal(self):
        for i in self.automationBlocks:
            i.updateInternal()