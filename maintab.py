#standard imports
import json
#third party imports
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
#local imports
import gamedefine
import game
import logging
import achevements

class purchaseStrip(QWidget):
    def __init__(self, name):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.name = name
        if not gamedefine.internalGameDefine[name] == None:
            self.internalItem = gamedefine.internalGameDefine[name]
            self.visualItem = gamedefine.visualGameDefine[name]
        else:
            self.item = gamedefine.internalGameDefine["proton"]
            self.visualItem = gamedefine.visualGameDefine["proton"]
            name = "proton"
            logging.log(f"error importing item '{name}' from gamedefine", 3)
        
        self.label = QLabel(f"You have {gamedefine.amounts[name]} {self.visualItem['visualName'].lower()}")
        self.layout.addWidget(self.label)
        if not name == "quarks":
            self.getCurrentCostDict = game.getCurrentCost(name)
            self.currentCost = self.getCurrentCostDict[list(self.getCurrentCostDict.keys())[0]]
            self.whatItCosts = list(self.getCurrentCostDict.keys())[0]
            self.purchaseButton = QPushButton(f"Cost: {self.currentCost} {gamedefine.visualGameDefine[self.whatItCosts]['visualName'].lower()}")
        else:
            self.purchaseButton = QPushButton("Free")
        self.purchaseButton.clicked.connect(self.purchase)
        self.layout.addWidget(self.purchaseButton)
        
        self.setLayout(self.layout)
    
    def purchase(self):
        if self.name == "quarks":
            game.purchase("quarks")
            return 0
        
        if game.canAfford(self.name):
            game.purchase(self.name)

    def showAchievementPopup(self, achievement):
        self.achievementPopup = achevements.achevementPopup(achievement, self, True)
        
    def updateTab(self):
        """
        Updates the tab with the current information.

        This method updates the label text to display the amount of a specific item the player has.
        It also updates the purchase button text to display the cost of the item.
        If the item is "quarks", the purchase button text is set to "Free".
        """
        self.label.setText(f"You have {game.humanReadableNumber(gamedefine.amounts[self.name])} {self.visualItem['visualName'].lower()}")
        if not self.name == "quarks":
            self.getCurrentCostDict = game.getCurrentCost(self.name)
            self.currentCost = self.getCurrentCostDict[list(self.getCurrentCostDict.keys())[0]]
            self.whatItCosts = list(self.getCurrentCostDict.keys())[0]
            self.purchaseButton.setText(f"Cost: {game.humanReadableNumber(self.currentCost)} {gamedefine.visualGameDefine[self.whatItCosts]['visualName'].lower()}")
            if not game.canAfford(self.name):
                self.purchaseButton.setDisabled(True)
            else:
                self.purchaseButton.setDisabled(False)
        else:
            self.purchaseButton.setText("Free")
        

        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.purchaseStrips = []
        for i in gamedefine.purchaseToCreate:
            if not i == "electrons":
                print("Creating " + str(i))
                self.purchaseStrips.append(purchaseStrip(i))
                self.layout.addWidget(self.purchaseStrips[-1])
        
        self.setLayout(self.layout)
    
    def updateDisplay(self):
        for i in self.purchaseStrips:
            i.updateTab()