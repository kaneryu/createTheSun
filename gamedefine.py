import time
from dataclasses import dataclass, asdict
from dacite import from_dict
from copy import deepcopy
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
                        "timeEquation": "10.5^(-1 * %1 + 100) + 10"
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
                            "timeEquation": "10.5^(-1 * %1 + 100) + 50",
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
        "particleAccelerator" : [False, "0"],
        "protonicForge": [False, "0"]
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

    "unlockables": {
        "hydrogenUnlock": {
                "visual": False,
                "unlockType": "item",
                "whatUnlocks": "hydrogen",
                "needs": [
                    {
                        "type": "automation",
                        "what": "protonicForge",
                        "amount": 3
                    }
                ]
            },
        "rewriteTabUnlock": {
            "visual": False,
            "unlockType": "tab",
            "whatUnlocks": "rewrite",
            "needs": [
                {
                    "type": "item",
                    "what": "hydrogen",
                    "amount": 20
                }
            ]
        },
    },

    "unlockedUnlockables": [],

    "rewriteInternalDefine": {},

    "rewriteVisualDefine": {
        "protonSpillover": {
            "name": "Proton Spillover",
            "description": "A small amount of protons will decompose into 4 quarks.",
            "technicalDescription": "There will be a 5% chance every second that a proton will decompose into 4 quarks."
        },
        "hydrogenSpillover": {
            "name": "Hydrogen Spillover",
            "description": "A small amount of hydrogen will decompose into 2 protons.",
            "technicalDescription": "There will be a 5% chance every second that a hydrogen will decompose into 2 protons."
        },
        "quarkEfficency": {
            "name": "Quark Efficency",
            "description": "Protons now cost 2 quarks instead of 3.",
            "technicalDescription": ""
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
    "tutorialPopupDone": False

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
        
    unlockedAchevements: list[str]

    unlockables: dict
        
    unlockedUnlockables: list[str]

    rewriteInternalDefine: dict

    rewriteVisualDefine: dict
    
    unlockedRewrites: list[str]

    lastAchevementGain: list


    sessionStartTime: int | float
    playTime: int | float
    tutorialPopupDone: bool


    

force: list[str] = [] # for force loading

lastAutosaveTime = 0
autosaveTime = 300000

def loadSave(saveDict: dict):
    global gamedefine, force
    
    newDict = deepcopy(defualtGameDefine)
    newDict.update(saveDict)
    
    gamedefine = from_dict(data_class=GameDefine, data=newDict)
    gamedefine.mainTabBuyMultiple = 1
    
    return gamedefine
    
def getSaveData(savedata: GameDefine | None = None) -> dict:
    global gamedefine, defualtGameDefine
    
    saveable = ["amounts", "clickGainMultiplierList", "multiplierList", "upgradeLevels", "upgradeDisabledState", "upgradeDetails", "unlockedAchevements", "electronDetails", "unlockedUnlockables", "purchaseToCreate", "automationsToCreate", "playTime"]
    toRemove = []
    for i in defualtGameDefine:
        if i not in saveable:
            toRemove.append(i)
    
    
    if savedata == None:
        savedata = gamedefine

    
    saveDict = asdict(savedata)
    
    for i in toRemove:
        saveDict.pop(i)
    
    # print(f"made save {saveDict}")
    return saveDict    

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
    

# testdict_ = {'amounts': {'quarks': 100037, 'electrons': 100, 'protons': 1000000, 'hydrogen': 0, 'stars': 0, 'galaxies': 0, 'superclusters': 0}, 'clickGainMultiplierList': {'quarks': [1], 'electrons': [1], 'protons': [1], 'hydrogen': [1], 'stars': [1], 'galaxies': [1], 'superclusters': [1]}, 'multiplierList': {'quarks': [1], 'electrons': [1], 'protons': [1], 'hydrogen': [1], 'stars': [1], 'galaxies': [1], 'superclusters': [1]}, 'upgradeLevels': {'particleAccelerator': 2, 'protonicForge': 0}, 'upgradeDisabledState': {'particleAccelerator': (False, '0'), 'protonicForge': (False, '0')}, 'upgradeDetails': {'particleAccelerator': {'timeToWait': 428.134117105719, 'whatItGives': [{'what': 'quarks', 'amount': 1}]}, 'protonicForge': {'timeToWait': 1000, 'whatItGives': [{'what': 'protons', 'amount': 1}], 'whatItCosts': [{'what': 'quarks', 'amount': 3}]}}, 'unlockedAchevements': [], 'electronDetails': {'waitTime': '0.2f', 'amount': 1, 'maxAmount': 100, 'minAmount': 0}, 'unlockedUnlockables': ['hydrogenUnlock', 'upgradeTabUnlock', 'protonSpilloverUnlock'], 'purchaseToCreate': ['quarks', 'protons', 'hydrogen'], 'automationsToCreate': ['particleAccelerator', 'protonicForge']}

# print(convertFloatsToStr(testdict_))

gamedefine = from_dict(data_class=GameDefine, data=defualtGameDefine)
initalized = True