from src.createthesun.gameLogic import numberLogic
import src.createthesun.observerModel as observerModel
from src.createthesun.__main__ import preStartUp as main_preStartUp

def test_magnitude():
    result = numberLogic.magnitude(1000)
    assert result == 1
    
    result = numberLogic.magnitude(2000)
    assert result == 1
    
    result = numberLogic.magnitude(10_000)
    assert result == 1
    
    result = numberLogic.magnitude(100_000)
    assert result == 1
    
    result = numberLogic.magnitude(1_000_000)
    assert result == 2
    
    result = numberLogic.magnitude(1_000_000_000)
    assert result == 3
    
    result = numberLogic.magnitude(1_000_000_000_000)
    assert result == 4
    
def test_observerModel():
    observerModel.log = {"creationEvents": [], "deregisterEvents": [], "callEvents": [], "recievedEvents": []} # for some reason there is an old log that needs to be cleared
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

    

    # self.assertListEqual(creationLog, [observer1Id, observer2Id, observer3Id])
    assert deregisterLog == [observer1Id, observer2Id]
    assert callLog == [{"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}, {"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}, {"event": observerModel.Observable.ITEM_OBSERVABLE, "callType": observerModel.ObservableCallType.GAINED, "information": "test"}]
    assert recievedLog == [observer1Id, observer2Id, observer2Id, None]
    
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
