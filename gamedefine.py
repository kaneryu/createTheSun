import time
from dataclasses import dataclass, asdict
from dacite import from_dict
from copy import deepcopy
import json
import regex
import deepdiff
from PySide6.QtWidgets import QTabWidget
from gameLogic import automationGameLogic
import versions
import quickload

initalized = False

defualtGameDefine = {
    "itemVisualDefine": {
        "quarks": {
            "visualName": "Quarks",
            "description": "Quarks are the building blocks of protons. They are made of nothing...?",
            "id": ["quarks", 0]
        },
        "electrons": {
            "visualName": "Electrons",
            "description": "Electrons are the building blocks of atoms.",
            "id": ["electrons", 1]
        },
        "protons": {
            "visualName": "Protons",
            "description": "Protons are the building blocks of atoms. They are made of quarks.",
            "id": ["protons", 2]
        },
        "hydrogen": {
            "visualName": "Hydrogen",
            "description": "Hydrogen is the simplest element. It is made of one proton and one electron.",
            "id": ["hydrogen", 3]
        },
        "stars": {
            "visualName": "Stars",
            "description": "Stars are the building blocks of galaxies. They are made of hydrogen.",
            "id": ["stars", 4]
        },
        "galaxies": {
            "visualName": "Galaxies",
            "description": "Galaxies are the building blocks of superclusters. They are made of stars.",
            "id": ["galaxies", 5]
        },
        "superclusters": {
            "visualName": "Superclusters",
            "description": "Superclusters are the building blocks of the universe. They are made of galaxies.",
            "id": ["superclusters", 6]
        }
    },

    "itemInternalDefine": {
        "quarks": {
            "whatItCosts": [
                {
                "what": "nothing",
                "amount": -1
                }
            ],

            "defaultCost": -1,
            "costEquation": "",
            "whatItGives": [
                {
                    "what": "quarks",
                    "amount": 1
                }
            ],
        },

        "electrons": {
            "whatItCosts": [
                {
                "what": "nothing",
                "amount": -1
                }
            ],

            "defaultCost": -1,
            "costEquation": "",
            "whatItGives": [
                {
                    "what": "electrons",
                    "amount": 1
                }
            ],
        },

        "protons": {
            "whatItCosts": [
                {
                "what": "quarks",
                "amount": 3
                }
            ],
            "defaultCost": 3,
            "costEquation": "%1 * 3",
            "whatItGives": [
                {
                    "what": "protons",
                    "amount": 1
                }
            ],
        },

        "hydrogen": {
            "whatItCosts": [
                {
                "what": "protons",
                "amount": 1
                },
                {
                "what": "electrons",
                "amount": 1
                }
            ],
            "defaultCost": 1,
            "costEquation": "%1 * 1",
            "whatItGives": [
                {
                    "what": "hydrogen",
                    "amount": 1
                }
            ],
        },

        "stars": {
            "whatItCosts": [
                {
                "what": "hydrogen",
                "amount": 1e57
                }
            ],
            "defaultCost": 1e57,
            "costEquation": "%1 * 1e57",
            "whatItGives": [
                {
                    "what": "Stars",
                    "amount": 2
                }
            ],
        },

        "galaxies": {
            "whatItCosts": [
                {
                "what": "stars",
                "amount": 1e11
                },
            ],
            "defaultCost": 1e11,
            "costEquation": "%1 * 1e11",
            "whatItGives": [
                {
                    "what": "galaxies",
                    "amount": 1
                }
            ],
        },

        "superclusters": {
            "whatItCosts": [
                {
                "what": "galaxies",
                "amount": 100000
                }
            ],
            "defaultCost": 100000,
            "costEquation": "%1 * 100000",
            "whatItGives": [
                {
                    "what": "superclusters",
                    "amount": 1
                }
            ],
        }
    },

    "automationInternalDefine": {
        "particleAccelerator": {
            "firstCost": [
                {
                    "what": "quarks",
                    "amount": 100
                                
                },
                {
                    "what": "electrons",
                    "amount": 100
                },
                {
                    "what": "protons",
                    "amount": 30
                }
            ],
        
            "maxLevel": 50,
            
            "multiLevelUpgradesStarts": [1, 30],
            "multiLevelUpgrades": [
                {
                    "startLevel": 1,
                    "upgradeCost" : [            
                        {
                            "what": "quarks",
                            "amount": "(%1 - 1) * 15 + 100",
                            "variables": ["level"]
                        },
                        {
                            "what": "electrons",
                            "amount": "1.1^((-1 * %1) + 34.5) + 10",
                            "variables": ["level"]
                        }      
                    ],
                    "withRequirement": False,
                    "type": "idleGenerator",
                    "idleGenerator" : {
                        "whatItGives": [
                            {
                                "what": "quarks",
                                "amount": 1
                            }
                        ],
                        "withRequirement": False,
                        "time": 1000,
                        # in this case, %1 is upgrade level
                        "equationType": "timeEquation",
                        "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))"
                    }
                        
                },
                {
                    "startLevel": 30,
                    "upgradeCost" : [            
                        {
                            "what": "quarks",
                            "amount": "(%1 - 1) * 30 - 500",
                            "variables": ["level"] 
                        },
                        {
                            "what": "electrons",
                            "amount": "1.04^((-1 * %1) + 82) + 4",
                            "variables": ["level"]
                        }      
                    ],
                    "withRequirement": False,
                    "type": "idleGenerator",
                    "idleGenerator" : {
                        "withRequirement": False,
                        "whatItGives": [
                            {
                                "what": "quarks",
                                "amount": 3
                            }
                        ],
                        "time": 10,
                        # in this case, %1 is upgrade level
                        "equationType": "amountEquation",
                        "amountEquation": [
                            {
                            "equation": "(%1-30)+3"
                            }
                        ]
                    }
                        
                }

            ]       
        },
        
        "protonicForge": {
            "firstCost": [
                {
                    "what": "quarks",
                    "amount": 500
                                
                },
                {
                    "what": "electrons",
                    "amount": 100
                },
                {
                    "what": "protons",
                    "amount": 200
                }
            ],
            
            "multiLevelUpgradesStarts": [1, 50],
            
            "multiLevelUpgrades": [
                {
                    "startLevel": 1,

                    "upgradeCost" : [            
                        {
                            "what": "protons",
                            "amount": "((%1-1)*30+200)",
                            "variables": ["level"]   
                        },
                        {
                            "what": "electrons",
                            "amount": "1.1^(-1*%1+34.5)+14",
                            "variables": ["level"]
                        }
                    ],
                    
                    "maxLevel": 50,
                    "type" : "idleGenerator",
                    "withRequirement": True,
                    "idleGenerator" : {
                            "whatItGives": [
                                {
                                    "what": "protons",
                                    "amount": 1
                                }
                            ],
                            "type" : "idleGenerator",
                            "withRequirement": True,
                            "whatItCosts": [
                                {
                                    "what": "quarks",
                                    "amount": "atMarketPrice"     
                                }
                            ],
                            "time": 1000,
                            "equationType": "timeEquation",
                            # in this case, %1 is upgrade level
                            "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))",
                    },
            
                },
            
            
            
                {
                    "startLevel": 50,
                    "maxLevel": 150,
                    "upgradeCost" : [            
                        {
                            "what": "protons",
                            "amount": "(%1-1)*60 - 500",
                            "variables": ["level"] 
                        },
                        {
                            "what": "electrons",
                            "amount": "1.1^(-1*%1+34.5)+14",
                            "variables": ["level"]
                        },
                    ],
                    "type" : "idleGenerator",
                    "withRequirement": True,
                    "idleGenerator" : {
                        "withRequirement": True,
                        "whatItGives": [
                            {
                                "what": "protons",
                                "amount": 1
                            }
                        ],
                        "whatItCosts": [
                            {
                                "what": "quarks",
                                "amount": "atMarketPrice"
                            }
                        ],
                        "time": 10,
                        "equationType": "amountEquation",
                        # in this case, %1 is upgrade level
                        "amountEquation": [
                            {
                                "equation": "(%1-45)/2+3",
                            }

                        ]
                    }
                }

            ]
            
        }
    },
        
        
    "automationVisualDefine": {
        
        "particleAccelerator": [
            {
                "default": False,
                "visualName": "Particle Accelerator",
                "description": "Accelerates particles to create quarks.",
                
                "upgradeVisualName": "Increase Loop Size",
                "upgradeDescription": "Increase the size of the particle accelerator loop for more quarks per second.",
                "firstupgradeUsefulDescription": "Creates 1 Quark per second",
                
                "currentUpgradeUsefulDescription": "You are currently gaining 1 Quark every %%% seconds",
                "upgradeUsefulDescription": "Upgrade to gain 1 Quark every %%% seconds",
                "usefulDescriptionBlank": "tickTime",
                "disabledText": "How are you seeing this?",
                
                "id": ["particleAccelerator", 0]
                
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
                
                "id": ["particleAccelerator", 0]

            }
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
                    "upgradeId": ["protonicForgeTickUpgrade", 0]       
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
                    
                    "upgradeId": ["protonicForgeAmountUpgrade", 0]    
                }
            ]
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
        "superclusters": 0
    },

    "clickGainMultiplierList": {
        "quarks": [1],
        "electrons": [1],
        "protons": [1],
        "hydrogen": [1],
        "stars": [1],
        "galaxies": [1],
        "superclusters": [1]
    },

    "multiplierList": {
        "quarks": [1],
        "electrons": [1],
        "protons": [1],
        "hydrogen": [1],
        "stars": [1],
        "galaxies": [1],
        "superclusters": [1]
    },

    "mainTabBuyMultiple": 1,

    "electronDetails": {
        "waitTime": 500,
        "amount": 1,
        "maxAmount": 100,
        "minAmount": 0, 
    },

    "automationLevels": {
        "particleAccelerator" : 0,
        "protonicForge": 0
    },
    
    "automationDisabledState": {
        "particleAccelerator" : [False],
        "protonicForge": [False]
    },

    "automationDetails": {
        "particleAccelerator" : {
            "timeToWait" : 1000,
            "whatItGives" : [
                {
                    "what": "quarks",
                    "amount": 1
                }
            ]
        },
        
        "protonicForge": {
            
            "timeToWait": 1000,
            "whatItGives": [
                {
                    "what": "protons",
                    "amount": 1
                }
            ],
            "whatItCosts": [
                {
                    "what": "quarks",
                    "amount": 3     
                }
            ]
        }
    },

    "achevementInternalDefine": {
        "theBeginning": {
            "hidden": False,
            
            "whatItRequires": [
                {
                    "type": "item",
                    "what": "quarks",
                    "amount": 1
                },
                {
                    "type": "item",
                    "what": "protons",
                    "amount": 1                
                }        
            ],
            
            "type": "show",
            "whatItGives": [
                {
                    "type": "item",
                    "what": "nothing",
                    "amount": -1
                }
            ]
        },
        
        "automation": {
            "hidden": False,
            "whatItRequires": [
                {
                    "type": "automation",
                    "what": "protonicForge",
                    "amount": 1
                }  
            ],
            "type": "itemReward",
            "whatItGives": [
                {
                    "type": "item",
                    "what": "protons",
                    "specialAmount": False,
                    "amount": 10
                }
            ]
        },
        
        "rewrite": {
            "hidden": False,
            "whatItRequires": [
                {
                    "type": "item",
                    "what": "hydrogen",
                    "amount": 10
                }  
            ],
            "type": "show",
            "whatItGives": [
                {
                    "type": "item",
                    "what": "nothing",
                    "specialAmount": False,
                    "amount": -1
                }
            ]
        },
        
        "perpetualMotion": {
            "hidden": False,
            "whatItRequires": [
                {
                    "type": "rewrite",
                    "what": "protonSpillover",
                    "amount": 1
                }  
            ],
            "type": "itemReward",
            "whatItGives": [
                {
                    "type": "item",
                    "what": "quarks",
                    "specialAmount": True,
                    "amount" : {"type": "double", "cap": 100_000_000}
                }
            ]
        }
    },

    "achevementVisualDefine": {
        "theBeginning": {
            "visualName": "The Beginning",
            "hoverDescription": "At the start, there was nothing... \n Create your first quark and proton.",
            "rewardDescription": ""
        },
        
        "automation": {
            "visualName": "Automation",
            "hoverDescription": "Automation is upon us. \n Create your first protonic forge.",
            "rewardDescription": "Unlock to recive 10 protons"
        },
        
        "rewrite": {
            "visualName": "Rewrite",
            "hoverDescription": "The universe is being rewritten. \n Unlock the rewrite tab.",
            "rewardDescription": ""
        },
        
        "perpetualMotion": {
            "visualName": "Perpetual Motion",
            "hoverDescription": "Pretty sure that's illegal somehow... \n Unlock the Proton Spillover rewrite.",
            "rewardDescription": "Gain double your current amount of quarks, capped to 100M"
        }
    },

    "unlockedAchevements": [],

    "unlockables": { # if visible is set to true, a corresponding visual define must be set. It's not required if it's set to false
        "hydrogenUnlock": {
                "visible": True,
                "unlockType": "item",
                "whatUnlocks": "hydrogen",
                "needs": [
                    {
                        "type": "automation",
                        "what": "protonicForge",
                        "amount": 3
                    },
                    {
                        "type": "item",
                        "what": "quarks",
                        "amount": 1000
                    },
                    {
                        "type": "item",
                        "what": "protons",
                        "amount": 50
                    }
                ],
                "makeVisible": ["rewriteTabUnlock"]
            },
        "rewriteTabUnlock": {
            "visible": False,
            "unlockType": "tab",
            "whatUnlocks": "rewrite",
            "needs": [
                {
                    "type": "item",
                    "what": "hydrogen",
                    "amount": 20000
                },
                {
                    "type": "item",
                    "what": "protons",
                    "amount": 100_000
                }
            ],
            "makeVisible": None
        },
    },
    
    "unlockablesVisualDefine": {
        "hydrogenUnlock": {
            "visualName": "Hydrogen Unlock",
            "hoverDescription": "Unlock Hydrogen",
            "scale": "linear" # for the progress bar, options are linear or log
        },
        "rewriteTabUnlock": {
            "visualName": "Rewrite Tab Unlock",
            "hoverDescription": "Unlock the rewrite tab",
            "scale": "linear"
        }
    },

    "unlockedUnlockables": [],

    "rewriteInternalDefine": {
        "protonSpillover": {
            "cost": [
                {
                    "what": "quarks",
                    "amount": 10000
                },
                {
                    "what": "protons",
                    "amount": 2000
                },
                {
                    "what": "hydrogen",
                    "amount": 100
                },
                {
                    "what": "electrons",
                    "amount": 100
                }
            ],
            "type": "spillover",
            "spillover": {
                "time": 100,
                "takes": {
                        "what": "protons",
                        "amount": 1
                    },
                
                "gives": [
                    {
                        "what": "quarks",
                        "amount": 4
                    }
                ],
                
                "cap": "%1 / 2",
                "capvar": ["gainPerSecond"],
                # 1/2 of the proton gain per second
                "hardcap": 1_000_000
                # maximum amount of protons that can be consumed per time
            }            
        },
        
        "hydrogenSpillover": {
             "cost": [
                {
                    "what": "quarks",
                    "amount": 50_000_000
                },
                {
                    "what": "protons",
                    "amount": 10_000
                },
                {
                    "what": "hydrogen",
                    "amount": 10_000
                },
                {
                    "what": "electrons",
                    "amount": 100
                }
            ],
            "type": "spillover",
            "spillover": {
                "time": 100,
                "takes": {
                        "what": "hydrogen",
                        "amount": 1
                    },
                
                "gives": [
                    {
                        "what": "protons",
                        "amount": 2
                    },
                    {
                        "what": "electrons",
                        "amount": 2
                    }
                ],
                
                "cap": "%1 / 2",
                "capvar": ["gainPerSecond"],
                # 1/2 of the proton gain per second
                "hardcap": 1_000_000
                # maximum amount of protons that can be consumed per time
            }            
        },
        
        
        
    },

    "rewriteVisualDefine": {
        "protonSpillover": {
            "name": "Proton Spillover",
            "description": "Protons will decompose into quarks. The more protons you have, the more quarks you will gain.",
            "technicalDescription": "A random amount of protons, capped to 1/2 of your proton gain per second will be turned into quarks\nThe hard cap of protons that can be consumed per second is 1M.",
            "resultDescription": "You are currently gaining %1 quarks per second."
        },
        "hydrogenSpillover": {
            "name": "Hydrogen Spillover",
            "description": "A random amount of hydrogen will decompose into 2 protons, and 2 electrons.",
            "technicalDescription": "A random amount of hydrogen, capped to 1/2 of your hydrogen gain per second will be turned into protons and electrons.\nThe hard cap of hydrogen that can be consumed per second is 1M. ",
            "resultDescription": "You are currently gaining %1 protons and %2 electrons per second."
        },
        "quarkEfficency": {
            "name": "Quark Efficency",
            "description": "Protons now cost 2 quarks instead of 3.",
            "technicalDescription": "This will affect everything in the game, for example your Protonic Forges."
        },
        "folding": {
            "name": "Folding",
            "description": "In exchange for removing your hydrogen spillover, you now gain a multiplier to your proton gain corresponding to how much hydrogen you have.",
            "technicalDescription": "The multiplier is (hydrogen / 100) + 1"
        },
        "hyperfolding": {
            "name": "Hyperfolding",
            "description": "In exchange for removing your proton spillover, you now gain a multiplier to your quark gain corresponding to how much protons you have.",
            "technicalDescription": "The multiplier is (protons / 200) + 1"
        }
    },

    "unlockedRewrites": [],

    "lastAchevementGain": ["nothing", -1], #achevement name, timestamp


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


    

