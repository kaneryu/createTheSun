import sympy as sp
import regex as re
import time
from math import floor, ceil, log
import gamedefine
import gameLogic.numberLogic as numberLogic

def getCurrentInternalMultiLevelUpgrade(upgrade: str, level: int | None = None) -> dict:
    
    if level == None:
        target = getCurrentMultiLevelUpgradeIndex(upgrade)
    else:
        target = getCurrentMultiLevelUpgradeIndex(upgrade, level)

    if target == 0:
        return gamedefine.automationInternalDefine[upgrade]["multiLevelUpgrades"][target]
    else:    
        return gamedefine.automationInternalDefine[upgrade]["multiLevelUpgrades"][target]

def getCurrentMultiLevelUpgradeIndex(upgrade: str, level: int | None = None) -> int:
    
    
    if level == None:
        currentLevel = gamedefine.upgradeLevels[upgrade]
    else:
        currentLevel = level
    
    target = -1
    
    for i in gamedefine.automationInternalDefine[upgrade]["multiLevelUpgradesStarts"]:
        if currentLevel >= i:
            target += 1
    
    if target == -1:
        target = 0
        
    return target

def getCurrentVisualMultiLevelUpgrade(upgrade: str, level: int | None = None) -> dict:
    
    if level == None:
        target = getCurrentMultiLevelUpgradeIndex(upgrade)
    else:
        target = getCurrentMultiLevelUpgradeIndex(upgrade, level)

    if target == 0:
        return gamedefine.automationVisualDefine[upgrade][0]
    else:    
        return gamedefine.automationVisualDefine[upgrade][target]

