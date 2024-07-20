from .observerModel import registerObserver, Observable, ObservableCallType, callEvent
from .customWidgets import dialogs
import gamedefine
from tabs import achevementsTab

import time

unlockables = gamedefine.gamedefine.unlockables
unlockedUnlockables = gamedefine.gamedefine.unlockedUnlockables

def checkUnlocks(event):
    for key in unlockables:
        ongoingCheck = True
        currentDict = unlockables[key]
        if not key in unlockedUnlockables:
            for item in currentDict["needs"]: #type: ignore
                if item["type"] == "item": #type: ignore
                    if not gamedefine.gamedefine.amounts[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                
                if item["type"] == "automation": #type: ignore
                    if not gamedefine.gamedefine.automationLevels[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
            
            if ongoingCheck == True and not key in gamedefine.gamedefine.unlockedUnlockables:
                unlock(key)         
                
def unlock(key, force = False):
    currentDict = unlockables[key]
    if not force:
        if key in gamedefine.gamedefine.unlockedUnlockables:
            return
    
    if currentDict["unlockType"] == "item":
        gamedefine.gamedefine.unlockedUnlockables.append(key)

        if not currentDict["whatUnlocks"] in gamedefine.gamedefine.purchaseToCreate:
            gamedefine.gamedefine.purchaseToCreate.append(currentDict["whatUnlocks"]) #type: ignore
            callEvent(Observable.RESET_OBSERVABLE, ObservableCallType.GAINED, f"mainTab")
    
    if not currentDict["makeVisible"] == None:
        for i in currentDict["makeVisible"]:
            gamedefine.gamedefine.unlockables[i]["visible"] = True
            callEvent(Observable.RESET_OBSERVABLE, ObservableCallType.GAINED, f"unlockTab")
    
    currentDict["visible"] = False # no need to show it anymore, it's unlocked
    
def checkAchevements(event):
    for i in gamedefine.gamedefine.achevementInternalDefine:
        if not i in gamedefine.gamedefine.unlockedAchevements:
            
            ongoingCheck = True
            currentDict = gamedefine.gamedefine.achevementInternalDefine[i]
            for item in currentDict["whatItRequires"]: #type: ignore
                if item["type"] == "item": #type: ignore
                    if not gamedefine.gamedefine.amounts[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                
                if item["type"] == "automation": #type: ignore
                    if not gamedefine.gamedefine.automationLevels[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                        
                if item["type"] == "rewrite":
                    if not item["what"] in gamedefine.gamedefine.unlockedRewrites:
                        ongoingCheck = False
            
            if ongoingCheck == True:
                print(f"Achevement Get! {i}")
                gamedefine.gamedefine.unlockedAchevements.append(i)
                gamedefine.gamedefine.lastAchevementGain = [i, time.time() * 1000]
                achevementsTab.achevementPopup(i)

def reciever(event):
    checkUnlocks(event)
    checkAchevements(event)

def firstQuarkPopup(event):
    if gamedefine.gamedefine.amounts["quarks"] >= 1 and gamedefine.gamedefine.tutorialPopupDone == False:
        gamedefine.gamedefine.tutorialPopupDone = True
        print("First Quark Popup")
        dialogs.CustomDialog(f"## Welcome to Create The Sun! Check out the Goals and Automation tabs.", "Tutorial", cancelable = False).exec()
        firstQuarkPopupObserver.deregister()
        
itemObserver = registerObserver(reciever, Observable.ITEM_OBSERVABLE, ObservableCallType.ALL)
automationObserver = registerObserver(reciever, Observable.AUTOMATION_OBSERVABLE, ObservableCallType.ALL)
firstQuarkPopupObserver = registerObserver(firstQuarkPopup, Observable.ITEM_OBSERVABLE, ObservableCallType.GAINED)