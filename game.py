import sympy as sp
import regex as re
from math import floor, ceil, log
import gamedefine
def canAffordUpgradeTask(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade's task.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade's task or not.
    """
    costs = gamedefine.upgradeDetails[upgrade]["whatItCosts"]
    
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
    if gamedefine.upgradeLevels[upgrade] >= gamedefine.upgradeInternalDefine[upgrade]["maxLevel"]:
        return
    
    if gamedefine.upgradeLevels[upgrade] == 0:
        costs = gamedefine.upgradeInternalDefine[upgrade]["firstCost"]
    else:
        costs = gamedefine.upgradeInternalDefine[upgrade]["upgradeCost"]
    

    for i in costs:
        gamedefine.amounts[i["what"]] -= i["amount"]
    gamedefine.upgradeLevels[upgrade] += 1
    print(f"purchased {upgrade}, now have {gamedefine.upgradeLevels[upgrade]}")
    return

    
def canAffordUpgrade(upgrade : str) -> bool:
    """
    Checks if you can afford an upgrade.
    
    Args:
        upgrade (str): The upgrade to check
    
    Returns:
        bool: Whether you can afford the upgrade or not.
    """
    if gamedefine.upgradeLevels[upgrade] >= gamedefine.upgradeInternalDefine[upgrade]["maxLevel"]:
        return False
    if gamedefine.upgradeLevels[upgrade] == 0:
        costs = gamedefine.upgradeInternalDefine[upgrade]["firstCost"]
    else:
        costs = gamedefine.upgradeInternalDefine[upgrade]["upgradeCost"]
    
    ongoing = True
    
    for i in costs:
        if gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
    
    return ongoing
    
    
def canAfford(item: str) -> bool:
    """
    Checks if you can afford an item.

    Args:
        item (str): The item to check.

    Returns:
        bool: Whether you can afford the item or not.
    """

    if gamedefine.internalGameDefine[item]["costEquation"] == "":
        return True

    whatItCosts = gamedefine.internalGameDefine[item]["whatItCosts"]
    
    ongoing = True
    
    for i in whatItCosts:
        if gamedefine.amounts[i["what"]] < i["amount"]:
            ongoing = False
    
    return ongoing

def purchase(item: str) -> None:
    """
    Purchases an item.

    Args:
        item (str): The item to purchase.
        cost (int): The cost of the item.
    """

    if gamedefine.internalGameDefine[item]["costEquation"] == "":
        gamedefine.amounts[item] += 1
        print(f"purchased {item}, now have {gamedefine.amounts[item]}")
        return

    whatItCosts = gamedefine.internalGameDefine[item]["whatItCosts"]
    whatItGives = gamedefine.internalGameDefine[item]["whatItGives"]
    
    for i in whatItCosts:
        gamedefine.amounts[i["what"]] -= i["amount"]
    for i in whatItGives:
        gamedefine.amounts[i["what"]] += i["amount"]
    print(f"purchased {item}, now have {gamedefine.amounts[item]}")
    
    return

def getCurrentCost(item: str, _round : bool | None = False, eNotation : bool | None = True) -> dict:
    """
    Returns the current cost of an item.
    
    Args:
        item (str): The item to get the cost of.
        _round (bool | None): Whether to round the cost or not. Defaults to False.
    
    Returns:
        dict: The current cost of the item.    
    """
    
    equation = gamedefine.internalGameDefine[item]["costEquation"]
    if equation == "":
        return 0

    whatItCosts = gamedefine.internalGameDefine[item]["whatItCosts"][0]

    currentCost = int(evaluateCostEquation(equation, 1))

    if _round:
        return {whatItCosts: round(currentCost)}
    else: 
        return {whatItCosts: currentCost}
    
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

def nonilize(number):
    if number == 0:
        return 0
    
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.1f %s' % (number / k**magnitude, magnitudeDict[magnitude - 1])

def magnitude(number):
    if number == 0:
        return 0
    k = 1000.0
    return int(floor(log(number, k)))

def humanReadableNumber(number):
    if number == 0:
        return "0"
    if magnitude(number) > 11:
        return '{:.2e}'.format(number)
    else:
        if number < 1000:
            return str(number)
        else:
            return nonilize(number)
        

magnitudeDict = {
    -1: "",
    0:  "K",
    1:  "M",
    2:  "B",
    3:  "T",
    4:  "Qa",
    5:  "Qt",
    6:  "Sx",
    7:  "Sp",
    8:  "Oc",
    9:  "No",
    10:	"Dc",
    11:	"UDc",
    12:	"DDc",
    13:	"TDc",
    14:	"QaDc",
    15:	"QtDc",
    16:	"SxDc",
    17:	"SpDc",
    18: "ODc",
    19: "NDc",
    20: "Vg",
    21: "UVg",
    22: "DVg",
    23: "TVg",
    24: "QaVg",
    25: "QtVg",
    26: "SxVg",
    27: "SpVg",
    28: "OVg",
    29: "NVg",
    30: "Tg",
    31: "UTg",
    32: "DTg",
    33: "TTg",
    34: "QaTg",
    35: "QtTg",
    36: "SxTg",
    37: "SpTg",
    38: "OTg",
    39: "NTg",
    40: "Qd",
    41: "UQd",
    42: "DQd",
    43: "TQd",
    44: "QaQd",
    45: "QtQd",
    46: "SxQd",
    47: "SpQd",
    48: "OQd",
    49: "NQd",
    50: "Qi",
    51: "UQi",
    52: "DQi",
    53: "TQi",
    54: "QaQi",
    55: "QtQi",
    56: "SxQi",
    57: "SpQi",
    58: "OQi",
    59: "NQi",
    60: "Se",
    61: "USe",
    62: "DSe",
    63: "TSe",
    64: "QaSe",
    65: "QtSe",
    66: "SxSe",
    67: "SpSe",
    68: "OSe",
    69: "NSe",
    70: "St",
    71: "USt",
    72: "DSt",
    73: "TSt",
    74: "QaSt",
    75: "QtSt",
    76: "SxSt",
    77: "SpSt",
    78: "OSt",
    79: "NSt",
    80: "Og",
    81: "UOg",
    82: "DOg",
    83: "TOg",
    84: "QaOg",
    85: "QtOg",
    86: "SxOg",
    87: "SpOg",
    88: "OOg",
    89: "NOg",
    90: "Nn",
    91: "UNn",
    92: "DNn",
    93: "TNn",
    94: "QaNn",
    95: "QtNn",
    96: "SxNn",
    97: "SpNn",
    98:	"ONn",
    99:	"NNn",
    100: "Ce" 
}