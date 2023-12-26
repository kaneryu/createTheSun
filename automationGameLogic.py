import sympy as sp
import regex as re
import time
from math import floor, ceil, log
import gamedefine


def getCurrentInternalMultiLevelUpgrade(upgrade: str) -> dict:
    
    target = getCurrentMultiLevelUpgradeIndex(upgrade)

    if target == 0:
        return (False, gamedefine.automationInternalDefine[upgrade])
    else:    
        return gamedefine.automationInternalDefine[upgrade]["multiLevelUpgrades"][target]

def getCurrentMultiLevelUpgradeIndex(upgrade: str) -> int:
    
    currentLevel = gamedefine.upgradeLevels[upgrade]
    target = 0
    
    for i in gamedefine.automationInternalDefine[upgrade]["multiLevelUpgradesStarts"]:
        if currentLevel >= i:
            target += 1
    return target

def getCurrentVisualMultiLevelUpgrade(upgrade: str) -> dict:

    target = getCurrentMultiLevelUpgradeIndex(upgrade)

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
        costs = getCurrentInternalMultiLevelUpgrade(upgrade)["upgradeCost"]
    
    ongoing = True
    
    for i in costs:
        if gamedefine.amounts[i["what"]] < i["amount"]:
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
            
            gamedefine.upgradeDetails[upgrade]["timeToWait"] = evaluateCostEquation(idleGenDict["equation"], gamedefine.upgradeLevels[upgrade])
            for i in len(idleGenDict["whatItGives"]):
                gamedefine.upgradeDetails[upgrade]["whatItGives"][i]["amount"] = idleGenDict["whatItGives"][i]["amount"]
            
            if idleGenDict["withRequirement"]:
                
                for i in len(idleGenDict["whatItCosts"]):
                    gamedefine.upgradeDetails[upgrade]["whatItCosts"][i]["amount"] = idleGenDict["whatItCosts"][i]["amount"]
            
        elif idleGenDict["equationType"] == "amountEquation":
            
            gamedefine.upgradeDetails[upgrade]["timeToWait"] = idleGenDict["time"]
            for i in len(idleGenDict["whatItGives"]):
                amount = evaluateCostEquation(idleGenDict["amountEquation"][i], gamedefine.upgradeLevels[upgrade])
                gamedefine.upgradeDetails[upgrade]["whatItGives"][i]["amount"] = amount
                
            if idleGenDict["withRequirement"]:
                for i in len(idleGenDict["whatItCosts"]):
                    amount = evaluateCostEquation(idleGenDict["costEquation"][i], gamedefine.upgradeLevels[upgrade])
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
        if internalDefine["type"] == "idleGenerator":
            if time.time() * 1000 - lastTickTime > gamedefine.upgradeDetails[upgrade]["timeToWait"]:
                lastTickTime = time.time() * 1000
                if internalDefine["withRequirement"]:
                    if canAffordUpgradeTask(upgrade):
                        for i in gamedefine.upgradeDetails[upgrade]["whatYouGet"]:
                            gamedefine.amounts[i["what"]] += i["amount"]
                        for i in gamedefine.upgradeDetails[upgrade]["whatItCosts"]:
                            gamedefine.amounts[i["what"]] -= i["amount"]
                    else:
                        lastTickTime += 10000 # softlock prevention; add 10 seconds
                else:         
                    for i in gamedefine.upgradeDetails[upgrade]["whatYouGet"]:
                        gamedefine.amounts[i["what"]] += i["amount"]
                        
    return lastTickTime
        

def evaluateCostEquation(costEquation: str, *args: int) -> int:
    """
    Evaluates the cost equation.

    Args:
        costEquation (str): The cost equation to evaluate.
        *args: The arguments to put into the cost equation.

    Returns:
        int: The result of the cost equation.    
    """

    # if there are too many arguments, it will break
    if f"%{len(args) + 1}%" in costEquation:
        # failed, 0
        return ([-1, 0])
    # if there are too few arguments, it will break
    if f"%{len(args)}%" in costEquation:
        # failed, 0
        return ([-1, 0])
    # break up the equation into a list of strings
    equation = splitCostEquation(costEquation)

    amountVarsFound = 1
    for i in range(len(equation)):
        # if it's a number, replace it with the argument
        if equation[i] == "%":
            equation[i] = str(args[amountVarsFound - 1])
            amountVarsFound += 1
    # join the list of strings into one string
    equation = "".join(equation)
    expr = sp.sympify(equation)

    return expr.evalf()


def splitCostEquation(costEquation: str) -> list[str]:
    """
    Splits the cost equation into a list of strings.

    Args:
        costEquation (str): The cost equation to split.

    Returns:
        list[str]: The list of strings.
    """

    groups = []
    latestGroup = ""
    i = 0
    while i < len(costEquation):
        if costEquation[i] == "%":
            if latestGroup != "":
                groups.append(latestGroup)
                latestGroup = ""
            if costEquation[i + 1].isnumeric():
                groups.append("%")
                i = i + 1
        else:
            latestGroup += costEquation[i]
        i += 1
    if latestGroup != "":
        groups.append(latestGroup)
    return (groups)

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
            futureDec = currentVisualDict["upgradeUsefulDescription"]
            
            if currentVisualDict["usefulDescriptionBlank"] == "amount":
                currentDec = currentDec.replace("%%%", str(gamedefine.upgradeDetails[upgrade]["timeToWait"]))
                futureDec = futureDec.replace("%%%", str(gamedefine.upgradeDetails[upgrade]["timeToWait"]))
            elif currentVisualDict["usefulDescriptionBlank"] == "tickTime":
                currentDec = currentDec.replace("%%%", str(gamedefine.upgradeDetails[upgrade]["whatYouGet"][0]["amount"]))
                futureDec = futureDec.replace("%%%", str(gamedefine.upgradeDetails[upgrade]["whatYouGet"][0]["amount"]))
            
            return currentDec + " \n " + futureDec

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