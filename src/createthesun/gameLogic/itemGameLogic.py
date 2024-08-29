from math import ceil, floor, log

import regex as re
import sympy as sp

from ..gameLogic import numberLogic
from .. import gamedefine


from PySide6.QtCore import QObject
from PySide6.QtCore import Signal , Slot

# first argment is the item, second is misc
_instance = None
class ItemGameLogic(QObject):
    
    
    
    @staticmethod
    def getInstance():
        global _instance
        if _instance is None:
            _instance = ItemGameLogic()
        return _instance

    def __new__(cls, *args, **kwargs):
        global _instance
        if not _instance:
            _instance = super(ItemGameLogic, cls).__new__(cls, *args, **kwargs)
        return _instance

    def __init__(self):
        super().__init__()

    @Slot(str, result=bool)
    def canAfford(self, item: str, doBuyMultiply=True) -> bool:
        """
        Checks if you can afford an item.

        Args:
            item (str): The item to check.

        Returns:
            bool: Whether you can afford the item or not.
        """

        buyMultiplier = gamedefine.game.mainTabBuyMultiple if doBuyMultiply else 1
       
        if gamedefine.items[item].costEquation == "":
            return True

        costs = gamedefine.items[item].cost
        ongoing = True

        for i in costs:
            print(f"checking if {i['what'].name} has {i['amount'] * buyMultiplier} {i['what'].name} and has {i['what'].amount}")
            if i["what"].amount < i["amount"] * buyMultiplier:
                ongoing = False
                

        return ongoing

    @Slot(str, result=None)
    def _purchase(self, item: str, doBuyMultiply=False) -> None:
        """
        Purchases an item.

        Args:
            item (str): The item to purchase.
        """

        buyMultiplier = gamedefine.game.mainTabBuyMultiple if doBuyMultiply else 1

        if gamedefine.items[item].costEquation == "":
        
            gamedefine.items[item].amount += 1
            print(f"purchased {item}, now have {gamedefine.items[item].amount}")
            return

    
        costs = gamedefine.items[item].cost
        gives = gamedefine.items[item].gives
        

        for i in costs:
            i["what"].amount -= i["amount"] * buyMultiplier
        for i in gives:
            i["what"].amount += i["amount"] * buyMultiplier
        print(f"purchased {item}, now have {gamedefine.items[item].amount}, with buy multiplier {buyMultiplier}")

        return

    @Slot(str, result=None)
    def purchase(self, item: str) -> None:
        if self.canAfford(item):
            self._purchase(item)

    @Slot(str, result=None)
    def getCurrentCost(self, item: str, _round: bool | None = False, eNotation: bool | None = True) -> float:
        """
        Returns the current cost of an item.

        Args:
            item (str): The item to get the cost of.
            _round (bool | None): Whether to round the cost or not. Defaults to False.

        Returns:
            dict: The current cost of the item.
        """

        buyMultiplier = gamedefine.game.mainTabBuyMultiple

        equation = gamedefine.gamedefine.itemInternalDefine[item]["costEquation"]
        if equation == "":
            return {"failed": True}

        whatItCosts = gamedefine.gamedefine.itemInternalDefine[item]["whatItCosts"][0]

        currentCost = int(numberLogic.evaluateCostEquation(equation, 1))

        # if _round:
        #     return {whatItCosts: round(currentCost) * buyMultiplier}
        # else:
        #     return {whatItCosts: currentCost * buyMultiplier}

        if _round:
            return round(currentCost * buyMultiplier)
        else:
            return currentCost * buyMultiplier

    @Slot(str, result=str)
    def parseCost(self, item: str) -> str:
        buyMultiplier = gamedefine.game.mainTabBuyMultiple

        if not gamedefine.items[item].defaultCost == -1:
            cost = gamedefine.items[item].cost
            gives = gamedefine.items[item].gives
            string = ["Purchase "]
        else:
            return "Free"
        exempt = ["Hydrogen"]
        for i in gives:
            string.append(str(numberLogic.humanReadableNumber(i["amount"] * buyMultiplier)) + " ")

            string.append(i["what"].getName_(i["amount"] * buyMultiplier).lower())
            numberLogic.humanReadableNumber
            if gives.index(i) < len(gives) - 2:
                string.append(", ")
            elif gives.index(i) == len(gives) - 2:
                string.append(" and ")
            else:
                string.append(" for ")
                
        for i in cost:
            string.append(str(numberLogic.humanReadableNumber(i["amount"] * buyMultiplier)) + " ")

            string.append(i["what"].getName_(i["amount"] * buyMultiplier).lower())

            if cost.index(i) < len(cost) - 2:
                string.append(", ")
            elif cost.index(i) == len(cost) - 2:
                string.append(" and ")
            else:
                string.append(".")

        return "".join(string)

    @Slot(result=None)
    def maxAll(self):
        def maxAllPurchase(item):
            costs = gamedefine.items[item].cost
            gives = gamedefine.items[item].gives    

            maxAmountPossible = 1

            for i in costs:
                maxAmountPossible = gamedefine.items[i].amount // i["amount"]

            for i in costs:
                gamedefine.items[i].amount -= int(i["amount"] * maxAmountPossible)
            for i in gives:
                gamedefine.items[i].amount += int(i["amount"] * maxAmountPossible)

            print(f"max all purchased {maxAmountPossible} of {item}, now have {gamedefine.items[item].amount}")

            return

        affordList = []
        for i in gamedefine.items:
            if not gamedefine.items[i].cost[0]["what"] == "nothing":
                if i in gamedefine.game.purchaseToCreate:
                    if self.canAfford(i, doBuyMultiply=False):
                        affordList.append(i)

        for i in affordList:
            maxAllPurchase(
                i
            )  # this fixes the 'cascade effect' of the max all button by not actually purchasing it until the end

gamedefine.itemGameLogic = ItemGameLogic