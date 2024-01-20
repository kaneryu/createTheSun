from observerModel import newObserver, Observable, ObservableCallType
from gamedefine import unlockables, unlockedUnlockables
import gamedefine


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
    

newObserver(checkUnlocks, Observable.ITEM_OBSERVABLE, ObservableCallType.TIME)
newObserver(checkUnlocks, Observable.AUTOMATION_OBSERVABLE, ObservableCallType.TIME)