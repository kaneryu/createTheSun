import achevements
import warnings
from typing import Union
from enum import StrEnum
from PyQt6.QtCore import pyqtSignal

class Observable(StrEnum):
    ITEM_OBSERVABLE = "itemObserv"
    #Will be called when an item is gained through manually, and will be called every 5 seconds with the current item amounts
    ACHEVEMENT_OBSERVABLE = "acheObserv"
    #Will be called when an achevement is earned
    AUTOMATION_OBSERVABLE = "autoObserv"
    #Will be called when an Automation is gained manually, and will be called every 5 seconds with the current level counts
    TIME_OBSERVABLE = "timeObserv"
    #Will be called every 5 seconds
    OTHER_OBSERVABLE = "otherObserv"
    #Probably will not be used. For any other observable not specific enough to fit in a single catagory
    #But in that case, it will most likely get it's own observable.
  
class ObservableCallType(StrEnum):
    #What to call on
    GAINED = "gained"
    TIME = "time"
    ALL = "all"
    OTHER = "other"
    
class ObservableCheckType(StrEnum):
    #AMOUNT = "amount"
    TYPE = "type"

'''
Bootleg implementation of the obeserver model.
There will be a list of observers: List[tuple(function, string, string, (string, string))]. The function is the function to call, the string is which event to
call the function on, the third string is what type of event to call on, and the fourth item is a tuple containing a check type, and the second string is what to check for.

Observables and their documentation are defined in the class above.
'''

observers = []

def newObserver(function_, what: Observable, callType: ObservableCallType, checkType: ObservableCheckType | None = None, check: str | None = None) -> None:
    print(f"new observer for {what} when {callType} occurs")
    allowedCallTypes = ["gained", "time", "all", "other"]
    allowedEvents = [
    "itemObserv",
    "acheObserv",
    "autoObserv",
    "timeObserv",
    "otherObserv"
    ]
    
    if not what in allowedEvents:
        raise TypeError("Incorrect type for what to call on, it should be a Enum from Observable")
    if not callType in allowedCallTypes:
        raise TypeError("Incorrect type for callType. Use the ObservableCallType enum.")
    if not checkType == "amount" and not checkType == None:
        raise TypeError("Incorrect type for checkType, it should use the ObservableCheckType enum")
    if not check == str and not check == None:
        raise TypeError("Check should be a str")
    
    observers.append([function_, what, callType, (checkType, check)])
    
    
def callEvent(what: Observable, callType: ObservableCallType, information: Union[str, tuple, int]):
    """
    Function to call an event
    """
    print("Calling event " + what)
    
    allowedEvents = [
    "itemObserv",
    "acheObserv",
    "autoObserv",
    "timeObserv",
    "otherObserv"
    ]
    
    allowedCallTypes = ["gained", "time", "all", "other"]
    
    if not callType in allowedCallTypes:
        raise TypeError("Incorrect type for callType. Use the ObservableCallType enum.")
    if not what in allowedEvents:
        raise TypeError("Incorrect type for what to call, it should be a enum from Observable")
    
    
    for item in observers:
        if item[1] == what:
            if item[2] == callType:
                if item[3][0] == ObservableCheckType.TYPE:
                    if information == item[3][1]:
                        item[0](information) #if there is a check and the check is sucsessful
                else:
                    item[0](information) #if there is no check
    