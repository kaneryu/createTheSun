import gamedefine
import copy
from PyQt6.QtCore import QSaveFile
import os
import pathlib
import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QVBoxLayout
import base64


save_ = {}
rootdir = pathlib.Path(__file__).parent

if os.path.exists(os.path.join(rootdir, "_internal")): #if the application has been compiled into an exe
    appdata = os.environ["APPDATA"]
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
else:
    appdata = os.path.join(rootdir, "appdata\\local")
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    
def b64Encode(what: str) -> str:
    return base64.b64encode(what.encode("utf-8")).decode("utf-8")

def b64Decode(what: str) -> str:
    return base64.b64decode(what.encode("utf-8")).decode("utf-8")

def lookForSave():
    savefilepath = os.path.join(savedir, "save.save1")
    if os.path.exists(savefilepath):
        return True

    return False

def save(export = False, exportEncoded = False):
    operationSucsess = CustomDialog("Saving Complete", "Saved")
    save_ = gamedefine.getSaveData()
    encodedSave = b64Encode(json.dumps(save_))
    
    if export:
        if exportEncoded:
            return encodedSave
        else:
            return save_
        
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    savefile = os.path.join(savedir, "save.save1")
    with open(savefile, "w") as f:
        f.write(encodedSave)
    operationSucsess.exec()
    
def load(noSpeak = False, loadWarn = True):
    dialog = CustomDialog("Are you sure you want to load? This will overwrite your current save.", "Load", True)
    saveNotFoundDialog = CustomDialog("There was no save found.", "No save fould", False)
    operationSucsess = CustomDialog("Saving Complete", "Saved")
    
    if not os.path.exists(savedir):
        saveNotFoundDialog.exec()
        return
    
    if loadWarn:
        if dialog.exec() == QDialog.DialogCode.Rejected:
            return
        
    savefile = os.path.join(savedir, "save.save1")
    
    if not os.path.exists(savefile):
        return
    
    with open(savefile, "r") as f:
        save_ = json.loads(b64Decode(f.read()))
    
    gamedefine.loadSave(save_)
    gamedefine.force = 1
    
    if not noSpeak:
        operationSucsess.exec()
    
class CustomDialog(QDialog):
    def __init__(self, text, windowTitle = "Dialog", cancelable = True, customQBtn = None ):
        super().__init__()

        self.setWindowTitle(windowTitle)
        if customQBtn == None:
            if cancelable == True:
                QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            else:
                QBtn = QDialogButtonBox.StandardButton.Ok
        else:
            QBtn = customQBtn

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_ = QVBoxLayout()
        message = QLabel(text)
        self.layout_.addWidget(message)
        self.layout_.addWidget(self.buttonBox)   
        self.setLayout(self.layout_)
        
