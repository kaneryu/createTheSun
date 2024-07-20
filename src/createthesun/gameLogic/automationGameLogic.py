import time
from math import ceil, floor, log

import sympy as sp

from .. import gamedefine, resourceGain
from . import numberLogic


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
    
def checkIfAutomationIsAffordable(automation : str) -> bool:
    """
    Checks if you can afford an automation, according to how many of the required item is being produced.
    
    Args:
        automation (str): The automation to check
    
    Returns:
        bool: Whether you can afford the upgrade or not.
    """
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        costs = getCurrentInternalMultiLevelUpgrade(automation)[1]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(automation)["idleGenerator"]["whatItCosts"]
    
    waittime = gamedefine.gamedefine.automationDetails[automation]["timeToWait"]
    
    ongoing = True
    index = 0
    
    for i in costs:
        if i["what"] in list(resourceGain.data.gainPerSecond.keys()):
            if i["amount"] == "atMarketPrice":
                itemToCheckFor = getCurrentInternalMultiLevelUpgrade(automation)["idleGenerator"]["whatItGives"][0]["what"]
                price = int(gamedefine.gamedefine.itemInternalDefine[itemToCheckFor]["whatItCosts"][0]["amount"])
                # print(gamedefine.gamedefine.itemInternalDefine[itemToCheckFor]["whatItCosts"][0]["amount"])
            else:
                price = int(i["amount"])
                
            if price / (waittime / 1000) > resourceGain.data.gainPerSecond[i["what"]]:
                ongoing = False
        else:
            print(f"{i} is not in resourceGain.data.gainPerSecond, so cannot be calculated for automation {automation}.")
            
        index += 1 
    # print(f"{price}price {waittime}waittime {price / (waittime / 1000)}eq {resourceGain.data.gainPerSecond[i["what"]]}resgainpersec")
    # print(f"can {automation} be afforded? {"yes" if ongoing else "no"}")
    return ongoing

def canAffordAutomationTask(automation : str) -> bool:
    """
    Checks if you can afford an automation's task.
    
    Args:
        automation (str): The automation to check
    
    Returns:
        bool: Whether you can afford the automation's task or not.
    """
    
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        costs = getCurrentInternalMultiLevelUpgrade(automation)[1]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(automation)["idleGenerator"]["whatItCosts"]
    
        
    ongoing = True
    
    for i in costs:
        if i["amount"] == "atMarketPrice":
            if gamedefine.gamedefine.amounts[i["what"]] < gamedefine.gamedefine.itemInternalDefine[i["what"]]["whatItCosts"][0]["amount"]:
                ongoing = False
        elif gamedefine.gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
            
    return ongoing

def purchaseAutomation(automation : str) -> None:
    """
    Purchases an automation.
    
    Args:
        automation (str): The automation to purchase.
    """
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        costs = gamedefine.gamedefine.automationInternalDefine[automation]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(automation)["upgradeCost"]
        
    index = 0
    for i in costs:
        gamedefine.gamedefine.amounts[i["what"]] -= getCostWithIndex(index, automation)
        index += 1 
    gamedefine.gamedefine.automationLevels[automation] += 1
    
    print(f"purchased {automation}, now have {gamedefine.gamedefine.automationLevels[automation]}")
    return

def updateAutomationStatus(automation : str) -> None:
    """
    Updates the status of a automation.
    For example, if you just upgraded protonic forge from level 1-2, the time to wait will be updated to 0.5 instead of 1.
    """
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        return
    
    currentUpgradeDict = getCurrentInternalMultiLevelUpgrade(automation)
    
    if type(currentUpgradeDict) == tuple:
        return #failed, level 0
    if currentUpgradeDict["type"] == "idleGenerator":
        
        idleGenDict = currentUpgradeDict["idleGenerator"]
        
        if idleGenDict["equationType"] == "timeEquation":
            
            gamedefine.gamedefine.automationDetails[automation]["timeToWait"] = numberLogic.evaluateCostEquation(idleGenDict["timeEquation"], gamedefine.gamedefine.automationLevels[automation]) 
            for i in range(len(idleGenDict["whatItGives"])):
                gamedefine.gamedefine.automationDetails[automation]["whatItGives"][i]["amount"] = idleGenDict["whatItGives"][i]["amount"]
            
            if idleGenDict["withRequirement"]:
                
                for i in range(len(idleGenDict["whatItCosts"])):
                    gamedefine.gamedefine.automationDetails[automation]["whatItCosts"][i]["amount"] = idleGenDict["whatItCosts"][i]["amount"]
            
        elif idleGenDict["equationType"] == "amountEquation":
            
            gamedefine.gamedefine.automationDetails[automation]["timeToWait"] = idleGenDict["time"]
            for i in range(len(idleGenDict["whatItGives"])):
                amount = numberLogic.evaluateCostEquation(idleGenDict["amountEquation"][i]["equation"], gamedefine.gamedefine.automationLevels[automation])
                gamedefine.gamedefine.automationDetails[automation]["whatItGives"][i]["amount"] = amount
                
            if idleGenDict["withRequirement"]:
                for i in idleGenDict["whatItCosts"]:
                    try:
                        i["equation"]
                    except KeyError:
                        continue
                    amount = numberLogic.evaluateCostEquation(i["equation"], gamedefine.gamedefine.automationLevels[automation])
                    i["amount"] = amount



    
                
