import gamedefine
import copy
import os
import pathlib
import json
import base64

from PyQt6.QtWidgets import QDialog


from customWidgets import dialogs


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

def save(export = False, exportEncoded = False, notify = True):
    operationSucsess = dialogs.popupNotification("Saved", "Saving Complete")
    
    save_ = gamedefine.getSaveData()
    try:
        encodedSave = b64Encode(json.dumps(save_))
    except Exception as e:
        dialogs.errorDialog("Error", f"There was an error saving your game. Please report this to the developer:\n{e}").exec()
        gamedefine.autosaveTime = -1
        return
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
    
    if notify:
        operationSucsess.exec()
    
def load(noSpeak = False, loadWarn = True, save = None):
    dialog = dialogs.yesNoDialog( "Load", "Are you sure you want to load? This will overwrite your current save.", preventClose_ = True)
    saveNotFoundDialog = dialogs.warningDialog("No save fould", "There was no save found.")
    operationSucsess = dialogs.popupNotification("Loaded", "Loading Complete")
    
    if save == None:
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
    else:
        save_ = save
    
    gamedefine.loadSave(save_)
    gamedefine.force = 1
    
    if not noSpeak:
        operationSucsess.exec()
    

