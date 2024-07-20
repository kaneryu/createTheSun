#standard imports
import json
from copy import deepcopy
import sys
import math
#third party imports
# from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpacerItem
# from PyQt6.QtGui import QIntValidator

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QIntValidator

#local imports
import .gamedefine
import .observerModel
import .gameLogic.numberLogic as numberLogic
import .gameLogic.automationGameLogic as automationGameLogic

    

        
class unlockStrip(QWidget):
    def __init__(self, name: str, maintab: bool | None = False):
        super().__init__()
        self.containerLayout = QVBoxLayout()
        self.innerLayout = QHBoxLayout()
        self.innerLayout.setContentsMargins(0,0,0,0)
        self.innerContainer = QWidget()
        self.innerContainer.setLayout(self.innerLayout)
        self.innerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.name = name
        self.maintab = maintab
        self.internalItem = gamedefine.gamedefine.unlockables[name]
        self.visualItem = gamedefine.gamedefine.unlockablesVisualDefine[name]
        
        self.setToolTip(gamedefine.gamedefine.unlockablesVisualDefine[name]["hoverDescription"])
        self.setToolTipDuration(5000)
        
        self.label = QLabel(self.visualItem['visualName'])
        

        
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(50)
        
        self.innerLayout.addWidget(self.label)
        self.innerLayout.addWidget(self.progress)
        
        self.containerLayout.addWidget(self.innerContainer)
        if not maintab:
            self.needsLabel = QLabel(self.getYouNeedText())
            self.containerLayout.addWidget(self.needsLabel)
        
        self.setLayout(self.containerLayout)
    
    def getAmountNeeded(self) -> list[tuple[str, str, int]]:
        #                             tuple is: type, item needed, amount needed
        returnValue: list[tuple[str, str, int]] = []
        for need in self.internalItem["needs"]:
            returnValue.append((need["type"], need["what"], need["amount"]))
            
        return returnValue

    def getAmountDepedingOnType(self, type, what) -> int:
        if type == "item":
            return gamedefine.gamedefine.amounts[what]
        if type == "automation":
            return gamedefine.gamedefine.automationLevels[what]
        
        raise ValueError("Type not found")

    def getAmountCurrentlyAvailable(self) -> list[tuple[str, str, int]]:
        #                             tuple is: type, item, amount currenly available
        returnValue: list[tuple[str, str, int]] = []
        for need in self.internalItem["needs"]:
            returnValue.append((need["type"], need["what"], self.getAmountDepedingOnType(need["type"], need["what"])))
        return returnValue
    
    def calculatePercentageToUnlock(self) -> int:
        amountNeeded = self.getAmountNeeded()
        amountCurrentlyAvailable = self.getAmountCurrentlyAvailable()
        
        percentages: list[int] = []
        
        for needed in amountNeeded:
            for available in amountCurrentlyAvailable:
                if needed[1] == available[1]:
                    percentages.append(min(math.floor((available[2] / needed[2]) * 100), 100))

                    
        if self.visualItem["scale"] == "linear":
            percentageSum = sum(percentages)
            divisor = 100 * len(percentages)
            return round((percentageSum / divisor) * 100)
        
        if self.visualItem["scale"] == "log":
            percentageSum = sum(percentages)
            logBase = 100 * len(percentages)
            return round(math.log(percentageSum, logBase) * 100)
        
        raise ValueError("Scale not found")
    
    def getYouNeedText(self) -> str:
        exempt = ["hydrogen"]
        def addS(amount, what: str):
            if what.lower() in exempt:
                return what
            if amount == 1:
                return what[::-1] # remove the s
            return what
        
        amountNeeded = self.getAmountNeeded()
        amountHave = self.getAmountCurrentlyAvailable()
        string = "You Need:\n\t"
        for amountNeededItem, amountHaveItem in zip(amountNeeded, amountHave):

            visualName: str
            if amountNeededItem[0] == "item":
                visualName = gamedefine.gamedefine.itemVisualDefine[amountNeededItem[1]]["visualName"]
                string += f"{amountNeededItem[2]} {addS(self.getAmountDepedingOnType(amountNeededItem[0], amountNeededItem[1]), amountNeededItem[1])} (Currently have {self.getAmountDepedingOnType(amountHaveItem[0], amountHaveItem[1])})\n\t"
                   
            elif amountNeededItem[0] == "automation":
                visualName = automationGameLogic.getAutomationName(amountNeededItem[1])
                string += f"Level {amountNeededItem[2]} {visualName} (Currently have Level {self.getAmountDepedingOnType(amountHaveItem[0], amountHaveItem[1])})\n\t"
                
            else:
                raise ValueError("Type not found")    
            
            # example line:
            # You Need:
            #    5 Protonic Forges (Currently have 3)
            #    200 Quarks (Currently have 100)
            
        
        return string
    
    def updateTab(self):
        """
        Updates the tab with the current information.
        """
        def mainTabUpdateTab():
            """
            Updates the tab with the current information.
            """

            highestPercentage: tuple[int, str] = (-1, "")
            for item in gamedefine.gamedefine.unlockables:
                if not gamedefine.gamedefine.unlockables[item]["visible"]:
                    continue # if it's not visible, skip
                
                self.internalItem = gamedefine.gamedefine.unlockables[item]
                self.visualItem = gamedefine.gamedefine.unlockablesVisualDefine[item]
                
                if self.calculatePercentageToUnlock() > highestPercentage[0]:
                    highestPercentage = (self.calculatePercentageToUnlock(), item)
            
            self.name = highestPercentage[1]
            self.internalItem = gamedefine.gamedefine.unlockables[highestPercentage[1]]
            self.visualItem = gamedefine.gamedefine.unlockablesVisualDefine[highestPercentage[1]]
            
            self.label.setText(self.visualItem['visualName'])
            self.setToolTip(gamedefine.gamedefine.unlockablesVisualDefine[highestPercentage[1]]["hoverDescription"])
            self.progress.setValue(self.calculatePercentageToUnlock())
            
        if not self.maintab:
            self.progress.setValue(self.calculatePercentageToUnlock())
            self.needsLabel.setText(self.getYouNeedText())
        else:
            mainTabUpdateTab()
        
            

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.explainer = QLabel("This is the unlock tab. Here you can view how close you are to unlocking new things")
        self.layout_.addWidget(self.explainer)
        
        observerModel.registerObserver(self.reset, observerModel.Observable.RESET_OBSERVABLE, observerModel.ObservableCallType.ALL, observerModel.ObservableCheckType.TYPE, "unlockTab")
        
        self.unlockStrips: list[unlockStrip] = []
        for i in gamedefine.gamedefine.unlockables:
            currentDict = gamedefine.gamedefine.unlockables[i]
            if currentDict["visible"]:
                self.unlockStrips.append(unlockStrip(i))
                self.layout_.addWidget(self.unlockStrips[-1])
        
        self.setLayout(self.layout_)
    
    
    def updateDisplay(self):
        for i in self.unlockStrips:
            i.updateTab()
        
        visibleAmount = 0
        for i in gamedefine.gamedefine.unlockables:
            if gamedefine.gamedefine.unlockables[i]["visible"]:
                visibleAmount += 1
        
        if not len(self.unlockStrips) == visibleAmount:
            self.reset(None)
            
               
        
    
    def reset(self, event):
        for i in reversed(range(len(self.unlockStrips))):
            widget = self.unlockStrips[i]
            self.layout_.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
            self.unlockStrips.pop(i)
            print("randremoved")

        
        
        for i in gamedefine.gamedefine.unlockables:
            currentDict = gamedefine.gamedefine.unlockables[i]
            if currentDict["visible"]:
                self.unlockStrips.append(unlockStrip(i))
                self.layout_.addWidget(self.unlockStrips[-1])