visualGameDefine = {
    "quarks": {
        "visualName": "Quarks",
        "description": "Quarks are the building blocks of protons. They are made of nothing...?",
        "id": ["quarks", 0]
    },
    "electrons": {
        "visualName": "Electrons",
        "description": "Electrons are the building blocks of atoms. They are made of nothing...?",
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

internalGameDefine = {
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
            "amount": 1
            }
        ],
        "defaultCost": 1,
        "costEquation": "%1 * 6",
        "whatItGives": [
            {
                "what": "protons",
                "amount": 2
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

upgradeInternalDefine = {
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
        
        "maxLevel": 50,
        
        "withRequirement": False,
        "type" : "idleGenerator",
        "idleGenerator" : {
                "whatItGives": [
                    {
                        "what": "quarks",
                        "amount": 1
                    }
                ],
                "time": 1000,
                # in this case, %1 is upgrade level
                "equationType": "timeEquation",
                "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))",   
        },
        
        "multiLevelUpgradesOn": True,
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
                "idleGenerator" : {
                    "whatItGives": [
                        {
                            "what": "quarks",
                            "amount": 1
                        }
                    ],
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
                "idleGenerator" : {
                    "whatItGives": [
                        {
                            "what": "quarks",
                            "amount": 3
                        }
                    ],
                    "time": 1000,
                    # in this case, %1 is upgrade level
                    "equationType": "whatItGivesEQ",
                    "timeEquation": "(x-30)+3"
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
        
        "maxLevel": 100,
        "type" : "idleGenerator",
        "withRequirement": True,
        "idleGenerator" : {
                "whatItGives": [
                    {
                        "what": "protons",
                        "baseAmount": 1
                    }
                ],
                "whatItCosts": [
                    {
                        "what": "quarks",
                        "amount": 3     
                    }
                ],
                "time": 1000,
                # in this case, %1 is upgrade level
                "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))",
        },
        
        "multiLevelUpgradesOn": True,
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
                    },
                ],
                "idleGenerator" : {
                    "whatItGives": [
                        {
                            "what": "protons",
                            "baseAmount": 1
                        }
                    ],
                    "time": 1000,
                    # in this case, %1 is upgrade level
                    "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))"
                }
            },
            {
                "startLevel": 50,
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
                "idleGenerator" : {
                    "whatItGives": [
                        {
                            "what": "protons",
                            "baseAmount": 3
                        }
                    ],
                    "whatItCosts": [
                        {
                            "what": "quarks",
                            "amount": 5
                        }
                    ],
                    "time": 1000,
                    # in this case, %1 is upgrade level
                    "timeEquation": "abs(tan(-((%1+34)/600)-10.93791))"
                }
            }

        ]
        
    }
}
    
    
upgradeVisualDefine = {
    
    "particleAccelerator": {
        "visualName": "Particle Accelerator",
        "description": "Accelerates particles to create quarks.",
        "id": ["particleAccelerator", 0],
        
        "upgradeVisualName": "Increase Loop Size",
        "upgradeDescription": "Increase the size of the particle accelerator loop for more quarks per second.",
        "firstupgradeUsefulDescription": "Creates 1 Quark per second",
        "currentUpgradeUsefulDescription": ["You are currently gaining 1 Quark every ", "%%%", " seconds"],
        "upgradeUsefulDescription": ["Upgrade to gain 1 Quark every  ", "%%%", " seconds"],
        "usefulDescriptionBlank": "tickTime",
        "upgradeId": ["particleAcceleratorUpgrade", 0],
        
        "multiLevelUpgrades": [
            {
                "default": True                
            },
            {
                "default": False,
                "description": "Somebody spilled coffee on the accelerator, causing it to go 3x faster!",
                "currentUpgradeUsefulDescription": ["You are currently gaining 3 Quarks every ", "%%%", " seconds"],
                "upgradeUsefulDescription": ["Upgrade to gain 3 Quarks every ", "%%%", " seconds"],
                "visualName": "Particle Accelerator",
                "description": "Accelerates particles to create quarks."
            }
        ]
    },
    "protonicForge": {
        "visualName": "Protonic Forge",
        "description": "Automatically combines quarks into protons.",
        "id": ["protonicForge", 0],
        
        "upgradeVisualName": "Increase Forge Size",
        "upgradeDescription": "Increase the size of the forge, allowing for more quarks to be combined into protons per second",
        "firstupgradeUsefulDescription": "Creates 1 Proton per second",
        "currentUpgradeUsefulDescription": ["You are currently gaining 1 Proton every ", "%%%", " seconds"],
        "upgradeUsefulDescription": ["Upgrade to gain 1 Proton every ", "%%%", " seconds"],
        "usefulDescriptionBlank": "tickTime",
        "upgradeId": ["protonicForgeUpgrade", 0],
        
        "multiLevelUpgrades": [
            {
                "default": True                
            },
            {
                "default": False,
                "description": "A new breakthrough has lead to 3x more proton production!",
                "currentUpgradeUsefulDescription": ["You are currently gaining 3 Protons every ", "%%%", " seconds"],
                "upgradeUsefulDescription": ["Upgrade to gain 3 Protons every ", "%%%", " seconds"],
                "visualName": "Blast Protonic Forge",
                "description": "Accelerates particles to create quarks."
            }
        ]
    }
    
    
}

purchaseToCreate = ["quarks", "protons", "hydrogen"]
upgradesToCreate = ["particleAccelerator", "protonicForge"]

amounts = {
    "quarks": 99999999999999999999999999999999,
    "electrons": 0,
    "protons": 99999999999999999999999999999999,
    "hydrogen": 0,
    "stars": 0,
    "galaxies": 0,
    "superclusters": 0
}

electronDetails = {
    "waitTime": 1,
    "amount": 1,
    "maxAmount": 100,
    "minAmount": 0, 
}

upgradeLevels = {
    "particleAccelerator" : 30,
    "protonicForge": 0
}

upgradeDetails = {
    "particleAccelerator" : {
        "timeToWait" : 1000,
        "whatYouGet" : [
            {
                "what": "quarks",
                "amount": 1
            }
        ]
    },
    
    "protonicForge": {
        
        "timeToWait": 1000,
        "whatYouGet": [
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