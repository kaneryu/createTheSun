#######
from __future__ import annotations
#######

import json
import time
from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Self


import deepdiff
import regex
import versions
from dacite import from_dict
from PySide6.QtWidgets import QTabWidget
from PySide6.QtCore import QObject, Signal, Slot, Property as QProperty, QTimer


from . import quickload

ItemGameLogic = None
items: dict[str, _Item] = {}

# Base Classes
class _Item(QObject):
    """This is the base class for all items, will not be accessed directly. It supports switch items, which are items that have been modified from the base item.
    
    Note that switches are guranteed to always be in the same order, so the first switch will always be the first switch, and so on.
    The use of switch items are optional, so this class can be used without them.
    """
    nameChanged = Signal(str)
    descriptionChanged = Signal(str)
    amountChanged = Signal(int)
    affordablilityChanged = Signal(bool)
    costChanged = Signal(list)
    
    def __init__(self):
        super().__init__()
        global items
        items[self.__class__.__name__] = self
        
        self._name: str = ""
        self._description: str = ""

        self._amount: int = 0
        
        self._affordable: bool = True
        
        self.internalName: str = ""
        self.singlarName: str = ""
        self._cost: list[dict[_Item, int]] = []
        self.defaultCost: int = 0
        self.costEquation: str = ""
        self.gives: list[dict[_Item, int]] = []
        self.switches: list[object] = []
        
        self.nameChanged.connect(self.affordablilityCheck)
        self.amountChanged.connect(self.affordablilityCheck)
        
        self.costChanged.connect(self.recheckcosts)

    
    def recheckcosts(self):
        for i in self.cost:
            i["what"].amountChanged.connect(self.affordablilityCheck)
            
    
    
    def periodicalChecks(self):
        self.affordablilityCheck()
    
    def getSwitch(self, switch: int) -> object:
        """This function will return the correct switch item based on the switch number.
        
        Args:
            switch (int): The switch number.
        
        Returns:
            Item_Switch: The correct switch item.
        """
        return self.switches[switch]
    @QProperty(str, notify=costChanged)
    def cost(self) -> list[dict[_Item, int]]:
        return self._cost
    
    @cost.setter
    def cost(self, value: list[dict[_Item, int]]):
        self._cost = value
        self.costChanged.emit(value)
    
    @QProperty(str, notify=nameChanged)
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
        self.nameChanged.emit(value)

    
    @QProperty(str, notify=descriptionChanged)
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
        self.descriptionChanged.emit(value)

    
    @QProperty(int, notify=amountChanged)
    def amount(self) -> int:
        return self._amount
    
    @amount.setter
    def amount(self, value: int):
        self._amount = value
        self.amountChanged.emit(value)

    @QProperty(bool, notify=affordablilityChanged)
    def affordable(self) -> bool:
        return self._affordable

    @affordable.setter
    def affordable(self, value: bool):
        self._affordable = value
        self.affordablilityChanged.emit(value)
        
    @Slot(result=str)
    def getName(self) -> str:
        if not self.amount == 1:
            return self.name
        else:
            return self.singlarName
    
    def getName_(self, number) -> str:
        if not number == 1:
            return self.name
        else:
            return self.singlarName

    @Slot()
    def affordablilityCheck(self):
        if ItemGameLogic is not None:
            self.affordable = ItemGameLogic.getInstance().canAfford(self.name)
        else: 
            print("affordablilityCheck: ItemGameLogic is not defined")

class _LevelAutomation:
    """This is the base class for all automations, will not be accessed directly, even when instantiated.
    It should instead be used with the Automation class, which will return the correct LevelAutomation class.
    """
    def __init__(self):
        
        self.name: str = ""
        self.description: str = ""
        self.upgradeName: str = ""
        self.upgradeDescription: str = ""
        
        self.statDescription: str = ""
        self.upgradeStatDescription: str = ""
        self.statDescriptionBlank: str = ""

        self.disabledText: str = ""
        
        
        self.startLevel: int = 0
        self.upgradeCost: list[dict[str, int]] = []
        self.withRequirement: bool = False
        self.type: str = ""
        self.idleGenerator: dict[str, int] = {}
        
