import time

def getTimeSec() -> float:
    return time.time()

def getTimeMs() -> float:
    return time.time() * 1000

def getTimeSinceTimestampMs(timestamp: float) -> float:
    return getTimeMs() - timestamp

def getTimeSinceTimestampSec(timestamp: float) -> float:
    return getTimeSec() - timestamp

runEveryMsCheck_ = {}

def checkIntervalElapsed(timeToWait: int, id: str, debug: bool = False) -> bool:
    if id not in runEveryMsCheck_:
        runEveryMsCheck_[id] = 0
    
    if debug: print("runEveryMsCheck_:", runEveryMsCheck_)
    if debug: print("id:", id)
    if getTimeSinceTimestampMs(runEveryMsCheck_[id]) >= timeToWait:
        runEveryMsCheck_[id] = getTimeMs()
        if debug: print("success, id:", id)
        return True

    if debug: print("not yet, id:", id)
    return False