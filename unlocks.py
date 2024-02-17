from observerModel import registerObserver, Observable, ObservableCallType

from gamedefine import gamedefine
from tabs import achevementsTab

import time

unlockables = gamedefine.unlockables
unlockedUnlockables = gamedefine.unlockedUnlockables

def checkUnlocks(event):
    for key in unlockables:
        ongoingCheck = True
        currentDict = unlockables[key]
        if not key in unlockedUnlockables:
            for item in currentDict["needs"]: #type: ignore
                if item["type"] == "item": #type: ignore
                    if not gamedefine.amounts[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                
                if item["type"] == "automation": #type: ignore
                    if not gamedefine.automationLevels[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
            
            if ongoingCheck == True and not key in gamedefine.unlockedUnlockables:
                gamedefine.unlockedUnlockables.append(key)
                unlock(key)         
                
def unlock(key):
    currentDict = unlockables[key]
    if currentDict["unlockType"] == "item":
        gamedefine.purchaseToCreate.append(currentDict["whatUnlocks"]) #type: ignore
    
    
def checkAchevements(event):
    for i in gamedefine.achevementInternalDefine:
        if not i in gamedefine.unlockedAchevements:
            
            ongoingCheck = True
            currentDict = gamedefine.achevementInternalDefine[i]
            for item in currentDict["whatItRequires"]: #type: ignore
                if item["type"] == "item": #type: ignore
                    if not gamedefine.amounts[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                
                if item["type"] == "automation": #type: ignore
                    if not gamedefine.automationLevels[item["what"]] >= item["amount"]: #type: ignore
                        ongoingCheck = False
                        
                if item["type"] == "rewrite":
                    if not item["what"] in gamedefine.unlockedRewrites:
                        ongoingCheck = False
            
            if ongoingCheck == True:
                print(f"Achevement Get! {i}")
                gamedefine.unlockedAchevements.append(i)
                gamedefine.lastAchevementGain = (i, time.time() * 1000)
                achevementsTab.achevementPopup(i)

def reciever(event):
    checkUnlocks(event)
    checkAchevements(event)

itemObserver = registerObserver(reciever, Observable.ITEM_OBSERVABLE, ObservableCallType.ALL)
automationObserver = registerObserver(reciever, Observable.AUTOMATION_OBSERVABLE, ObservableCallType.ALL)