class Automation:
    """This is the base class for all automations, will not be accessed directly.
    
    """
    def __init__(self):
        self.firstCost: list[dict[str, int]] = []
        self.maxLevel: int = 0
        self.multiLevelUpgradesStarts: list[int] = []
        self.multiLevelUpgrades: list[Automation] = []
    
    def getAutomationClass(self, level: int) -> _LevelAutomation:
        """This function will return the correct LevelAutomation class based on the level of the automation.
        
        Args:
            level (int): The level of the automation.
        
        Returns:
            _LevelAutomation: The correct LevelAutomation class.
        """
        return self.multiLevelUpgrades[self.getMultiLevel(level)]

    def getMultiLevel(self, level: int) -> int:
        """This function will return the correct LevelAutomation class based on the level of the automation.
        
        Args:
            level (int): The level of the automation.
        
        Returns:
            int: The correct LevelAutomation class.
        """
        _ = 0
        while level >= self.multiLevelUpgradesStarts[_]:
            _ += 1
        
        return self.multiLevelUpgrades[_]
        
class Achevement:
    pass

class Unlockable:
    pass

class Rewrite:
    pass

initalized = False

class Quarks(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Quarks"
        self.singlarName = "Quark"
        self.description = "Quarks are the building blocks of protons. They are made of nothing...?"
        self.internalName = "quarks"
        
        self.cost = [{"what": None, "amount": -1}]
        self.defaultCost = -1
        self.costEquation = ""
        self.gives = [{"what": items["Quarks"], "amount": 1}]
        
        
Quarks()

class Electrons(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Electrons"
        self.singlarName = "Electron"
        self.description = "Electrons are the building blocks of atoms."
        self.internalName = "electrons"
        
        self.cost = [{"what": None, "amount": -1}]
        self.defaultCost = -1
        self.costEquation = ""
        self.gives = [{"what": items["Electrons"], "amount": 1}]
electronkeepref = Electrons()


class Protons(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Protons"
        self.singlarName = "Proton"
        self.description = "Protons are the building blocks of atoms. They are made of quarks."
        self.internalName = "protons"
        self.amount = 3
        self.cost = [{"what": items["Quarks"], "amount": 3}]
        self.costEquation = "%1 * 3"
        self.gives = [{"what": items["Protons"], "amount": 1}]
Protons()

class Hydrogen(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Hydrogen"
        self.singlarName = "Hydrogen"
        self.description = "Hydrogen is the simplest element. It is made of one proton and one electron."
        
        self.internalName = "hydrogen"
        self.cost = [{"what": items["Quarks"], "amount": 1}, {"what": items["Protons"], "amount": 1}, {"what": items["Electrons"], "amount": 1}]
        self.costEquation = "%1 * 3"
        self.gives = [{"what": items["Hydrogen"], "amount": 1}]
Hydrogen()

class Stars(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Stars"
        self.singlarName = "Star"
        self.description = "Stars are the building blocks of galaxies. They are made of hydrogen."
        
        self.internalName = "stars"
        self.cost = [{"what": items["Hydrogen"], "amount": 1e57}]
        self.costEquation = "%1 * 1e57"
        self.gives = [{"what": items["Stars"], "amount": 2}]
Stars()

class Galaxies(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Galaxies"
        self.singlarName = "Galaxy"
        self.description = "Galaxies are the building blocks of superclusters. They are made of stars."
        
        self.internalName = "galaxies"
        self.cost = [{"what": items["Stars"], "amount": 1e11}]
        self.costEquation = "%1 * 1e11"
        self.gives = [{"what": items["Galaxies"], "amount": 1}]
Galaxies()

class Superclusters(_Item):
    def __init__(self):
        super().__init__()
        self.name = "Superclusters"
        self.singlarName = "Supercluster"
        self.description = "Superclusters are the building blocks of the universe. They are made of galaxies."
        
        self.internalName = "superclusters"
        self.cost = [{"what": items["Galaxies"], "amount": 100000}]
        self.costEquation = "%1 * 100000"
        self.gives = [{"what": items["Superclusters"], "amount": 1}]
Superclusters()

class Game(QObject):
    purchaseToCreateChanged = Signal(list[str])
    automationsToCreateChanged = Signal(list[str])
    mainTabBuyMultipleChanged = Signal(int)
    playTimeChanged = Signal(int)
    tutorialPopupDoneChanged = Signal(bool)  
    
    def __init__(self) -> None:
        super().__init__()
        
        self._purchaseToCreate = ["Quarks", "Protons"]
        self._automationsToCreate = ["particleAccelerator", "protonicForge"]
        
        self._mainTabBuyMultiple = 1
        
        self._playTime = 0
        self._tutorialPopupDone = False

    @QProperty(list, notify=purchaseToCreateChanged)
    def purchaseToCreate(self) -> list[str]:
        return self._purchaseToCreate
    
    @purchaseToCreate.setter
    def purchaseToCreate(self, value: list[str]):
        self._purchaseToCreate = value
        self.purchaseToCreateChanged.emit(value)
    
        
    @QProperty(list, notify=automationsToCreateChanged)
    def automationsToCreate(self) -> list[str]:
        return self._automationsToCreate
    
    @automationsToCreate.setter
    def automationsToCreate(self, value: list[str]):
        self._automationsToCreate = value
        self.automationsToCreateChanged.emit(value)
    
    @QProperty(int, notify=mainTabBuyMultipleChanged)
    def mainTabBuyMultiple(self) -> int:
        return self._mainTabBuyMultiple
    
    @mainTabBuyMultiple.setter
    def mainTabBuyMultiple(self, value: int):
        self._mainTabBuyMultiple = value
        self.mainTabBuyMultipleChanged.emit(value)
    
    @QProperty(int, notify=playTimeChanged)
    def playTime(self) -> int:
        return self._playTime
    
    @playTime.setter
    def playTime(self, value: int):
        self._playTime = value
        self.playTimeChanged.emit(value)
    
    @QProperty(bool, notify=tutorialPopupDoneChanged)
    def tutorialPopupDone(self) -> bool:
        return self._tutorialPopupDone
    
    @tutorialPopupDone.setter
    def tutorialPopupDone(self, value: bool):
        self._tutorialPopupDone = value
        self.tutorialPopupDoneChanged.emit(value)
        
game = Game()

defualtGameDefine = {
    "itemVisualDefine": {
        "quarks": {
            "visualName": "Quarks",
            "description": "Quarks are the building blocks of protons. They are made of nothing...?",
            "id": ["quarks", 0],
        },
        "electrons": {
            "visualName": "Electrons",
            "description": "Electrons are the building blocks of atoms.",
            "id": ["electrons", 1],
        },
        "protons": {
            "visualName": "Protons",
            "description": "Protons are the building blocks of atoms. They are made of quarks.",
            "id": ["protons", 2],
        },
        "hydrogen": {
            "visualName": "Hydrogen",
            "description": "Hydrogen is the simplest element. It is made of one proton and one electron.",
            "id": ["hydrogen", 3],
        },
        "stars": {
            "visualName": "Stars",
            "description": "Stars are the building blocks of galaxies. They are made of hydrogen.",
            "id": ["stars", 4],
        },
        "galaxies": {
            "visualName": "Galaxies",
            "description": "Galaxies are the building blocks of superclusters. They are made of stars.",
            "id": ["galaxies", 5],
        },
        "superclusters": {
            "visualName": "Superclusters",
            "description": "Superclusters are the building blocks of the universe. They are made of galaxies.",
            "id": ["superclusters", 6],
        },
    },
    "itemInternalDefine": {
        "quarks": {
            "whatItCosts": [{"what": "nothing", "amount": -1}],
            "defaultCost": -1,
            "costEquation": "",
            "whatItGives": [{"what": "quarks", "amount": 1}],
        },
        "electrons": {
            "whatItCosts": [{"what": "nothing", "amount": -1}],
            "defaultCost": -1,
            "costEquation": "",
            "whatItGives": [{"what": "electrons", "amount": 1}],
        },
        "protons": {
            "whatItCosts": [{"what": "quarks", "amount": 3}],
            "defaultCost": 3,
            "costEquation": "%1 * 3",
            "whatItGives": [{"what": "protons", "amount": 1}],
        },
        "hydrogen": {
            "whatItCosts": [{"what": "protons", "amount": 1}, {"what": "electrons", "amount": 1}],
            "defaultCost": 1,
            "costEquation": "%1 * 1",
            "whatItGives": [{"what": "hydrogen", "amount": 1}],
        },
        "stars": {
            "whatItCosts": [{"what": "hydrogen", "amount": 1e57}],
            "defaultCost": 1e57,
            "costEquation": "%1 * 1e57",
            "whatItGives": [{"what": "Stars", "amount": 2}],
        },
        "galaxies": {
            "whatItCosts": [
                {"what": "stars", "amount": 1e11},
            ],
            "defaultCost": 1e11,
            "costEquation": "%1 * 1e11",
            "whatItGives": [{"what": "galaxies", "amount": 1}],
        },
        "superclusters": {
            "whatItCosts": [{"what": "galaxies", "amount": 100000}],
            "defaultCost": 100000,
            "costEquation": "%1 * 100000",
            "whatItGives": [{"what": "superclusters", "amount": 1}],
        },
    },
    "automationInternalDefine": {
        "particleAccelerator": {
            "firstCost": [
                {"what": "quarks", "amount": 100},
                {"what": "electrons", "amount": 100},
                {"what": "protons", "amount": 30},
            ],
            "maxLevel": 50,
            "multiLevelUpgradesStarts": [1, 30],
            "multiLevelUpgrades": [
                {
                    "startLevel": 1,
                    "upgradeCost": [
                        {"what": "quarks", "amount": "(%1 - 1) * 15 + 100", "variables": ["level"]},
                        {"what": "electrons", "amount": "1.1^((-1 * %1) + 34.5) + 10", "variables": ["level"]},
                    ],
                    "withRequirement": False,
                    "type": "idleGenerator",
                    "idleGenerator": {
                        "whatItGives": [{"what": "quarks", "amount": 1}],
                        "withRequirement": False,
                        "time": 1000,
                        # in this case, %1 is upgrade level
                        "equationType": "timeEquation",
                        "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))",
                    },
                },
                {
                    "startLevel": 30,
                    "upgradeCost": [
                        {"what": "quarks", "amount": "(%1 - 1) * 30 - 500", "variables": ["level"]},
                        {"what": "electrons", "amount": "1.04^((-1 * %1) + 82) + 4", "variables": ["level"]},
                    ],
                    "withRequirement": False,
                    "type": "idleGenerator",
                    "idleGenerator": {
                        "withRequirement": False,
                        "whatItGives": [{"what": "quarks", "amount": 3}],
                        "time": 10,
                        # in this case, %1 is upgrade level
                        "equationType": "amountEquation",
                        "amountEquation": [{"equation": "(%1-30)+3"}],
                    },
                },
            ],
        },
        "protonicForge": {
            "firstCost": [
                {"what": "quarks", "amount": 500},
                {"what": "electrons", "amount": 100},
                {"what": "protons", "amount": 200},
            ],
            "multiLevelUpgradesStarts": [1, 50],
            "multiLevelUpgrades": [
                {
                    "startLevel": 1,
                    "upgradeCost": [
                        {"what": "protons", "amount": "((%1-1)*30+200)", "variables": ["level"]},
                        {"what": "electrons", "amount": "1.1^(-1*%1+34.5)+14", "variables": ["level"]},
                    ],
                    "maxLevel": 50,
                    "type": "idleGenerator",
                    "withRequirement": True,
                    "idleGenerator": {
                        "whatItGives": [{"what": "protons", "amount": 1}],
                        "type": "idleGenerator",
                        "withRequirement": True,
                        "whatItCosts": [{"what": "quarks", "amount": "atMarketPrice"}],
                        "time": 1000,
                        "equationType": "timeEquation",
                        # in this case, %1 is upgrade level
                        "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))",
                    },
                },
                {
                    "startLevel": 50,
                    "maxLevel": 150,
                    "upgradeCost": [
                        {"what": "protons", "amount": "(%1-1)*60 - 500", "variables": ["level"]},
                        {"what": "electrons", "amount": "1.1^(-1*%1+34.5)+14", "variables": ["level"]},
                    ],
                    "type": "idleGenerator",
                    "withRequirement": True,
                    "idleGenerator": {
                        "withRequirement": True,
                        "whatItGives": [{"what": "protons", "amount": 1}],
                        "whatItCosts": [{"what": "quarks", "amount": "atMarketPrice"}],
                        "time": 10,
                        "equationType": "amountEquation",
                        # in this case, %1 is upgrade level
                        "amountEquation": [
                            {
                                "equation": "(%1-45)/2+3",
                            }
                        ],
                    },
                },
            ],
        },
    },
    "automationVisualDefine": {
        "particleAccelerator": [
            {
                "default": False,
                "visualName": "Particle Accelerator",
                "description": "Accelerates particles to create quarks.",
                "upgradeVisualName": "Increase Loop Size",
                "upgradeDescription": "Increase the size of the particle accelerator loop for more quarks per second.",
                "firstupgradeUsefulDescription": "Creates 1 Quark per second", # rolled into statDescription (See below)
                "currentUpgradeUsefulDescription": "You are currently gaining 1 Quark every %%% seconds", # renamed to statDescription
                "upgradeUsefulDescription": "Upgrade to gain 1 Quark every %%% seconds",
                "usefulDescriptionBlank": "tickTime",
                "disabledText": "How are you seeing this?",
                "id": ["particleAccelerator", 0],
            },
            {
                "default": False,
                "visualName": "Particle Accelerator",
                "description": "Accelerates particles to create quarks.",
                "upgradeVisualName": "Increase Loop Size",
                "upgradeDescription": "Increase the size of the particle accelerator loop for more quarks per second.",
                "firstupgradeUsefulDescription": "Creates 1 Quark per second",
                "currentUpgradeUsefulDescription": "You are currently gaining %%% Quarks every 0.011 seconds",
                "upgradeUsefulDescription": "Upgrade to gain %%% Quarks every 0.011 seconds",
                "usefulDescriptionBlank": "amount",
                "disabledText": "How are you seing this?",
                "id": ["particleAccelerator", 0],
            },
        ],
        "protonicForge": [
            {
                "visualName": "Protonic Forge",
                "description": "Automatically combines quarks into protons.",
                "upgradeVisualName": "Increase Forge Size",
                "upgradeDescription": "Increase the size of the forge, allowing for more quarks to be combined into protons per second",
                "firstupgradeUsefulDescription": "Creates 1 Proton per second",
                "currentUpgradeUsefulDescription": "You are currently gaining 1 Proton every %%% seconds",
                "upgradeUsefulDescription": "Upgrade to gain 1 Proton every %%% seconds",
                "disabledText": "Disabled: Not enough Quark production",
                "usefulDescriptionBlank": "tickTime",
                "upgradeId": ["protonicForgeTickUpgrade", 0],
            },
            {
                "visualName": "Blast Protonic Forge",
                "description": "Automatically combines quarks into protons.",
                "upgradeVisualName": "Increase Forge Size",
                "upgradeDescription": "Increase the size of the forge, allowing for more protons to be produced per 0.011 seconds",
                "firstupgradeUsefulDescription": "Creates 1 Proton per second",
                "currentUpgradeUsefulDescription": "You are currently gaining %%% Protons every 0.011 seconds",
                "upgradeUsefulDescription": "Upgrade to gain %%% Protons every 0.011 seconds",
                "usefulDescriptionBlank": "amount",
                "disabledText": "Disabled: Not enough Quark production",
                "upgradeId": ["protonicForgeAmountUpgrade", 0],
            },
        ],
    },
    "purchaseToCreate": ["quarks", "protons"],
    "automationsToCreate": ["particleAccelerator", "protonicForge"],
    "amounts": {
        "quarks": 0,
        "electrons": 100,
        "protons": 0,
        "hydrogen": 0,
        "stars": 0,
        "galaxies": 0,
        "superclusters": 0,
    },
    "clickGainMultiplierList": {
        "quarks": [1],
        "electrons": [1],
        "protons": [1],
        "hydrogen": [1],
        "stars": [1],
        "galaxies": [1],
        "superclusters": [1],
    },
    "multiplierList": {
        "quarks": [1],
        "electrons": [1],
        "protons": [1],
        "hydrogen": [1],
        "stars": [1],
        "galaxies": [1],
        "superclusters": [1],
    },
    "mainTabBuyMultiple": 1,
    "electronDetails": {
        "waitTime": 500,
        "amount": 1,
        "maxAmount": 100,
        "minAmount": 0,
    },
    "automationLevels": {"particleAccelerator": 0, "protonicForge": 0},
    "automationDisabledState": {"particleAccelerator": [False], "protonicForge": [False]},
    "automationDetails": {
        "particleAccelerator": {"timeToWait": 1000, "whatItGives": [{"what": "quarks", "amount": 1}]},
        "protonicForge": {
            "timeToWait": 1000,
            "whatItGives": [{"what": "protons", "amount": 1}],
            "whatItCosts": [{"what": "quarks", "amount": 3}],
        },
    },
    "achevementInternalDefine": {
        "theBeginning": {
            "hidden": False,
            "whatItRequires": [
                {"type": "item", "what": "quarks", "amount": 1},
                {"type": "item", "what": "protons", "amount": 1},
            ],
            "type": "show",
            "whatItGives": [{"type": "item", "what": "nothing", "amount": -1}],
        },
        "automation": {
            "hidden": False,
            "whatItRequires": [{"type": "automation", "what": "protonicForge", "amount": 1}],
            "type": "itemReward",
            "whatItGives": [{"type": "item", "what": "protons", "specialAmount": False, "amount": 10}],
        },
        "rewrite": {
            "hidden": False,
            "whatItRequires": [{"type": "item", "what": "hydrogen", "amount": 10}],
            "type": "show",
            "whatItGives": [{"type": "item", "what": "nothing", "specialAmount": False, "amount": -1}],
        },
        "perpetualMotion": {
            "hidden": False,
            "whatItRequires": [{"type": "rewrite", "what": "protonSpillover", "amount": 1}],
            "type": "itemReward",
            "whatItGives": [
                {
                    "type": "item",
                    "what": "quarks",
                    "specialAmount": True,
                    "amount": {"type": "double", "cap": 100_000_000},
                }
            ],
        },
    },
    "achevementVisualDefine": {
        "theBeginning": {
            "visualName": "The Beginning",
            "hoverDescription": "At the start, there was nothing... \n Create your first quark and proton.",
            "rewardDescription": "",
        },
        "automation": {
            "visualName": "Automation",
            "hoverDescription": "Automation is upon us. \n Create your first protonic forge.",
            "rewardDescription": "Unlock to recive 10 protons",
        },
        "rewrite": {
            "visualName": "Rewrite",
            "hoverDescription": "The universe is being rewritten. \n Unlock the rewrite tab.",
            "rewardDescription": "",
        },
        "perpetualMotion": {
            "visualName": "Perpetual Motion",
            "hoverDescription": "Pretty sure that's illegal somehow... \n Unlock the Proton Spillover rewrite.",
            "rewardDescription": "Gain double your current amount of quarks, capped to 100M",
        },
    },
    "unlockedAchevements": [],
    "unlockables": {  # if visible is set to true, a corresponding visual define must be set. It's not required if it's set to false
        "hydrogenUnlock": {
            "visible": True,
            "unlockType": "item",
            "whatUnlocks": "hydrogen",
            "needs": [
                {"type": "automation", "what": "protonicForge", "amount": 3},
                {"type": "item", "what": "quarks", "amount": 1000},
                {"type": "item", "what": "protons", "amount": 50},
            ],
            "makeVisible": ["rewriteTabUnlock"],
        },
        "rewriteTabUnlock": {
            "visible": False,
            "unlockType": "tab",
            "whatUnlocks": "rewrite",
            "needs": [
                {"type": "item", "what": "hydrogen", "amount": 20000},
                {"type": "item", "what": "protons", "amount": 100_000},
            ],
            "makeVisible": None,
        },
    },
    "unlockablesVisualDefine": {
        "hydrogenUnlock": {
            "visualName": "Hydrogen Unlock",
            "hoverDescription": "Unlock Hydrogen",
            "scale": "linear",  # for the progress bar, options are linear or log
        },
        "rewriteTabUnlock": {
            "visualName": "Rewrite Tab Unlock",
            "hoverDescription": "Unlock the rewrite tab",
            "scale": "linear",
        },
    },
    "unlockedUnlockables": [],
    "rewriteInternalDefine": {
        "protonSpillover": {
            "cost": [
                {"what": "quarks", "amount": 10000},
                {"what": "protons", "amount": 2000},
                {"what": "hydrogen", "amount": 100},
                {"what": "electrons", "amount": 100},
            ],
            "type": "spillover",
            "spillover": {
                "time": 100,
                "takes": {"what": "protons", "amount": 1},
                "gives": [{"what": "quarks", "amount": 4}],
                "cap": "%1 / 2",
                "capvar": ["gainPerSecond"],
                # 1/2 of the proton gain per second
                "hardcap": 1_000_000,
                # maximum amount of protons that can be consumed per time
            },
        },
        "hydrogenSpillover": {
            "cost": [
                {"what": "quarks", "amount": 50_000_000},
                {"what": "protons", "amount": 10_000},
                {"what": "hydrogen", "amount": 10_000},
                {"what": "electrons", "amount": 100},
            ],
            "type": "spillover",
            "spillover": {
                "time": 100,
                "takes": {"what": "hydrogen", "amount": 1},
                "gives": [{"what": "protons", "amount": 2}, {"what": "electrons", "amount": 2}],
                "cap": "%1 / 2",
                "capvar": ["gainPerSecond"],
                # 1/2 of the proton gain per second
                "hardcap": 1_000_000,
                # maximum amount of protons that can be consumed per time
            },
        },
    },
    "rewriteVisualDefine": {
        "protonSpillover": {
            "name": "Proton Spillover",
            "description": "Protons will decompose into quarks. The more protons you have, the more quarks you will gain.",
            "technicalDescription": "A random amount of protons, capped to 1/2 of your proton gain per second will be turned into quarks\nThe hard cap of protons that can be consumed per second is 1M.",
            "resultDescription": "You are currently gaining %1 quarks per second.",
        },
        "hydrogenSpillover": {
            "name": "Hydrogen Spillover",
            "description": "A random amount of hydrogen will decompose into 2 protons, and 2 electrons.",
            "technicalDescription": "A random amount of hydrogen, capped to 1/2 of your hydrogen gain per second will be turned into protons and electrons.\nThe hard cap of hydrogen that can be consumed per second is 1M. ",
            "resultDescription": "You are currently gaining %1 protons and %2 electrons per second.",
        },
        "quarkEfficency": {
            "name": "Quark Efficency",
            "description": "Protons now cost 2 quarks instead of 3.",
            "technicalDescription": "This will affect everything in the game, for example your Protonic Forges.",
        },
        "folding": {
            "name": "Folding",
            "description": "In exchange for removing your hydrogen spillover, you now gain a multiplier to your proton gain corresponding to how much hydrogen you have.",
            "technicalDescription": "The multiplier is (hydrogen / 100) + 1",
        },
        "hyperfolding": {
            "name": "Hyperfolding",
            "description": "In exchange for removing your proton spillover, you now gain a multiplier to your quark gain corresponding to how much protons you have.",
            "technicalDescription": "The multiplier is (protons / 200) + 1",
        },
    },
    "unlockedRewrites": [],
    "lastAchevementGain": ["nothing", -1],  # achevement name, timestamp
    "sessionStartTime": 0,
    "playTime": 0,
    "tutorialPopupDone": False,
}


@dataclass
class GameDefine:
    # def __init__(self):
    itemVisualDefine: dict

    itemInternalDefine: dict

    automationInternalDefine: dict

    automationVisualDefine: dict

    purchaseToCreate: list[str]
    automationsToCreate: list[str]

    amounts: dict[str, int]

    clickGainMultiplierList: dict[str, list[int | float]]

    multiplierList: dict[str, list[int | float]]

    mainTabBuyMultiple: int

    electronDetails: dict[str, int]
    automationLevels: dict[str, int]

    automationDisabledState: dict[str, list]

    automationDetails: dict

    achevementInternalDefine: dict

    achevementVisualDefine: dict

    unlockedAchevements: list[str | None]

    unlockables: dict

    unlockablesVisualDefine: dict

    unlockedUnlockables: list[str | None]

    rewriteInternalDefine: dict

    rewriteVisualDefine: dict

    unlockedRewrites: list[str | None]

    lastAchevementGain: list

    sessionStartTime: int | float
    playTime: int | float
    tutorialPopupDone: bool


force: list[str] = []  # for force loading

lastAutosaveTime = 0
autosaveTime = 300000


# def loadSave(saveDict: list[dict]):
#     global gamedefine
#     newsave = deepcopy(defualtGameDefine)

#     for item in saveDict:
#         changes = item["changes"]
#         location: str
#         location = item["location"]

#         try:
#             exec(f"newsave{location} = changes")
#         except IndexError:
#             # example where this path would be triggered:
#             # dict = {"hello": []}
#             # diff = [{"changes": 1, "location": ["hello"][2]}]
#             # so in this case, we need to add 3 items to the list, so we reach the third index
#             # this will allow us to use the index based assignment

#             # Ignore the comments above, i've just made it so the item is appended to the list.

#             # make sure all quotes are double
#             location = location.replace("'", '"')

#             # match all keys
#             matches = regex.findall(r"[^[\]]*", location)

#             # remove the last key (which would be the list index)

#             # the regex removes the brackets, we have to add it back

#             matches = [i for i in matches if not len(i) == 0]
#             amount = matches.pop()
#             matches = [f"[{i}]" for i in matches]

#             what = "".join(matches)
#             oldCode = f"""
# toAppend = newsave{what}
# for i in range({amount} + 1):
#     toAppend.append(None)
#             """
#             code = f"newsave{location}.append(changes)"
#             exec(code)

#     gamedefine = from_dict(data_class=GameDefine, data=newsave)
#     gamedefine.mainTabBuyMultiple = 1

#     for item in gamedefine.automationLevels:
#         if gamedefine.automationLevels[item] > 0:
#             automationGameLogic.updateAutomationStatus(item)

#     return gamedefine


def getSaveData(data: GameDefine | None = None) -> list[dict]:
    if data == None:
        savedata = asdict(gamedefine)
    elif type(data) == GameDefine:
        savedata = asdict(data)
    else:
        raise TypeError("Wrong type for data, must be Gamedefine or None")

    return getDiffedSave(savedata)


def getDiffedSave(workingSave: dict) -> list[dict]:
    """Will return a save based on only what has changed between the current gamedefine dict and the default one.

    Returns:
        dict: The diff save.
    """
    print(workingSave)
    rawDiff = str(deepdiff.diff.DeepDiff(defualtGameDefine, workingSave))
    underCookedDiff: list[str]
    underCookedDiff = regex.findall('root[^"]*', rawDiff)

    for i in range(len(underCookedDiff)):
        if not "root" in underCookedDiff[i]:
            underCookedDiff.pop(i)
        underCookedDiff[i] = underCookedDiff[i].replace("root", "")

    cookedDiff: list[dict]
    cookedDiff = []

    for i in underCookedDiff:
        inProgress = {}
        print(f"workingSave{i}")

        inProgress["changes"] = eval(f"workingSave{i}")
        inProgress["location"] = i
        cookedDiff.append(inProgress)

    return cookedDiff


def getSaveMetadata(savedata: GameDefine | None = None) -> dict:
    global gamedefine
    metadata: dict = {"amounts": {}, "achevements": {}}

    if savedata == None:
        savedata = gamedefine

    for i in savedata.amounts:  # type: ignore
        metadata["amounts"][i] = savedata.amounts[i]  # type: ignore

    metadata["playTime"] = savedata.playTime  # type: ignore

    metadata["achevements"]["have"] = len(savedata.unlockedAchevements)  # type: ignore
    metadata["achevements"]["notUnlocked"] = len(savedata.achevementInternalDefine)  # type: ignore
    metadata["lastUsedOn"] = time.time()

    metadata["version"] = repr(gameVersion)

    return metadata


gamedefine = from_dict(data_class=GameDefine, data=defualtGameDefine)
initalized = True
gameVersion: versions.Version = (
    versions.Version(
        quickload.quickload("version.txt", quickload.QuickloadType.TEXT, quickload.ErrorTolerance.FILE_NOT_FOUND)
    )
    if not quickload.quickload("version.txt", quickload.QuickloadType.TEXT, quickload.ErrorTolerance.FILE_NOT_FOUND)
    == "fileNotFound"
    else versions.Version()
)  # type:ignore
theTabWidget: QTabWidget = None  # type:ignore - this will be set to a tabwidget later
# import base64
# def b64Decode(what: str) -> str:
#     return base64.b64decode(what.encode("utf-8")).decode("utf-8")

# f = open("./appdata/local/CreateTheSun/Saves/save.save5", 'r')
# print(loadSave(json.loads(b64Decode(f.read()))))

# f.close()

