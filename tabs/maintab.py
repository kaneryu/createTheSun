#standard imports
import json
#third party imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpacerItem
from PyQt6.QtGui import QIntValidator
#local imports
import gamedefine
import gameLogic.itemGameLogic as itemGameLogic
import logging_ as logging
import assets.fonts.urbanist.urbanistFont as urbanistFont
import observerModel
import achevements
import gameLogic.numberLogic as numberLogic

class purchaseStrip(QWidget):
    def __init__(self, name):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.name = name
        
        if not gamedefine.itemVisualDefine[name] == None:
            self.internalItem = gamedefine.itemInternalDefine[name]
            self.visualItem = gamedefine.itemVisualDefine[name]
        else:
            self.item = gamedefine.itemInternalDefine["proton"]
            self.visualItem = gamedefine.itemVisualDefine["proton"]
            name = "proton"
            logging.log(f"error importing item '{name}' from gamedefine", 3)
            
        self.setToolTip(gamedefine.itemVisualDefine[name]["description"])
        self.setToolTipDuration(5000)
        
        self.label = QLabel(f"You have {numberLogic.humanReadableNumber(gamedefine.amounts[name])} {self.visualItem['visualName'].lower()}")
        
        self.layout_.addWidget(self.label)
        if not name == "quarks":
            self.purchaseButton = QPushButton("")
        else:
            self.purchaseButton = QPushButton("Free")
        self.purchaseButton.clicked.connect(self.purchase)
        self.layout_.addWidget(self.purchaseButton)
        
        self.setLayout(self.layout_)
    
    def purchase(self):
        observerModel.g_observable.notify_observers(type = "purchase", name = self.name)

        if self.name == "quarks":
            itemGameLogic.purchase("quarks")
            return 0
        
        if itemGameLogic.canAfford(self.name):
            itemGameLogic.purchase(self.name)

    
    def updateTab(self):
        """
        Updates the tab with the current information.

        This method updates the label text to display the amount of a specific item the player has.
        It also updates the purchase button text to display the cost of the item.
        If the item is "quarks", the purchase button text is set to "Free".
        """
        self.label.setText(f"You have {numberLogic.humanReadableNumber(gamedefine.amounts[self.name])} {self.visualItem['visualName'].lower()}")
        
        if not self.internalItem["whatItCosts"][0]["amount"] == -1:

            self.purchaseButton.setText(itemGameLogic.parseCost(self.name))
            if not itemGameLogic.canAfford(self.name):
                self.purchaseButton.setDisabled(True)
            else:
                self.purchaseButton.setDisabled(False)
        else:
            self.purchaseButton.setText("Free")
            
    def showAchevement(self, achevement):
        hecker = achevements.achevementPopup("theBeginning")
        
        hecker.show()
        
            
class header(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignRight)

        
        self.label = QLabel("Buy x")
        self.textEdit = QLineEdit("1")       
        
        self.textEdit.setValidator(QIntValidator())
        self.textEdit.textChanged.connect(self.updateBuyMultiple)
        
        self.spacer = QSpacerItem(10, 0)
        
        
        self.maxAllButton = QPushButton("Max All")
        self.maxAllButton.clicked.connect(itemGameLogic.maxAll)
        
        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.textEdit)
        self.layout_.addItem(self.spacer)
        self.layout_.addWidget(self.maxAllButton)
        self.setLayout(self.layout_)
        self.setMaximumWidth(500)
        
        
    def updateBuyMultiple(self):
        try:
            gamedefine.mainTabBuyMultiple = int(self.textEdit.text())
        except:
            gamedefine.mainTabBuyMultiple = 1
            self.textEdit.setText("1")



        
        
        
class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.header_ = header()
        self.layout_.addWidget(self.header_)
        
        self.purchaseStrips = []
        for i in gamedefine.purchaseToCreate:
            if not i == "electrons":
                print("Creating " + str(i))
                self.purchaseStrips.append(purchaseStrip(i))
                self.layout_.addWidget(self.purchaseStrips[-1])
        
        self.setLayout(self.layout_)
    
    def updateDisplay(self):
        for i in self.purchaseStrips:
            i.updateTab()
            