from . import observerModel,gamedefine
from copy import deepcopy

import time
import dataclasses

@dataclasses.dataclass
class data_:
    amounts: dict
    gainPerSecond: dict
    lastCheckedTime: float | int




def receive(event):
    global data
    previous = deepcopy(data.amounts)
    
    for i in gamedefine.gamedefine.amounts:
        if not i == "electrons":
            data.amounts[i] = gamedefine.gamedefine.amounts[i]
    
    for i in data.amounts:
        if not i in data.gainPerSecond:
            data.gainPerSecond[i] = 0
            print(f"removing {i}")
        else:
            try:
                data.gainPerSecond[i] = round((data.amounts[i] - previous[i]) / ((time.time()) - data.lastCheckedTime), 3)
            except ZeroDivisionError:
                data.gainPerSecond[i] = round((data.amounts[i] - previous[i]) / ((time.time()) - data.lastCheckedTime - 1), 3)
        if data.gainPerSecond[i] < 0:
            data.gainPerSecond[i] = 0
        
    #print("Received" + str(event) + " " + str(data.amounts) + " " + str(data.gainPerSecond) + " " + str(data.lastCheckedTime) + " " + str(time.time() * 1000))
    data.lastCheckedTime = time.time()


data = data_({}, {}, time.time())
itemObserver = observerModel.registerObserver(receive, observerModel.Observable.ITEM_OBSERVABLE, observerModel.ObservableCallType.ALL)
