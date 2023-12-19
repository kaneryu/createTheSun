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
            "nothing",
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
            "nothing"
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
            "quarks"
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
            "protons"
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
            "hydrogen"
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
            "stars"
        ],
        "defaultCost": 1e57,
        "costEquation": "%1 * 1e57",
        "whatItGives": [
            {
                "what": "galaxies",
                "amount": 1
            }
        ],
    },

    "superclusters": {
        "whatItCosts": [
            "galaxies"
        ],
        "defaultCost": 1e57,
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
                "amount": 5
                            
            },
            {
                "what": "electrons",
                "amount": 100
            },
            {
                "what": "protons",
                "amount": 10
            }
        ],
        
        "upgradeCost" : [            
            {
                "what": "quarks",
                "amount": 5        
            },
            {
                "what": "electrons",
                "amount": 50
            }           
        ],
        
        "maxLevel": 1000,
        "withRequirement": False,
        "type" : "idleGenerator",
        "idleGenerator" : {
                "whatItGives": [
                    {
                        "what": "quarks",
                        "baseAmount": 1
                    }
                ],
                "baseTime": 1000,
                # in this case, %1 is upgrade level
                "timeEquation": "tan(-((%1+30)/600)-90)",
                "maxLevel": 10,
                "whatItGives": [
                        {
                            "what": "quarks",
                            "baseAmount": 1
                        }
                    ],    
        }       
    },
    
    "protonicForge": {
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
                "amount": 50
            }
        ],
        
        "upgradeCost" : [            
            {
                "what": "protons",
                "amount": 100     
            },
            {
                "what": "electrons",
                "amount": 50
            }           
        ],
        
        "maxLevel": 4000,
        
        "type" : "idleGenerator",
        "withRequirement": True,
        "idleGenerator" : {
                "whatItGives": [
                    {
                        "what": "protons",
                        "baseAmount": 1
                    }
                ],
                "baseTime": 1000,
                # in this case, %1 is upgrade level
                "timeEquation": "tan((-(%1+34)/4000)-90)",
                "maxLevel": 10,
                "whatItGives": [
                        {
                            "what": "protons",
                            "baseAmount": 1
                        }
                    ],    
        }       
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
        "upgradeId": ["particleAcceleratorUpgrade", 0]
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
        "upgradeId": ["protonicForgeUpgrade", 0]
    }
    
    
}

purchaseToCreate = ["quarks", "protons"]
upgradesToCreate = ["particleAccelerator", "protonicForge"]

amounts = {
    "quarks": 0,
    "electrons": 0,
    "protons": 0,
    "hydrogen": 0,
    "stars": 0,
    "galaxies": 0,
    "superclusters": 0
}

electronDetails = {
    "waitTime": 1000,
    "amount": 1,
    "maxAmount": 100,
    "minAmount": 0, 
}

upgradeLevels = {
    "particleAccelerator" : 0,
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
        
        "timeToWait": 100,
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