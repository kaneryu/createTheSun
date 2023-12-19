#External Imports
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import os, json, base64, time
from internal_utils import _base64 as base64

#Internal Imports
import mainTab, upgradesTab, version
import game as _game



BLANK_SAVE = version.BLANK_SAVE
saveDict = BLANK_SAVE



def loadSave():
    try:
        app.topLabel.config(text="Loading...")
        time.sleep(1)
    except NameError:
        pass
    global saveDict
    if os.path.exists("save.txt"):
        with open("save.txt", "r") as f:
            save = f.read()
        temp = base64.base64Decode(save)
        saveDict = json.loads(temp)
        
        if not "noSave" in saveDict:
            print("save is not an BTS save file")
            saveDict = _game.gameDict
            
        if not saveDict["gameVersion"] == str(version.version) + "," + str(version.build):
            print("Incorrect Version")
            #saveDict = _game.gameDict
    else:
        
        saveDict = _game.gameDict
        
    _game.gameDict = saveDict 
       
    try:
        app.topLabel.config(text="Create The Sun")
    except NameError:
        pass
    
    return saveDict

def saveSave():
    global saveDict
    
    try:
        app.topLabel.config(text="Saving...")
    except NameError:
        pass
    
    save = json.dumps(_game.gameDict)
    temp = base64.base64Encode(save)
    with open("save.txt", "w") as f:
        f.write(temp)
        
    try:
        app.topLabel.config(text="Create The Sun")
    except NameError:
        pass

class Applicaton(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        global saveDict
        
        loadSave()
        saveDict = _game.gameDict
        
        print(f"loaded save: {_game.gameDict["noSave"]}")
        
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.topFrame = ttk.Frame(self.master)
        self.topLabel = ttk.Label(self.topFrame, text="Create The Sun")
        self.topFrame.pack()
        self.topLabel.pack()
        
        self.master = master
        self.menu = tk.Menu(self.master)
        self.menu.add_command(label="Save", command = saveSave)
        self.menu.add_command(label="Load", command = loadSave)



        notebook = ttk.Notebook(master)
        
        self.mainTabFrame = mainTab.mainTab(notebook)
        self.upgradesTabFrame = upgradesTab.upgradesTab(notebook)
        

        notebook.add(self.mainTabFrame, text="Main")
        notebook.add(self.upgradesTabFrame, text="Upgrades")
        notebook.pack(fill = "both", expand = True)
        
        
        

def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to save before you quit?"):
        saveSave()
        root.destroy()
    else:
        root.destroy()
        
root = tk.Tk()
root.title("Create The Sun")
root.geometry("500x500")
root.resizable(False, False)
root.iconbitmap("icon.ico")

app = Applicaton(root)

print(app.mainTabFrame.children)
root.protocol("WM_DELETE_WINDOW", onClosing)

root.config(menu=app.menu)
app.pack()
gameThread = Thread(target = _game.game)

_game.running = True
_game.hasEverBeenTrue = True
gameThread.start()
def takeNoTime():
    
    root.after(10, takeNoTime)
    pass

root.after(1, takeNoTime)
root.mainloop()
_game.running = False