def canAffordAutomation(automation : str) -> bool:
    """
    Checks if you can afford an automation.
    
    Args:
        automation (str): The automation to check
    
    Returns:
        bool: Whether you can afford the automation or not.
    """
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        costs = gamedefine.gamedefine.automationInternalDefine[automation]["firstCost"]
    else:
        costs = getCurrentInternalMultiLevelUpgrade(automation)["upgradeCost"]
    
    ongoing = True
    index = 0
    for i in costs:
        if gamedefine.gamedefine.amounts[i["what"]] < getCostWithIndex(index, automation):
            ongoing = False
            
        index += 1 
    
    return ongoing



def doAutomationTask(automation, lastTickTime):
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        return lastTickTime
    else:
        internalDefine = getCurrentInternalMultiLevelUpgrade(automation)["idleGenerator"]
        
    if gamedefine.gamedefine.automationLevels[automation] > 0:
        
        if time.time() * 1000 - lastTickTime > gamedefine.gamedefine.automationDetails[automation]["timeToWait"]:
            gamedefine.gamedefine.automationDisabledState[automation] = [False, "0"]
            lastTickTime = time.time() * 1000
            
            if not internalDefine["withRequirement"]:     
                for i in gamedefine.gamedefine.automationDetails[automation]["whatItGives"]:
                    gamedefine.gamedefine.amounts[i["what"]] += int(i["amount"])
                return lastTickTime
        
            if internalDefine["withRequirement"]:
                
                if not checkIfAutomationIsAffordable(automation):
                    gamedefine.gamedefine.automationDisabledState[automation] = [True]
                    return lastTickTime + 5000 # add 5 seconds
                
                if canAffordAutomationTask(automation):
                    for i in gamedefine.gamedefine.automationDetails[automation]["whatItGives"]:
                        gamedefine.gamedefine.amounts[i["what"]] += int(i["amount"])
                        
                    for i in gamedefine.gamedefine.automationDetails[automation]["whatItCosts"]:
                        if i["amount"] == "atMarketPrice":
                            itemToCheckFor = getCurrentInternalMultiLevelUpgrade(automation)["idleGenerator"]["whatItGives"][0]["what"]
                            price = int(gamedefine.gamedefine.itemInternalDefine[itemToCheckFor]["whatItCosts"][0]["amount"])
                            gamedefine.gamedefine.amounts[i["what"]] -= price
                        else:
                            gamedefine.gamedefine.amounts[i["what"]] -= int(i["amount"])
                else:
                    lastTickTime += 10000 # softlock prevention; add 10 seconds
                    gamedefine.gamedefine.automationDisabledState[automation] = [True]
                
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


def parseUsefulDescription(automation) -> str:
        if gamedefine.gamedefine.automationLevels[automation] == 0:
            index = getCurrentMultiLevelUpgradeIndex(automation)
            return gamedefine.gamedefine.automationVisualDefine[automation][index]["firstupgradeUsefulDescription"]
        else:
            currentVisualDict =  getCurrentVisualMultiLevelUpgrade(automation)
            
            currentInternalDict = getCurrentInternalMultiLevelUpgrade(automation)

        if currentInternalDict["type"] == "idleGenerator":
            currentDec = currentVisualDict["currentUpgradeUsefulDescription"]
            futureDec = ""
            
            if currentVisualDict["usefulDescriptionBlank"] == "tickTime":
                currentDec = currentDec.replace("%%%", str(round( gamedefine.gamedefine.automationDetails[automation]["timeToWait"]/1000, 3)))
                
                futureDec = getFutureDescription(automation)
                
            elif currentVisualDict["usefulDescriptionBlank"] == "amount":
                currentDec = currentDec.replace("%%%", str(round(gamedefine.gamedefine.automationDetails[automation]["whatItGives"][0]["amount"])))
                
                futureDec = getFutureDescription(automation)
            
            
            return currentDec + " \n " + futureDec
        
        return ""

def getFutureDescription(automation):
    
    futureInternalDict = getCurrentInternalMultiLevelUpgrade(automation, gamedefine.gamedefine.automationLevels[automation] + 1)
    futureVisualDict = getCurrentVisualMultiLevelUpgrade(automation, gamedefine.gamedefine.automationLevels[automation] + 1)
    
    if futureInternalDict["type"] == "idleGenerator":
        futureDec = str(futureVisualDict["upgradeUsefulDescription"])
        
        if futureVisualDict["usefulDescriptionBlank"] == "tickTime":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["timeEquation"], gamedefine.gamedefine.automationLevels[automation] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum/1000, 3)))
        elif futureVisualDict["usefulDescriptionBlank"] == "amount":
            futureNum = numberLogic.evaluateCostEquation(futureInternalDict["idleGenerator"]["amountEquation"][0]["equation"], gamedefine.gamedefine.automationLevels[automation] + 1)

            futureDec = futureDec.replace("%%%", str(round(futureNum)))
        
        return futureDec


def parseAutomationName(automation):
            
    currentDict = getCurrentVisualMultiLevelUpgrade(automation)
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        return f"{currentDict["visualName"]} \n {currentDict["description"]} \n"
    else:
        return f"Level {gamedefine.gamedefine.automationLevels[automation]} {currentDict["visualName"]} \n {currentDict["description"]} \n"

def getDescription(automation):
    index = getCurrentMultiLevelUpgradeIndex(automation)
    
    if gamedefine.gamedefine.automationLevels[automation] == 0:
        return f""
    else:

        return f"{gamedefine.gamedefine.automationVisualDefine[automation][index]["upgradeVisualName"]} \n {gamedefine.gamedefine.automationVisualDefine[automation][index]["upgradeDescription"]}"

def getAutomationName(automation):
    return gamedefine.gamedefine.automationVisualDefine[automation][getCurrentMultiLevelUpgradeIndex(automation)]["visualName"]