def canAffordUpgradeTask(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade's task.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade's task or not.
    """
    
    if gamedefine.upgradeLevels[upgrade] == 0:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)[1]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["idleGenerator"]["whatItCosts"]
    
        
    ongoing = True
    
    for i in costs:
        if i["amount"] == "atMarketPrice":
            if gamedefine.amounts[i["what"]] < gamedefine.itemInternalDefine[i["what"]]["whatItCosts"][0]["amount"]:
                ongoing = False
        elif gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
    
    return ongoing

def purchaseUpgrade(upgrade : str) -> None:
    """
    Purchases an upgrade.
    
    Args:
        upgrade (str): The upgrade to purchase.
    """
    if gamedefine.upgradeLevels[upgrade] == 0:
        costs = gamedefine.automationInternalDefine[upgrade]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["upgradeCost"]
    
    for i in costs:
        gamedefine.amounts[i["what"]] -= i["amount"]
    gamedefine.upgradeLevels[upgrade] += 1
    
    print(f"purchased {upgrade}, now have {gamedefine.upgradeLevels[upgrade]}")
    return

def updateUpgradeStatus(upgrade : str) -> None:
    """
    Updates the status of a upgrade.
    For example, if you just upgraded protonic forge from level 1-2, the time to wait will be updated to 0.5 instead of 1.
    """
    if gamedefine.upgradeLevels[upgrade] == 0:
        return
    
    currentUpgradeDict = getCurrentInternalMultiLevelUpgrade(upgrade)
    
    if type(currentUpgradeDict) == tuple:
        return #failed, level 0
    if currentUpgradeDict["type"] == "idleGenerator":
        
        idleGenDict = currentUpgradeDict["idleGenerator"]
        
        if idleGenDict["equationType"] == "timeEquation":
            
            gamedefine.upgradeDetails[upgrade]["timeToWait"] = numberLogic.evaluateCostEquation(idleGenDict["timeEquation"], gamedefine.upgradeLevels[upgrade])
            for i in range(len(idleGenDict["whatItGives"])):
                gamedefine.upgradeDetails[upgrade]["whatItGives"][i]["amount"] = idleGenDict["whatItGives"][i]["amount"]
            
            if idleGenDict["withRequirement"]:
                
                for i in range(len(idleGenDict["whatItCosts"])):
                    gamedefine.upgradeDetails[upgrade]["whatItCosts"][i]["amount"] = idleGenDict["whatItCosts"][i]["amount"]
            
        elif idleGenDict["equationType"] == "amountEquation":
            
            gamedefine.upgradeDetails[upgrade]["timeToWait"] = idleGenDict["time"]
            for i in range(len(idleGenDict["whatItGives"])):
                amount = numberLogic.evaluateCostEquation(idleGenDict["amountEquation"][i]["equation"], gamedefine.upgradeLevels[upgrade])
                gamedefine.upgradeDetails[upgrade]["whatItGives"][i]["amount"] = amount
                
            if idleGenDict["withRequirement"]:
                for i in range(len(idleGenDict["whatItCosts"])):
                    amount = numberLogic.evaluateCostEquation(idleGenDict["costEquation"][i], gamedefine.upgradeLevels[upgrade])
                    gamedefine.upgradeDetails[upgrade]["whatItCosts"][i]["amount"] = amount



         
                
                
def canAffordUpgrade(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade or not.
    """
    if gamedefine.upgradeLevels[upgrade] == 0:
        costs = gamedefine.automationInternalDefine[upgrade]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["upgradeCost"]
    
    ongoing = True
    
    for i in costs:
        if gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
    
    return ongoing

def doUpgradeTask(upgrade, lastTickTime):
    if gamedefine.upgradeLevels[upgrade] == 0:
        return lastTickTime
    else:
        internalDefine = getCurrentInternalMultiLevelUpgrade(upgrade)["idleGenerator"]
    if gamedefine.upgradeLevels[upgrade] > 0:
        if time.time() * 1000 - lastTickTime > gamedefine.upgradeDetails[upgrade]["timeToWait"]:
            gamedefine.upgradeDisabledState[upgrade] = (False, "0")
            lastTickTime = time.time() * 1000
            if internalDefine["withRequirement"]:
                if canAffordUpgradeTask(upgrade):
                    for i in gamedefine.upgradeDetails[upgrade]["whatItGives"]:
                        gamedefine.amounts[i["what"]] += i["amount"]
                        
                    for i in gamedefine.upgradeDetails[upgrade]["whatItCosts"]:
                        if i["amount"] == "atMarketPrice":
                            gamedefine.amounts[i["what"]] -= gamedefine.itemInternalDefine[i["what"]]["whatItCosts"][0]["amount"]
                        else:
                            gamedefine.amounts[i["what"]] -= i["amount"]
                else:
                    lastTickTime += 10000 # softlock prevention; add 10 seconds
                    gamedefine.upgradeDisabledState[upgrade] = (True, "10") # type: ignore
            else:         
                for i in gamedefine.upgradeDetails[upgrade]["whatItGives"]:
                    gamedefine.amounts[i["what"]] += i["amount"]
        else:
            if gamedefine.upgradeDisabledState[upgrade][0] == True:
                gamedefine.upgradeDisabledState[upgrade] = (True, str(ceil((gamedefine.upgradeDetails[upgrade]["timeToWait"] - (time.time() * 1000 - lastTickTime))/1000))) # type: ignore
    return lastTickTime
        



def parseCost(name):
    if gamedefine.upgradeLevels[name] == 0:
        what = gamedefine.automationInternalDefine[name]["firstCost"]
        string = ["Purchase for "]    
    else:
        what = getCurrentInternalMultiLevelUpgrade(name)["upgradeCost"]
        string = ["Upgradge for "]                    

                                            
    for i in what:
        string.append(str(i["amount"]) + " ")
        if i["amount"] == 1:
            string.append(i["what"][:-1])
        else:
            string.append(i["what"])
            
        if what.index(i) < len(what) - 2:
            string.append(", ")
        elif what.index(i) == len(what) - 2:
            string.append(" and ")
        else:
            string.append(".")
    
    return "".join(string)


def parseUsefulDescription(upgrade):
    
        if gamedefine.upgradeLevels[upgrade] == 0:
            index = getCurrentMultiLevelUpgradeIndex(upgrade)
            return gamedefine.automationVisualDefine[upgrade][index]["firstupgradeUsefulDescription"]
        else:
            currentVisualDict =  getCurrentVisualMultiLevelUpgrade(upgrade)
            
            currentInternalDict = getCurrentInternalMultiLevelUpgrade(upgrade)

        if currentInternalDict["type"] == "idleGenerator":
            currentDec = currentVisualDict["currentUpgradeUsefulDescription"]
            futureDec = ""
            
            if currentVisualDict["usefulDescriptionBlank"] == "tickTime":
                currentDec = currentDec.replace("%%%", str(round( gamedefine.upgradeDetails[upgrade]["timeToWait"]/1000, 3)))
                
                futureDec = getFutureDescription(upgrade)
                
            elif currentVisualDict["usefulDescriptionBlank"] == "amount":
                currentDec = currentDec.replace("%%%", str(round(gamedefine.upgradeDetails[upgrade]["whatItGives"][0]["amount"], 3)))
                
                futureDec = getFutureDescription(upgrade)
              
            return currentDec + " \n " + futureDec

def getFutureDescription(upgrade):
    
    futureInternalDict = getCurrentInternalMultiLevelUpgrade(upgrade, gamedefine.upgradeLevels[upgrade] + 1)
    futureVisualDict = getCurrentVisualMultiLevelUpgrade(upgrade, gamedefine.upgradeLevels[upgrade] + 1)
    
    if futureInternalDict["type"] == "idleGenerator":
        futureDec = str(futureVisualDict["upgradeUsefulDescription"])
        
        if futureVisualDict["usefulDescriptionBlank"] == "tickTime":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["timeEquation"], gamedefine.upgradeLevels[upgrade] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum/1000, 3)))
        elif futureVisualDict["usefulDescriptionBlank"] == "amount":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["amountEquation"][0]["equation"], gamedefine.upgradeLevels[upgrade] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum, 3)))
        
        return futureDec


def parseUpgradeName(upgrade):
    
    if gamedefine.upgradeLevels[upgrade] == 0:
        
        return gamedefine.automationVisualDefine[upgrade][0]["visualName"]
    else:
        
        currentDict = getCurrentVisualMultiLevelUpgrade(upgrade)
        return f"Level {gamedefine.upgradeLevels[upgrade]} {currentDict["visualName"]} \n {currentDict["description"]} \n"

def getDescription(upgrade):
    index = getCurrentMultiLevelUpgradeIndex(upgrade)
    
    if gamedefine.upgradeLevels[upgrade] == 0:
        return f"{gamedefine.automationVisualDefine[upgrade][index]["upgradeVisualName"]} \n {gamedefine.automationVisualDefine[upgrade][index]["upgradeDescription"]}"
    else:

        return f"{gamedefine.automationVisualDefine[upgrade][index]["upgradeVisualName"]} \n {gamedefine.automationVisualDefine[upgrade][index]["upgradeDescription"]}"