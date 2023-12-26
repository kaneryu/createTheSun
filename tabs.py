#from PyQt6.QtCore import
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
#from PyQt6.QtGui import 
import sys

import maintab
import automationtab

class mainTab(QWidget):
    def updateDisplay(self):
        self.tabContent.updateDisplay()
    def updateInternal(self):
        pass
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = maintab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
         
    def name(): #type: ignore
        return "Main Tab"

class upgradeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Upgrade Tab"))
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Upgrades"

class automationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = automationtab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        self.tabContent.updateDisplay()
        
    def updateInternal(self):
        self.tabContent.updateInternal()
    
    def name(): #type: ignore
        return "Automation"
        
class settingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Settings Tab"))
        self.setLayout(self.layout_)
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Settings"
    
class achievementsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Achievements Tab"))
        self.setLayout(self.layout_)
    def updateDisplay(self):
        return 0
    
    def name(): #type: ignore
        return "Achevements"

tabs = [mainTab, upgradeTab, settingsTab, achievementsTab]