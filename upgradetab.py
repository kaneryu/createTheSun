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
import game

class upgradeBlock(QFrame):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        self.visualDefine = gamedefine.upgradeVisualDefine[name]
        self.internalDefine = gamedefine.upgradeInternalDefine[name]
        
        self.upgradeLabel = QLabel(f"{self.visualDefine["visualName"]} \n {self.visualDefine["description"]} \n")
        self.upgradeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.upgradeLabel, 0, 0)
        
        self.upgradeDescription = QLabel(f"{self.visualDefine["upgradeVisualName"]} \n {self.visualDefine["upgradeDescription"]}")

        self.upgradeDescription.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.layout.addWidget(self.upgradeDescription, 1, 0)
        
        self.upgradeButton = QPushButton(self.parseCost(self.name))
        
        self.upgradeButton.clicked.connect(self.purchase)
        
        self.layout.addWidget(self.upgradeButton, 2, 0)
        
        self.usefulDescription = QLabel(self.parseUsefulDescription())
        
        self.layout.addWidget(self.usefulDescription, 3, 0)
        
        self.setLayout(self.layout)
    
    def purchase(self): 
        if game.canAffordUpgrade(self.name):
            game.purchaseUpgrade(self.name)
            if self.name == "particleAccelerator":
                equasion = gamedefine.upgradeInternalDefine[self.name]["idleGenerator"]["timeEquation"]
                gamedefine.upgradeDetails[self.name]["timeToWait"] = int(floor(game.evaluateCostEquation(equasion, gamedefine.upgradeLevels[self.name])))
                
                
    def parseCost(self, name):
        if gamedefine.upgradeLevels[name] == 0:
            what = self.internalDefine["firstCost"]
            string = ["Purchase for "]
        else:
            what = self.internalDefine["upgradeCost"]
            string = ["Upgradge for "]
        
        
        
        for i in what:
            string.append(str(i["amount"]) + " ")
            string.append(i["what"])
            if what.index(i) < len(what) - 2:
                string.append(", ")
            elif what.index(i) == len(what) - 2:
                string.append(" and ")
            else:
                string.append(".")
        
        return "".join(string)
    
    def parseUsefulDescription(self):
        
        if self.internalDefine["type"] == "idleGenerator":
            current = list(self.visualDefine["currentUpgradeUsefulDescription"])
            withNewUpgrade = list(self.visualDefine["upgradeUsefulDescription"])
            
            if self.visualDefine["usefulDescriptionBlank"] == "tickTime":
                current[current.index("%%%")] = str(round(game.evaluateCostEquation(self.internalDefine["idleGenerator"]["timeEquation"], gamedefine.upgradeLevels[self.name])))
                withNewUpgrade[withNewUpgrade.index("%%%")] = str(round(game.evaluateCostEquation(self.internalDefine["idleGenerator"]["timeEquation"], gamedefine.upgradeLevels[self.name])))
            print(str(round(game.evaluateCostEquation(self.internalDefine["idleGenerator"]["timeEquation"], gamedefine.upgradeLevels[self.name]))))
            return (f"{"".join(current)} \n {"".join(withNewUpgrade)}")
   
    def updateDisplay(self):
        if game.canAffordUpgrade(self.name):
            self.upgradeButton.setEnabled(True)
        else:
            self.upgradeButton.setEnabled(False)
        
        self.upgradeButton.setText(self.parseCost(self.name))
        #self.usefulDescription.setText(self.parseUsefulDescription())
        
    def updateInternal(self):
        if self.internalDefine["type"] == "idleGenerator":
            self.doUpgradeTask()
            
    def doUpgradeTask(self):
        if gamedefine.upgradeLevels[self.name] > 0:
            if self.internalDefine["type"] == "idleGenerator":
                if time.time() * 1000 - self.lastTickTime > gamedefine.upgradeDetails[self.name]["timeToWait"]:
                    self.lastTickTime = time.time() * 1000
                    
                    if self.internalDefine["withRequirement"]:
                        if game.canAffordUpgradeTask(self.name):
                            for i in gamedefine.upgradeDetails[self.name]["whatYouGet"]:
                                gamedefine.amounts[i["what"]] += i["amount"]
                    else:         
                        for i in gamedefine.upgradeDetails[self.name]["whatYouGet"]:
                            gamedefine.amounts[i["what"]] += i["amount"]
            
        

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.upgradeBlocks = []
        for i in gamedefine.upgradesToCreate:
            print("creating upgrade " + i)
            self.upgradeBlocks.append(upgradeBlock(i))
            self.layout.addWidget(self.upgradeBlocks[-1])
        
        self.setLayout(self.layout)
    
    def updateDisplay(self):
        for i in self.upgradeBlocks:
            i.updateDisplay()
    
    def updateInternal(self):
        for i in self.upgradeBlocks:
            i.updateInternal()