force: list[str] = [] # for force loading

lastAutosaveTime = 0
autosaveTime = 300000

def loadSave(saveDict: list[dict]):
    global gamedefine    
    newsave = deepcopy(defualtGameDefine)
    
    for item in saveDict:
        changes = item["changes"]
        location: str
        location = item["location"]

        try:
            exec(f"newsave{location} = changes")
        except IndexError:
            # example where this path would be triggered:
            # dict = {"hello": []}
            # diff = [{"changes": 1, "location": ["hello"][2]}]
            # so in this case, we need to add 3 items to the list, so we reach the third index
            # this will allow us to use the index based assignment
            
            # Ignore the comments above, i've just made it so the item is appended to the list.
            
            # make sure all quotes are double
            location = location.replace("'", '"')
            
            # match all keys
            matches = regex.findall(r'[^[\]]*', location)
            
            # remove the last key (which would be the list index)
            
            # the regex removes the brackets, we have to add it back

            matches = [i for i in matches if not len(i) == 0]
            amount = matches.pop()
            matches = [f'[{i}]' for i in matches]
            
            
            what = "".join(matches)
            oldCode = f"""
toAppend = newsave{what}
for i in range({amount} + 1):
    toAppend.append(None)
            """
            code = f"newsave{location}.append(changes)"
            exec(code)
            exec(f"newsave{location} = changes")
            
    gamedefine = from_dict(data_class=GameDefine, data=newsave)
    gamedefine.mainTabBuyMultiple = 1
    
    for item in gamedefine.automationLevels:
        if gamedefine.automationLevels[item] > 0:
            automationGameLogic.updateAutomationStatus(item)

    return gamedefine 
    
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
    underCookedDiff = regex.findall("root[^\"]*", rawDiff)

    for i in range(len(underCookedDiff)):
        if not "root" in underCookedDiff[i]:
            underCookedDiff.pop(i)
        underCookedDiff[i] = underCookedDiff[i].replace("root","")
        
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
    
    for i in savedata.amounts: # type: ignore
        metadata["amounts"][i] = savedata.amounts[i] # type: ignore 
     
    metadata["playTime"] = savedata.playTime # type: ignore
     
    
    metadata["achevements"]["have"] = len(savedata.unlockedAchevements) # type: ignore
    metadata["achevements"]["notUnlocked"] = len(savedata.achevementInternalDefine) # type: ignore
    metadata["lastUsedOn"] = time.time()
    

    
    metadata["version"] = repr(gameVersion)
    
    return metadata
    

