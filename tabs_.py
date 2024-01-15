# from PyQt6.QtCore import
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
# from PyQt6.QtGui import 

# from PySide6.QtCore import
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
# from PySide6.QtGui import

import sys
import save
import tabs.maintab as maintab
import tabs.automationtab as automationtab
import tabs.settingstab as settingstab
saveModule = save # I don't know if importing save from main.py will cause a circular import, but this feels safer for now.

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
    
    def tooltip(): #type: ignore
        return "The main tab of the game, where you can purchase quarks, protons, etc."
    
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

        
    def tooltip(): #type: ignore
        return "How can you see this?"
    
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
        
    def updateEverything(self):
        self.tabContent.updateEverything()
    
    def name(): #type: ignore
        return "Automation"
    
    def tooltip(): #type: ignore
        return "The tab where you purchase automations, which do things for you."
    
    
class settingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tabContent = settingstab.content()
        self.layout_.addWidget(self.tabContent)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        self.tabContent.updateDisplay()
    def updateInternal(self):
        self.tabContent.updateInternal()
    
    def name(): #type: ignore
        return "Settings"
    
        
    def tooltip(): #type: ignore
        return "The tab that contains all game settings, including saving and loading"
    
    
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
    
    def tooltip(): #type: ignore
        return "Shhhh..."
    

tabs = [mainTab, automationTab, settingsTab]