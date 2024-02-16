import gamedefine
import copy
import os
import pathlib
import json
import base64
import unlocks
import time

from PyQt6.QtWidgets import QDialog


from customWidgets import dialogs


save_ = {}
rootdir = pathlib.Path(__file__).parent
selectedSlot = 0


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

def save(export: bool = False, exportEncoded: bool = False, notify: bool = True, slot: int = 0, noProgSaveCreation: bool = False, blank: bool = False): # type: ignore
    def removeExtraLastUsedFiles(slot: int):
        previousLastUsed = [i for i in os.listdir(savedir) if f"lastused{slot}" in i.split(".")[1]]
        for i in previousLastUsed:
            os.remove(os.path.join(savedir, i))
            
    operationSucsess = dialogs.popupNotification("Saved", "Saving Complete")
    areYouSureDialog = dialogs.yesNoDialog( "Save", "Are you sure you want to save? This will overwrite the current save in that slot.", preventClose_ = True)
    global selectedSlot
    
    if slot != selectedSlot:
        areYouSureDialog.exec()
        if areYouSureDialog.result() == QDialog.DialogCode.Rejected:
            return
    
    gamedefine.playTime += time.time() - gamedefine.sessionStartTime
    
    if noProgSaveCreation:
        slot = -1
        
    if not blank:
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
        
        print(f"saving to slot {slot} with save {save_}")
        
        if not os.path.exists(savedir):
            os.makedirs(savedir)
            
            
        savefile = os.path.join(savedir, f"save.save{slot}")
        saveMetadataFile = os.path.join(savedir, f"metadata.metadata{slot}")
        lastUsedFile = os.path.join(savedir, f"{time.time()}.lastused{slot}")
        saveMetadata = json.dumps(gamedefine.getSaveMetadata())

        
        with open(savefile, "w") as f:
            f.write(encodedSave)
        
        with open(saveMetadataFile, "w") as f:
            f.write(saveMetadata)
        
        removeExtraLastUsedFiles(slot)
            
        with open(lastUsedFile, "w") as f:
            f.write("why u here...")
            
        if notify:
            operationSucsess.exec()
            
    else:
        blankSave = os.path.join(savedir, f"save.save-1")
        blankmetadata = os.path.join(savedir, f"metadata.metadata-1")
        
        newSave = os.path.join(savedir, f"save.save{slot}")
        newmetadata = os.path.join(savedir, f"metadata.metadata{slot}")
        
        blankSaveFile = open(blankSave, "r")
        blankmetadataFile = open(blankmetadata, "r")
        
        with open(newSave, "w") as f:
            f.write(blankSaveFile.read())
        
        with open(newmetadata, "w") as f:
            f.write(blankmetadataFile.read())
        
        blankSaveFile.close()
        blankmetadataFile.close()
        
    gamedefine.sessionStartTime = time.time()
    

def getSaveMetadataFromFile(slot: int = 0 ) -> dict:
    file = os.path.join(savedir, f"metadata.metadata{slot}")
    if os.path.exists(file):
        with open(file, 'r') as f:
            metadata: dict = json.loads(f.read())

        return metadata
    else:
        return {None:None}
        

def load(slot: int = 0, noSpeak = False, loadWarn = True, save = None):
    
    dialog = dialogs.yesNoDialog( "Load", "Are you sure you want to load? This will overwrite your current save.", preventClose_ = True)
    saveNotFoundDialog = dialogs.warningDialog("No save found", "There was no save found.")
    operationSucsess = dialogs.popupNotification("Loaded", "Loading Complete")
    
    if save == None:
        if not os.path.exists(savedir):
            saveNotFoundDialog.exec()
            return
        
        if loadWarn:
            if dialog.exec() == QDialog.DialogCode.Rejected:
                return
            
        savefile = os.path.join(savedir, f"save.save{slot}")
        
        if not os.path.exists(savefile):
            return
        
        with open(savefile, "r") as f:
            save_ = json.loads(b64Decode(f.read()))
    else:
        save_ = save
    
    gamedefine.loadSave(save_)
    gamedefine.force = 1
    
    for i in gamedefine.unlockedUnlockables:
        unlocks.unlock(i)
        
    global selectedSlot
    selectedSlot = slot
    
    gamedefine.sessionStartTime = time.time() * 1000
    if not noSpeak:
        operationSucsess.exec()
    
    
def getLastUsedSaveSlot() -> int:
    if not os.path.exists(savedir):
        return 0
    
    files = os.listdir(savedir)
    files = [i for i in files if ".lastused" in i]
    if len(files) == 0:
        return 0
    
    best = 0
    timeOfBest = 0
    for i in files:
        if int(i.split(".lastused")[0]) > timeOfBest:
            best = int(i.split(".lastused")[1])
            timeOfBest = int(i.split(".lastused")[0])
    
    return best
    
def getHighestSaveSlot() -> int:
    if not os.path.exists(savedir):
        return 0
    
    files = os.listdir(savedir)
    files = [i for i in files if "save" in i]
    if len(files) == 0:
        return 0
    
    best = 0
    for i in files:
        if int(i.split(".save")[1]) > best:
            best = int(i.split(".save")[1])
    
    return best

def getLastUsedTime(slot: int = 0) -> int:
    if not os.path.exists(savedir):
        return 0
    
    files = os.listdir(savedir)
    files = [i for i in files if f".lastused{slot}" in i]
        
    if len(files) == 0:
        return 0
    
    return int(files[0].split(".")[0])

    
