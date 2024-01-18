itemVisualDefine = {
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
}

itemInternalDefine = {
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
}

automationInternalDefine = {
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
                        "amount": 300       
                    },
                    {
                        "what": "electrons",
                        "amount": 25
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
                        "amount": 370    
                    },
                    {
                        "what": "electrons",
                        "amount": 50
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
                "amount": 1500
                            
            },
            {
                "what": "electrons",
                "amount": 100
            },
            {
                "what": "protons",
                "amount": 400
            }
        ],
        
        "multiLevelUpgradesStarts": [1, 50],
        
        "multiLevelUpgrades": [
            {
                "startLevel": 1,

                "upgradeCost" : [            
                    {
                        "what": "protons",
                        "amount": 200     
                    },
                    {
                        "what": "electrons",
                        "amount": 25
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
                        "amount": 350     
                    },
                    {
                        "what": "electrons",
                        "amount": 50
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
                            "equation": "(%1-45)/5",
                            
                        }
                        
                        
                        
                    ]
                }
            }

        ]
        
    }
}
    
    
automationVisualDefine = {
    
    "particleAccelerator": [
        {
            "default": False,
            "visualName": "Particle Accelerator",
            "description": "Accelerates particles to create quarks.",
            
            "upgradeVisualName": "Increase Loop Size",
            "upgradeDescription": "Increase the size of the particle accelerator loop for more quarks per second.",
            "firstupgradeUsefulDescription": "Creates 1 Quark per second",
            
            "currentUpgradeUsefulDescription": "You are currently gaining 1 Quarks every %%% seconds",
            "upgradeUsefulDescription": "Upgrade to gain 1 Quarks every %%% seconds",
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
    }

purchaseToCreate = ["quarks", "protons"]
automationsToCreate = ["particleAccelerator", "protonicForge"]

amounts = {
    "quarks": 100000,
    "electrons": 100,
    "protons": 1000000,
    "hydrogen": 0,
    "stars": 0,
    "galaxies": 0,
    "superclusters": 0
}

clickGainMultiplierList = {
    "quarks": [1],
    "electrons": [1],
    "protons": [1],
    "hydrogen": [1],
    "stars": [1],
    "galaxies": [1],
    "superclusters": [1]
}

multiplierList = {
    "quarks": [1],
    "electrons": [1],
    "protons": [1],
    "hydrogen": [1],
    "stars": [1],
    "galaxies": [1],
    "superclusters": [1]
}

mainTabBuyMultiple = 1

electronDetails = {
    "waitTime": 0.2,
    "amount": 1,
    "maxAmount": 100,
    "minAmount": 0, 
}

automationLevels = {
    "particleAccelerator" : 2,
    "protonicForge": 0
}
automationDisabledState = {
    "particleAccelerator" : (False, "0"),
    "protonicForge": (False, "0")
}

automationDetails = {
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
}

achevementInternalDefine = {
    "theBeginning": {
        
        "hidden": False,
        
        "whatItRequires": [
            {
                "what": "quarks",
                "amount": 1
            },
            {
                "what": "protons",
                "amount": 1                
            }        
        ],
        
        "type": "show",
        "whatItGives": [
            {
                "what": "nothing",
                "amount": -1
            }
        ]
    },
    
    "automation": {
        "hidden": False,
        "whatItRequires": [
            {
                "what": "particleAccelerator",
                "amount": 1
            }  
        ],
        "type": "itemReward",
        "whatItGives": [
            {
                "what": "protons",
                "amount": 10
            }
        ]
    }
}

achevementVisualDefine = {
    "theBeginning": {
        "visualName": "The Beginning",
        "hoverDescription": "At the start, there was nothing... \n Create your first quark and proton" 
    },
    
    "automation": {
        "visualName": "Automation",
        "hoverDescription": "Automation is upon us. \n Create your first particle accelerator",
        "rewardDescription": "Unlock to recive 10 protons"
    }
}

unlockedAchevements = []

unlockables = {
    "hydrogenUnlock": {
            "visual": False,
            "unlockType": "item",
            "whatUnlocks": "hydrogen",
            "needs": [
                {
                    "type": "automation",
                    "what": "particleAccelerator",
                    "amount": 2
                }
            ]
        },
    "upgradeTabUnlock": {
            "visual": False,
            "unlockType": "tab",
            "whatUnlocks": "upgradeTab",
            "needs": [
                {
                    "type": "item",
                    "what": "protons",
                    "amount": 2000                
                },
                {
                    "type": "time",
                    "what": "timePlayed",
                    "amount": 0 #just for future refrence
                }
            ]
        },
    "protonSpilloverUnlock": {
            "visual": False,
            "unlockType": "upgrade",
            "whatUnlocks": "protonSpillover",
            "needs": [
                {
                    "type": "item",
                    "what": "protons",
                    "amount": 2000
                }                
            ]
        }
}

unlockedUnlockables = []








saveable = [amounts, clickGainMultiplierList, multiplierList, automationLevels, automationDisabledState, automationDetails, unlockedAchevements, electronDetails, unlockedUnlockables, purchaseToCreate, automationsToCreate]
saveableStr = ["amounts", "clickGainMultiplierList", "multiplierList", "upgradeLevels", "upgradeDisabledState", "upgradeDetails", "unlockedAchevements", "electronDetails", "unlockedUnlockables", "purchaseToCreate", "automationsToCreate"]
force = [] # for force loading

lastAutosaveTime = 0
autosaveTime = 300000

def loadSave(saveDict: dict):
    global amounts, clickGainMultiplierList, multiplierList, automationLevels, automationDisabledState, automationDetails, unlockedAchevements, electronDetails, unlockedUnlockables, purchaseToCreate, automationsToCreate
    saveDict = convertStrToFloats(saveDict) # type: ignore
    for i in saveableStr:
        if not i in saveDict:
            saveDict[i] = ""
            
    amounts = saveDict["amounts"]
    clickGainMultiplierList = saveDict["clickGainMultiplierList"]
    multiplierList = saveDict["multiplierList"]
    automationLevels = saveDict["upgradeLevels"]
    automationDisabledState = saveDict["upgradeDisabledState"]
    automationDetails = saveDict["upgradeDetails"]
    unlockedAchevements = saveDict["unlockedAchevements"]
    electronDetails = saveDict["electronDetails"]
    unlockedUnlockables = saveDict["unlockedUnlockables"]
    purchaseToCreate = saveDict["purchaseToCreate"]
    automationsToCreate = saveDict["automationsToCreate"]
    
def getSaveData():
    saveDict = {}
    for i in range(len(saveable)):
        saveDict[saveableStr[i]] = saveable[i]
    print(convertFloatsToStr(saveDict))
    return convertFloatsToStr(saveDict)    

def convertFloatsToStr(input: dict | list):
    def convertFloatsToStrFromList(input_: list):
        workingList = input_
        for i in workingList:
            if type(i) == dict:
                convertFloatsToStrFromDict(i)
            if type(i) == list:
                convertFloatsToStrFromList(i)
            if type(i) == float:
                workingList[workingList.index(i)] = str(i) + "f" #bruhhhh why doesnt i = str(i) + "f" work
        return workingList
                
    def convertFloatsToStrFromDict(input: dict):
        for keys in input:
            if type(input[keys]) == float:
                input[keys] = str(input[keys]) + "f"
            if type(input[keys]) == dict:
                input[keys] = convertFloatsToStrFromDict(input[keys])
            if type(input[keys]) == list:
                input[keys] = convertFloatsToStrFromList(input[keys])
        return input
    
    if type(input) == dict:
        return convertFloatsToStrFromDict(input)
    if type(input) == list:
        return convertFloatsToStrFromList(input)    
    

def convertStrToFloats(input: dict):
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
    

testdict_ = {'amounts': {'quarks': 1138772.00000000, 'electrons': 100, 'protons': 2161998.60000018, 'hydrogen': 0, 'stars': 0, 'galaxies': 0, 'superclusters': 0}, 'clickGainMultiplierList': {'quarks': [1], 'electrons': [1], 'protons': [1], 'hydrogen': [1], 'stars': [1], 'galaxies': [1], 'superclusters': [1]}, 'multiplierList': {'quarks': [1], 'electrons': [1], 'protons': [1], 'hydrogen': [1], 'stars': [1], 'galaxies': [1], 'superclusters': [1]}, 'upgradeLevels': {'particleAccelerator': 127, 'protonicForge': 68}, 'upgradeDisabledState': {'particleAccelerator': (False, '0'), 'protonicForge': (False, '0')}, 'upgradeDetails': {'particleAccelerator': {'timeToWait': 10, 'whatItGives': [{'what': 'quarks', 'amount': 100.000000000000}]}, 'protonicForge': {'timeToWait': 10, 'whatItGives': [{'what': 'protons', 'amount': 4.60000000000000}], 'whatItCosts': [{'what': 'quarks', 'amount': 'atMarketPrice'}]}}, 'unlockedAchevements': [], 'electronDetails': {'waitTime': 1000, 'amount': 100, 'maxAmount': 100, 'minAmount': 0}, 'unlockedUnlockables': [], 'purchaseToCreate': ['quarks', 'protons'], 'automationsToCreate': ['particleAccelerator', 'protonicForge']}