def convertFloatsToStr(input: dict | list):
    def convertFloatsToStrFromList(input_: list):
        workingList = input_
        for i in workingList:
            if type(i) == dict:
                print(f"entering {i}")
                workingList[workingList.index(i)] = convertFloatsToStrFromDict(i)
            if type(i) == list:
                print(f"entering {i}")
                workingList[workingList.index(i)] = convertFloatsToStrFromList(i)
            if type(i) == float:
                print(f"fixing {i}")
                workingList[workingList.index(i)] = str(i) + "f" 
        return workingList
                
    def convertFloatsToStrFromDict(input: dict):
        for keys in input:
            if type(input[keys]) == float:
                print(f"fixing {input[keys]}")
                input[keys] = str(input[keys]) + "f"
            if type(input[keys]) == dict:
                print(f"entering {input[keys]}")
                input[keys] = convertFloatsToStrFromDict(input[keys])
            if type(input[keys]) == list:
                print(f"entering {input[keys]}")
                input[keys] = convertFloatsToStrFromList(input[keys])
        return input
    
    if type(input) == dict:
        return convertFloatsToStrFromDict(input)
    if type(input) == list:
        return convertFloatsToStrFromList(input)    
    
def convertStrToFloats(input: (dict | list)):
    def convertStrToFloatsFromList(input_: list):
        workingList = input_
        for i in workingList:
            if type(i) == dict:
                convertStrToFloatFromDict(i)
            if type(i) == list:
                convertStrToFloatsFromList(i)
            if type(i) == str:
                if i.endswith("f") and "." in i:
                    workingList[workingList.index(i)] = float(i[:-1])
        return workingList
                
    def convertStrToFloatFromDict(input: dict):
        for keys in input:
            if type(input[keys]) == str:
                if input[keys].endswith("f") and "." in input[keys]:
                    input[keys] = float(str(input[keys])[:-1])
            if type(input[keys]) == dict:
                input[keys] = convertStrToFloatFromDict(input[keys])
            if type(input[keys]) == list:
                input[keys] = convertStrToFloatsFromList(input[keys])
        return input
    
    if type(input) == dict:
        return convertStrToFloatFromDict(input)
    
    if type(input) == list:
        return convertStrToFloatsFromList(input)   
    



gamedefine = from_dict(data_class=GameDefine, data=defualtGameDefine)
initalized = True
gameVersion: versions.Version = versions.Version(quickload.quickload("version.txt", quickload.QuickloadType.TEXT, quickload.ErrorTolerance.FILE_NOT_FOUND)) if not quickload.quickload("version.txt", quickload.QuickloadType.TEXT, quickload.ErrorTolerance.FILE_NOT_FOUND) == "fileNotFound" else versions.Version("-1.0.0") # type:ignore
theTabWidget: QTabWidget = None # type:ignore - this will be set to a tabwidget later
# import base64
# def b64Decode(what: str) -> str:
#     return base64.b64decode(what.encode("utf-8")).decode("utf-8")

# f = open("./appdata/local/CreateTheSun/Saves/save.save5", 'r')
# print(loadSave(json.loads(b64Decode(f.read()))))

# f.close()
