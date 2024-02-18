import observerModel
from copy import deepcopy
import gamedefine
import time

class data_:
    amounts: dict = {}
    gainPerSecond: dict = {}
    lastCheckedTime: float | int = 0




def receive(event):
    global data
    previous = deepcopy(data.amounts)
    
    for i in gamedefine.gamedefine.amounts:
        data.amounts[i] = gamedefine.gamedefine.amounts[i]
    
    for i in data.amounts:
        if not i in data.gainPerSecond:
            data.gainPerSecond[i] = 0
        else:
            data.gainPerSecond[i] = (data.amounts[i] - previous[i]) / ((time.time() * 1000) - data.lastCheckedTime)
        
    
    data.lastCheckedTime = time.time() * 1000


data = data_() 
itemObserver = observerModel.registerObserver(receive, observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.TIME)
