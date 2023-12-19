
logLevel = 0
logLevels = ["debug", "info", "warning", "error"]
# 0 = debug
# 1 = info
# 2 = warning
# 3 = error
specialLogs = []
# updateLoopInfo

def log(message: str, level: int = 0, specialType: str = "") -> None:
    """
    Logs a message to the console.

    Args:
        message (str): The message to log.
        level (int): The level of the message. Defaults to 0.
    """
    if specialType != "":
        if specialType in specialLogs:
            print(message)
            return 1
        else:
            return -1
    
    if level >= logLevel:
        print(f"{logLevels[level]}: {message}")
    else:
        return -1
        
    
        

