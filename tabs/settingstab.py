#standard imports
import json
import time
#third party imports
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QProgressBar, QComboBox
#from PyQt6.QtGui import 
#local imports
import save
import gamedefine


def save_():
    save.save()
def load():
    save.load()
settings = {
    
    "save": {
        "name": "Save",
        "description": "Save your progress",
        "action": save_,
        "buttonName": "Save",
        "specialAttribute": "autosaveWidget",
        "updates": [True, True], # internalUpdate, displayUpdate
        "static": False
    },
    "load": {
        "name": "Load",
        "description": "Load your progress",
        "action": load,
        "buttonName": "Load",
        "specialAttribute": None,
        "updates": [False, False],
        "static": False
        },
}

class autosaveWidget(QWidget):
    def __init__(self, setting):
        super().__init__()
        self.layout_ = QHBoxLayout()
        self.progressbar = QProgressBar()
        self.chooseOption = QComboBox()
        chooseOptionChoices = ["Off", "1 minute", "5 minutes", "10 minutes", "30 minutes"]
        self.chooseOptionMs = [-1, 60000, 300000, 600000, 1800000]
        self.chooseOption.addItems(chooseOptionChoices)
        self.chooseOption.setCurrentIndex(self.chooseOptionMs.index(gamedefine.autosaveTime))
        self.chooseOption.currentIndexChanged.connect(lambda: self.chooseOptionChanged())
        self.layout_.addWidget(self.progressbar)
        self.layout_.addWidget(self.chooseOption)
        
        self.progressbar.setFormat("Autosave in %v seconds")
        gamedefine.lastAutosaveTime = time.time() * 1000
        
        self.setLayout(self.layout_)
        
    def updateDisplay(self):
        if int((gamedefine.autosaveTime - (time.time() * 1000 - gamedefine.lastAutosaveTime)) // 1000) < 2 or (time.time() * 1000 - gamedefine.lastAutosaveTime) // 1000 < 2:
            # if the time less is less than 2 seconds or less than 2 seconds after last autosave, then autosave is happening
            self.progressbar.setMaximum(0)
            return
        if not gamedefine.autosaveTime == -1 and not gamedefine.autosaveTime == 0 and not gamedefine.autosaveTime == None:
            self.progressbar.setValue(int((gamedefine.autosaveTime - (time.time() * 1000 - gamedefine.lastAutosaveTime)) // 1000))
            self.progressbar.setFormat("Autosave in %v seconds")
            self.progressbar.setMaximum(gamedefine.autosaveTime // 1000)
        else:
            self.progressbar.setValue(-1)
            self.progressbar.setFormat("Autosave is off")
            self.progressbar.setMaximum(0)
    def updateInternal(self):
        if not gamedefine.autosaveTime == -1 and not gamedefine.autosaveTime == 0 and not gamedefine.autosaveTime == None:
            if time.time() * 1000 - gamedefine.lastAutosaveTime >= gamedefine.autosaveTime:
                gamedefine.lastAutosaveTime = time.time() * 1000
                save.save(notify = False)
            
    def chooseOptionChanged(self):
        gamedefine.autosaveTime = self.chooseOptionMs[self.chooseOption.currentIndex()]
        print(gamedefine.autosaveTime)
        save.save(notify = False)

    
        
        


class setting(QFrame):
    def __init__(self, setting):
        super().__init__()
        self.thing = setting
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.layout_ = QGridLayout()
        self.setMaximumSize(QSize(700, 200))
        self.lastTickTime = 0
        
        self.label = QLabel(settings[setting]["name"])
        self.label.setWordWrap(True)
        self.setToolTip(settings[setting]["description"])
        self.setToolTipDuration(5000)
        self.layout_.addWidget(self.label, 0, 0)
        
        self.button = QPushButton(settings[setting]["buttonName"])
        self.button.clicked.connect(settings[setting]["action"])
        self.layout_.addWidget(self.button, 0, 1)
        
        if settings[setting]["specialAttribute"] == "autosaveWidget":
            self.specialAttribute = autosaveWidget(setting)
            self.layout_.addWidget(self.specialAttribute, 1, 0) 
        
        self.setLayout(self.layout_)
    
    def updateDisplay(self):
        if settings[self.thing]["specialAttribute"] == "autosaveWidget":
            self.specialAttribute.updateDisplay()
    
    def updateInternal(self):
        if settings[self.thing]["specialAttribute"] == "autosaveWidget":
            self.specialAttribute.updateInternal()


class content(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_ = QVBoxLayout()
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_)
        
        self.widgets: list[setting] = []
        for i in settings:
            self.widgets.append(setting(i))
            self.layout_.addWidget(self.widgets[-1])
        
    def updateDisplay(self):
        for i in self.widgets:
            i.updateDisplay()
    
    def updateInternal(self):
        for i in self.widgets:
            i.updateInternal()

    