import sympy as sp
import regex as re
from math import floor, ceil, log
import gamedefine


def canAfford(item: str) -> bool:
    """
    Checks if you can afford an item.

    Args:
        item (str): The item to check.

    Returns:
        bool: Whether you can afford the item or not.
    """

    if gamedefine.itemInternalDefine[item]["costEquation"] == "":
        return True

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"]
    
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

    if gamedefine.itemInternalDefine[item]["costEquation"] == "":
        gamedefine.amounts[item] += 1
        print(f"purchased {item}, now have {gamedefine.amounts[item]}")
        return

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"]
    whatItGives = gamedefine.itemInternalDefine[item]["whatItGives"]
    
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
    
    equation = gamedefine.itemInternalDefine[item]["costEquation"]
    if equation == "":
        return 0

    whatItCosts = gamedefine.itemInternalDefine[item]["whatItCosts"][0]

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


def parseCost(name):
    if not name == "quarks":
        what = gamedefine.itemInternalDefine[name]["whatItCosts"]
        string = ["Purchase for "]                    

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