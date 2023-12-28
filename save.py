import gamedefine
import copy
from PyQt6.QtCore import QSaveFile
import os
import json

save_ = {}


def save():
    for i in gamedefine.saveable:
        save_[gamedefine.saveableStr[gamedefine.saveable.index(i)]] = json.dumps(i)
    
    appdata = os.environ["APPDATA"]
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    savefile = os.path.join(savedir, "save.json")
    with open(savefile, "w") as f:
        json.dump(save_, f)
    
    
def load():
    appdata = os.environ["APPDATA"]
    savedir = os.path.join(appdata, "CreateTheSun", "Saves")
    if not os.path.exists(savedir):
        return
    savefile = os.path.join(savedir, "save.json")
    if not os.path.exists(savefile):
        return
    with open(savefile, "r") as f:
        save_ = json.load(f)
    
    for i in save_:

        gamedefine.saveable[gamedefine.saveableStr.index(i)] = copy.deepcopy(save_[i])
        