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
import tabs.achevementsTab as achevementsTab_
import resourceGain

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
        return "Purchase items like Quarks, Protons, Hydrogen, etc."
    
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
        return "Keep your fingers off the mouse."
    
    
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
        return "Settings..."
    
    
class achievementsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.content = achevementsTab_.content()
        self.layout_.addWidget(self.content)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        self.content.displayUpdate()
    
    def name(): #type: ignore
        return "Achevements"
    
    def tooltip(): #type: ignore
        return "A ledger of your accomplishments."
    
class rewritesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.addWidget(QLabel("Rewrites Tab"))
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        return 0
    
    def updateInternal(self):
        return 0
    
    def name(): #type: ignore
        return "Rewrites"

        
    def tooltip(): #type: ignore
        return "The laws of the universe are in yout hands."

class statsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.tracker = QLabel()
        self.layout_.addWidget(self.tracker)
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        tracked = ["You are gaining"]
        for i in resourceGain.data.gainPerSecond:
            tracked.append(f"{resourceGain.data.gainPerSecond[i]} {i}")
        tracked.append("Per second")
        final = ""
        for i in tracked:
            final += i + '\n'
            
            
        self.tracker.setText(final)
    
    def updateInternal(self):
        return 0
    
    def name(): #type: ignore
        return "Stats"

        
    def tooltip(): #type: ignore
        return "Information about production"

tabs = [mainTab, automationTab, achievementsTab, settingsTab, statsTab]
internalUpdateList = [automationTab.updateInternal, settingsTab.updateInternal]
internalUpdateable = [automationTab.updateInternal, settingsTab.updateInternal, statsTab.updateInternal]