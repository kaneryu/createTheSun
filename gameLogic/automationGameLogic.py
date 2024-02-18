import sympy as sp
import time
from math import floor, ceil, log
import gamedefine
import gameLogic.numberLogic as numberLogic
import resourceGain

def getCurrentInternalMultiLevelUpgrade(upgrade: str, level: int | None = None) -> dict:
    
    if level == None:
        target = getCurrentMultiLevelUpgradeIndex(upgrade)
    else:
        target = getCurrentMultiLevelUpgradeIndex(upgrade, level)

    if target == 0:
        return gamedefine.gamedefine.automationInternalDefine[upgrade]["multiLevelUpgrades"][target]
    else:    
        return gamedefine.gamedefine.automationInternalDefine[upgrade]["multiLevelUpgrades"][target]

def getCurrentMultiLevelUpgradeIndex(upgrade: str, level: int | None = None) -> int:
    
    
    if level == None:
        currentLevel = gamedefine.gamedefine.automationLevels[upgrade]
    else:
        currentLevel = level
    
    target = -1
    
    for i in gamedefine.gamedefine.automationInternalDefine[upgrade]["multiLevelUpgradesStarts"]:
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
        return gamedefine.gamedefine.automationVisualDefine[upgrade][0]
    else:    
        return gamedefine.gamedefine.automationVisualDefine[upgrade][target]

