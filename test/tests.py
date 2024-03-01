import unittest
from gameLogic import numberLogic
import observerModel
import gamedefine
import random
import dacite

class numberLogicTests(unittest.TestCase):
    def test_magnitude(self):
        result = numberLogic.magnitude(1000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(2000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(10_000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(100_000)
        self.assertEqual(result, 1)
        
        result = numberLogic.magnitude(1_000_000)
        self.assertEqual(result, 2)
        
        result = numberLogic.magnitude(1_000_000_000)
        self.assertEqual(result, 3)
        
        result = numberLogic.magnitude(1_000_000_000_000)
        self.assertEqual(result, 4)
        
class observerModelTests(unittest.TestCase):
    def test_observerModel(self):
        observer1 = observerModel.registerObserver(lambda x: print("test"), observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED)
        observer2 = observerModel.registerObserver(lambda x: print("test2"), observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED)
        observer3 = observerModel.registerObserver(lambda x: print("notShown"), observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.TIME)

        observerModel.callEvent(observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED, "test")

        observer1.deregister()

        observerModel.callEvent(observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED, "test")

        observer2.deregister()

        observerModel.callEvent(observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.GAINED, "test")
        
        observer1Id = observer1.id
        observer2Id = observer2.id
        observer3Id = observer3.id
        
        creationLog = observerModel.log["creationEvents"]
        deregisterLog = observerModel.log["deregisterEvents"]
        callLog = observerModel.log["callEvents"]
        recievedLog = observerModel.log["recievedEvents"]

        
        self.assertListEqual(creationLog, [observer1Id, observer2Id, observer3Id])
        self.assertListEqual(deregisterLog, [observer1Id, observer2Id])
        self.assertListEqual(callLog, [{"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}, {"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}, {"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}])
        self.assertListEqual(recievedLog, [observer1Id, observer2Id, observer2Id, None])
        
        # we expect:
        # observer1 to be created
        # observer2 to be created
        # observer3 to be created
        # then
        # observer1 called
        # observer2 called
        # observer3 NOT called
        # then
        # observer1 deregistered
        # then
        # observer1 NOT called
        # observer2 called
        # observer3 NOT called

        
class saveLoadTests(unittest.TestCase):
    def test_saveLoad(self):
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
    
            self.assertEqual(saveMeta["amounts"][amountToChange], amountToChangeValue)
            
            
            loadedSave = gamedefine.loadSave(save)
            
            self.assertEqual(loadedSave.amounts[amountToChange], amountToChangeValue)
            self.assertEqual(loadedSave.automationLevels[upgradeToLevel], upgradeToLevelValue)
            
            
            
        

    
if __name__ == '__main__':
    unittest.main()