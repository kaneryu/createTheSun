import createthesun.old.gamedefine as gamedefine
import random
import dacite

def test_saveLoad():
    seeds = [1923, 2000, 2023, 8231]
    
    possibleAmountsToChage = ["quarks", "protons", "hydrogen"]
    possibleAutomationsToLevel = ["particleAccelerator", "protonicForge"]
    
    for seed in seeds:
        random.seed(seed)
        amountToChange = random.choice(possibleAmountsToChage)
        amountToChangeValue = random.randint(1, 100)
        
        upgradeToLevel = random.choice(possibleAutomationsToLevel)
        upgradeToLevelValue = random.randint(1, 100)
        
        testData = dacite.from_dict(data_class=gamedefine.GameDefine, data= gamedefine.defualtGameDefine)
        
        testData.amounts[amountToChange] = amountToChangeValue
        testData.automationLevels[upgradeToLevel] = upgradeToLevelValue
        
        save = gamedefine.getSaveData(testData)
        saveMeta = gamedefine.getSaveMetadata(testData)

        assert saveMeta["amounts"][amountToChange] == amountToChangeValue
        
        
        loadedSave = gamedefine.loadSave(save)
        
        assert loadedSave.amounts[amountToChange] == amountToChangeValue
        assert loadedSave.automationLevels[upgradeToLevel] == upgradeToLevelValue