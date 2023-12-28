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
                "amount": 50
                            
            },
            {
                "what": "electrons",
                "amount": 100
            },
            {
                "what": "protons",
                "amount": 20
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
                        "amount": 50       
                    },
                    {
                        "what": "electrons",
                        "amount": 50
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
                        "amount": 30000    
                    },
                    {
                        "what": "electrons",
                        "amount": 60
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
                        "timeEquation": "(%1-30)+3"
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
                        "amount": 50
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
                        "amount": 60
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
            "usefulDescriptionBlank": "tickTime",
            
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
    "quarks": 100,
    "electrons": 100,
    "protons": 100,
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
    "waitTime": 1,
    "amount": 1,
    "maxAmount": 100,
    "minAmount": 0, 
}

upgradeLevels = {
    "particleAccelerator" : 20,
    "protonicForge": 20
}
upgradeDisabledState = {
    "particleAccelerator" : (False, "0"),
    "protonicForge": (False, "0")
}

upgradeDetails = {
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