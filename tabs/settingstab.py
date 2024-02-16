#standard imports
import json
import time
import os
#third party imports

from PySide6.QtCore import Qt, QSize, Signal as pyqtSignal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QProgressBar, QComboBox, QScrollArea, QScrollBar
# from PySide6.QtGui import


#local imports
import save
from customWidgets import dialogs
import gamedefine


def save_():
    save.save(slot = 0)
def load():
    save.load(slot = 0)

class saveLoadWidget(QWidget):
    class individualSaveLoadWidget(QWidget):
        def __init__(self, slotNum: int, metadata: dict):
            super().__init__()
            self.slotNum = slotNum
            self.metadata = metadata
            self.layout_ = QVBoxLayout()
            
            self.timeZone = time.timezone
            self.rawLastUsed = self.metadata["lastUsedOn"]
            self.humanReadableLastUsed = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(self.rawLastUsed))
            
            self.slotLabel = QLabel(f"Slot {self.slotNum}, Quarks: {self.metadata["amounts"]['quarks']},\nLast used: {self.humanReadableLastUsed}")
            self.layout_.addWidget(self.slotLabel)
            
            self.buttonLayout = QHBoxLayout()
            self.buttonContainer = QWidget()
            self.buttonContainer.setLayout(self.buttonLayout)
            self.layout_.addWidget(self.buttonContainer)
            
            self.saveButton = QPushButton("Save")
            self.saveButton.clicked.connect(lambda: saveLoad(True))
            self.buttonLayout.addWidget(self.saveButton)
            
            self.loadButton = QPushButton("Load")
            self.loadButton.clicked.connect(lambda: saveLoad(False))
            self.buttonLayout.addWidget(self.loadButton)
            
            self.setLayout(self.layout_)

            def saveLoad(save_: bool = True):
                if save_:
                    save.save(slot = self.slotNum)
                else:
                    save.load(slot = self.slotNum)
                
                self.parent().parent().updateDisplayWithLists() # type: ignore
            
    
    class newSlotWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.layout_ = QVBoxLayout()
            self.setLayout(self.layout_)
            
            self.newSlotButton = QPushButton("New Slot with current progress")
            self.newSlotButton.clicked.connect(lambda: self.newSlotWithCurrentProgress())
            self.layout_.addWidget(self.newSlotButton)
            
            self.newNewSlotButton = QPushButton("New Slot with no progress")
            self.newNewSlotButton.clicked.connect(lambda: self.newSlotWithNoProgress())
            self.layout_.addWidget(self.newNewSlotButton)
        
        def newSlotWithCurrentProgress(self):
            save.save(slot = save.getHighestSaveSlot() + 1, notify = False)
            save.load(slot = save.getHighestSaveSlot(), noSpeak = True)
            self.parent().updateDisplayWithLists() # type: ignore
        
        def newSlotWithNoProgress(self):
            save.save(slot = save.getHighestSaveSlot() + 1, blank = True)
            save.load(slot = save.getHighestSaveSlot(), noSpeak = True)
            self.parent().updateDisplayWithLists() # type: ignore
            
    def __init__(self):
        super().__init__()
        self.topLevelLayout = QVBoxLayout()
        self.containerLayout = QVBoxLayout()
        
        self.containerWidget = QWidget()
        
        self.containerWidget.setLayout(self.containerLayout)
        self.updateDisplayWithLists()
        
        self.autoSaver = autosaveWidget()
        
        self.currentSlotText = QLabel(f"Current Slot: {save.selectedSlot}")
        self.topLevelLayout.addWidget(self.currentSlotText)
        
        self.newSlotWidget_ = self.newSlotWidget()
        
        self.topLevelLayout.addWidget(self.autoSaver)
        self.topLevelLayout.addWidget(self.containerWidget)
        self.topLevelLayout.addWidget(self.newSlotWidget_)
        
        self.setLayout(self.topLevelLayout)

    def updateLists(self):
        self.saveDir: str = save.savedir
        
        self.metadataList: dict[int, str] = {}
        self.saveList: dict[int, str] = {}
        
        self.metadata: dict[int, dict] = {}
        
        
        if not len(os.listdir(self.saveDir)) == 0:
            for i in os.listdir(self.saveDir):
                if ".metadata" in i:
                    slotNum = int(i.split(".")[1].split("metadata")[1]) # format is always "metadata.metadata{slotNum}"
                    if slotNum == -1:
                        continue # skip the blanksave slot
                    self.metadataList[slotNum] = i
                elif ".save" in i:
                    slotNum = int(i.split(".")[1].split("save")[1])
                    self.saveList[slotNum] = i

            self.metadataList = dict(sorted(self.metadataList.items()))
            self.saveList = dict(sorted(self.saveList.items()))

            for i in self.metadataList:
                
                self.metadata[i] = save.getSaveMetadataFromFile(i)     
        else:
            pass
    
    def updateDisplayWithLists(self): 
        for i in reversed(range(self.containerLayout.count())):
            widget = self.containerLayout.itemAt(i).widget()
            widget.setParent(None)
            widget.deleteLater()
        
        self.updateLists()
        for i in self.metadata:
            try:
                self.containerLayout.addWidget(self.individualSaveLoadWidget(i, self.metadata[i]))
            except Exception as e:
                dialogs.errorDialog("Failed loading save slot", f"Failed loading save slot {i} with error: {e}").exec()

    def updateDisplay(self):
        self.autoSaver.updateDisplay()
        self.currentSlotText.setText(f"Current Slot: {save.selectedSlot}")
        
    def updateInternal(self):
        self.autoSaver.updateInternal()