def canAffordUpgradeTask(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade's task.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade's task or not.
    """
    
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)[1]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["idleGenerator"]["whatItCosts"]
    
        
    ongoing = True
    
    for i in costs:
        if i["amount"] == "atMarketPrice":
            if gamedefine.gamedefine.amounts[i["what"]] < gamedefine.gamedefine.itemInternalDefine[i["what"]]["whatItCosts"][0]["amount"]:
                ongoing = False
        elif gamedefine.gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
    
    return ongoing

def purchaseUpgrade(upgrade : str) -> None:
    """
    Purchases an upgrade.
    
    Args:
        upgrade (str): The upgrade to purchase.
    """
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        costs = gamedefine.gamedefine.automationInternalDefine[upgrade]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["upgradeCost"]
        
    index = 0
    for i in costs:
        gamedefine.gamedefine.amounts[i["what"]] -= getCostWithIndex(index, upgrade)
        index += 1 
    gamedefine.gamedefine.automationLevels[upgrade] += 1
    
    print(f"purchased {upgrade}, now have {gamedefine.gamedefine.automationLevels[upgrade]}")
    return

def updateUpgradeStatus(upgrade : str) -> None:
    """
    Updates the status of a upgrade.
    For example, if you just upgraded protonic forge from level 1-2, the time to wait will be updated to 0.5 instead of 1.
    """
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        return
    
    currentUpgradeDict = getCurrentInternalMultiLevelUpgrade(upgrade)
    
    if type(currentUpgradeDict) == tuple:
        return #failed, level 0
    if currentUpgradeDict["type"] == "idleGenerator":
        
        idleGenDict = currentUpgradeDict["idleGenerator"]
        
        if idleGenDict["equationType"] == "timeEquation":
            
            gamedefine.gamedefine.automationDetails[upgrade]["timeToWait"] = numberLogic.evaluateCostEquation(idleGenDict["timeEquation"], gamedefine.gamedefine.automationLevels[upgrade]) 
            for i in range(len(idleGenDict["whatItGives"])):
                gamedefine.gamedefine.automationDetails[upgrade]["whatItGives"][i]["amount"] = idleGenDict["whatItGives"][i]["amount"]
            
            if idleGenDict["withRequirement"]:
                
                for i in range(len(idleGenDict["whatItCosts"])):
                    gamedefine.gamedefine.automationDetails[upgrade]["whatItCosts"][i]["amount"] = idleGenDict["whatItCosts"][i]["amount"]
            
        elif idleGenDict["equationType"] == "amountEquation":
            
            gamedefine.gamedefine.automationDetails[upgrade]["timeToWait"] = idleGenDict["time"]
            for i in range(len(idleGenDict["whatItGives"])):
                amount = numberLogic.evaluateCostEquation(idleGenDict["amountEquation"][i]["equation"], gamedefine.gamedefine.automationLevels[upgrade])
                gamedefine.gamedefine.automationDetails[upgrade]["whatItGives"][i]["amount"] = amount
                
            if idleGenDict["withRequirement"]:
                for i in idleGenDict["whatItCosts"]:
                    try:
                        i["equation"]
                    except KeyError:
                        continue
                    amount = numberLogic.evaluateCostEquation(i["equation"], gamedefine.gamedefine.automationLevels[upgrade])
                    i["amount"] = amount



         
                
                
def canAffordUpgrade(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade or not.
    """
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        costs = gamedefine.gamedefine.automationInternalDefine[upgrade]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["upgradeCost"]
    
    ongoing = True
    index = 0
    for i in costs:
        if gamedefine.gamedefine.amounts[i["what"]] < getCostWithIndex(index, upgrade):
            ongoing = False
            
        index += 1 
    
    return ongoing

def checkIfUpgradeIsAffordable(automation : str) -> bool:
    """
    Checks if you can afford an upgrade, according to how many of the required item is being produced.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade or not.
    """
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        costs = gamedefine.gamedefine.automationInternalDefine[automation]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(automation)["upgradeCost"]
    
    waittime = gamedefine.gamedefine.automationDetails[automation]["timeToWait"]
    
    costsPerSecond = {}
    ongoing = True
    index = 0
    
    
    
    for i in costs:
        if costs[i]["what"] in list(resourceGain.data.gainPerSecond.keys()):
            if getCostWithIndex(index, automation) / (waittime / 1000) > resourceGain.data.gainPerSecond[i]:
                ongoing = False
        else:
            print(f"Error: {i} is not in resourceGain.data.gainPerSecond, so cannot be calculated for automation {automation}.")
            
        index += 1 
    
    return ongoing

def doUpgradeTask(upgrade, lastTickTime):
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        return lastTickTime
    else:
        internalDefine = getCurrentInternalMultiLevelUpgrade(upgrade)["idleGenerator"]
        
    if gamedefine.gamedefine.automationLevels[upgrade] > 0:
        
        if time.time() * 1000 - lastTickTime > gamedefine.gamedefine.automationDetails[upgrade]["timeToWait"]:
            gamedefine.gamedefine.automationDisabledState[upgrade] = [False, "0"]
            lastTickTime = time.time() * 1000
            
            if not internalDefine["withRequirement"]:     
                for i in gamedefine.gamedefine.automationDetails[upgrade]["whatItGives"]:
                    gamedefine.gamedefine.amounts[i["what"]] += int(i["amount"])
                return lastTickTime
        
            if internalDefine["withRequirement"]:
                
                if not checkIfUpgradeIsAffordable(upgrade):
                    gamedefine.gamedefine.automationDisabledState[upgrade] = [True]
                    return
                
                if canAffordUpgradeTask(upgrade):
                    for i in gamedefine.gamedefine.automationDetails[upgrade]["whatItGives"]:
                        gamedefine.gamedefine.amounts[i["what"]] += int(i["amount"])
                        
                    for i in gamedefine.gamedefine.automationDetails[upgrade]["whatItCosts"]:
                        if i["amount"] == "atMarketPrice":
                            gamedefine.gamedefine.amounts[i["what"]] -= int(gamedefine.gamedefine.itemInternalDefine[i["what"]]["whatItCosts"][0]["amount"])
                        else:
                            gamedefine.gamedefine.amounts[i["what"]] -= int(i["amount"])
                else:
                    lastTickTime += 10000 # softlock prevention; add 10 seconds
                    gamedefine.gamedefine.automationDisabledState[upgrade] = [True]
                
    return lastTickTime
        

def getCostWithIndex(index: int, automation: str) -> int:
    
    what: list
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        what = gamedefine.gamedefine.automationInternalDefine[automation]["firstCost"]
    else:
        what = getCurrentInternalMultiLevelUpgrade(automation)["upgradeCost"]
    
    if index > len(what) - 1:
        raise IndexError(f"Index {index} is incompatible with list {what}.")
    if index < 0:
        raise IndexError(f"Index cannot be less than one, but Index is {index}.")
    
    item = what[index]
    
    if type(item["amount"]) == str:
        variablelist = []
        
        for i in item["variables"]:
            
            if i == "level":
                variablelist.append(gamedefine.gamedefine.automationLevels[automation])
            
        result = numberLogic.evaluateCostEquation(item["amount"], arglist = variablelist)
 
        result = round(result)
        
    elif type(item["amount"]) == int:
        result = item["amount"]
        
    else:
        raise TypeError(f"Type of amount in upgrade {automation} with level {gamedefine.gamedefine.automationLevels[automation]} has the wrong type.")
    
    return result
    
def parseCost(name):
    if gamedefine.gamedefine.automationLevels[name] == 0:
        what = gamedefine.gamedefine.automationInternalDefine[name]["firstCost"]
        string = ["Purchase for "]    
    else:
        what = getCurrentInternalMultiLevelUpgrade(name)["upgradeCost"]
        string = ["Upgradge for "]                    

    index = 0                             
    for i in what:
        cost = getCostWithIndex(index, name)
        string.append(str(cost) + " ")
        if cost == 1:
            string.append(i["what"][:-1])
        else:
            string.append(i["what"])
            
        if what.index(i) < len(what) - 2:
            string.append(", ")
        elif what.index(i) == len(what) - 2:
            string.append(" and ")
        else:
            string.append(".")
    
        index += 1
    return "".join(string)


def parseUsefulDescription(upgrade) -> str:
        if gamedefine.gamedefine.automationLevels[upgrade] == 0:
            index = getCurrentMultiLevelUpgradeIndex(upgrade)
            return gamedefine.gamedefine.automationVisualDefine[upgrade][index]["firstupgradeUsefulDescription"]
        else:
            currentVisualDict =  getCurrentVisualMultiLevelUpgrade(upgrade)
            
            currentInternalDict = getCurrentInternalMultiLevelUpgrade(upgrade)

        if currentInternalDict["type"] == "idleGenerator":
            currentDec = currentVisualDict["currentUpgradeUsefulDescription"]
            futureDec = ""
            
            if currentVisualDict["usefulDescriptionBlank"] == "tickTime":
                currentDec = currentDec.replace("%%%", str(round( gamedefine.gamedefine.automationDetails[upgrade]["timeToWait"]/1000, 3)))
                
                futureDec = getFutureDescription(upgrade)
                
            elif currentVisualDict["usefulDescriptionBlank"] == "amount":
                currentDec = currentDec.replace("%%%", str(round(gamedefine.gamedefine.automationDetails[upgrade]["whatItGives"][0]["amount"])))
                
                futureDec = getFutureDescription(upgrade)
            
            
            return currentDec + " \n " + futureDec
        
        return ""

def getFutureDescription(upgrade):
    
    futureInternalDict = getCurrentInternalMultiLevelUpgrade(upgrade, gamedefine.gamedefine.automationLevels[upgrade] + 1)
    futureVisualDict = getCurrentVisualMultiLevelUpgrade(upgrade, gamedefine.gamedefine.automationLevels[upgrade] + 1)
    
    if futureInternalDict["type"] == "idleGenerator":
        futureDec = str(futureVisualDict["upgradeUsefulDescription"])
        
        if futureVisualDict["usefulDescriptionBlank"] == "tickTime":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["timeEquation"], gamedefine.gamedefine.automationLevels[upgrade] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum/1000, 3)))
        elif futureVisualDict["usefulDescriptionBlank"] == "amount":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["amountEquation"][0]["equation"], gamedefine.gamedefine.automationLevels[upgrade] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum)))
        
        return futureDec


def parseUpgradeName(upgrade):
            
    currentDict = getCurrentVisualMultiLevelUpgrade(upgrade)
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        return f"{currentDict["visualName"]} \n {currentDict["description"]} \n"
    else:
        return f"Level {gamedefine.gamedefine.automationLevels[upgrade]} {currentDict["visualName"]} \n {currentDict["description"]} \n"

def getDescription(upgrade):
    index = getCurrentMultiLevelUpgradeIndex(upgrade)
    
    if gamedefine.gamedefine.automationLevels[upgrade] == 0:
        return f""
    else:

        return f"{gamedefine.gamedefine.automationVisualDefine[upgrade][index]["upgradeVisualName"]} \n {gamedefine.gamedefine.automationVisualDefine[upgrade][index]["upgradeDescription"]}"