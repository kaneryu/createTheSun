import time

def getTimeSec() -> float:
    return time.time()

def getTimeMs() -> float:
    return time.time() * 1000

def getTimeSinceTimestampMs(timestamp: float) -> float:
    return getTimeMs() - timestamp

def getTimeSinceTimestampSec(timestamp: float) -> float:
    return getTimeSec() - timestamp