class autosaveWidget(QWidget):
    def __init__(self):
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
        self.chooseOption.setCurrentIndex(self.chooseOptionMs.index(gamedefine.autosaveTime))
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
                save.save(notify = False, slot = save.selectedSlot)
            
    def chooseOptionChanged(self):
        gamedefine.autosaveTime = self.chooseOptionMs[self.chooseOption.currentIndex()]
        save.save(notify = False)

    
        
        


class setting(QFrame):
    def __init__(self, setting):
        super().__init__()
        self.thing = setting
        self.updateable = settings[setting]["updates"]
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        
        if not settings[setting]["custom"]:
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
            
            if not settings[setting]["specialAttribute"] == None:

                self.specialAttribute = settings[setting]["specialAttribute"]()
                self.layout_.addWidget(self.specialAttribute, 1, 0) 
            
            self.setLayout(self.layout_)
        else:
            self.containerLayout = QVBoxLayout()
            self.specialAttribute = settings[setting]["specialAttribute"]()
            self.containerLayout.addWidget(self.specialAttribute)
            self.setToolTip(settings[setting]["description"])
            self.setToolTipDuration(5000)
            self.setLayout(self.containerLayout)
            
            
    
    def updateDisplay(self):
        if self.updateable[0]:
            self.specialAttribute.updateDisplay()
    
    def updateInternal(self):
        if self.updateable[1]:
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

settings = {
    # "save": {
    #     "name": "Save",
    #     "description": "Save your progress",
    #     "custom": False, # not fully custom according to the new standards
    #     "action": save_,
    #     "buttonName": "Save",
    #     "specialAttribute": autosaveWidget,
    #     "updates": [True, True], # internalUpdate, displayUpdate
    #     "static": False
    # },
    # "load": {
    #     "name": "Load",
    #     "description": "Load your progress",
    #     "custom": False,
    #     "action": load,
    #     "buttonName": "Load",
    #     "specialAttribute": None,
    #     "updates": [False, False],
    #     "static": False
    # },
    "newSaveLoadSetting": {
        "name": r"Save\Load",
        "description": "Save or load your progress from multiple slots",
        "custom": True,
        "action": None, # there will be custom functions called from within the custom widgets
        "buttonName": None, # again, will be fully custom
        "specialAttribute": saveLoadWidget,
        "updates": [True, True],
        "static": False
    }
}

    