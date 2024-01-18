from observerModel import newObserver, Observable
from gamedefine import unlockables, unlockedUnlockables
import gamedefine


def checkUnlocks(event):
    print(event)
    for key in unlockables:
        ongoingCheck = True
        if not key in unlockedUnlockables:
            for item in key["needs"]: #type: ignore
                if item["type"] == "item": #type: ignore
                    if not gamedefine.amounts["item"] >= item["amount"] #type: ignore
                        ongoingCheck = False
                
                if item["type"] == "automation": #type: ignore
                    if not gamedefine.automationLevels >= item["amount"] #type: ignore
                        ongoingCheck = False
            
            if ongoingCheck == True:
                unlock(key)         
                
def unlock(key):
    unlockable = unlockables[key]
    if unlockable["type"] == "item":
        gamedefine.purchaseToCreate.append[key["whatUnlocks"]] #type: ignore
    

newObserver(checkUnlocks, Observable.ITEM_OBSERVABLE, Observable.GAINED)
newObserver(checkUnlocks, Observable.AUTOMATION_OBSERVABLE, Observable.GAINED)