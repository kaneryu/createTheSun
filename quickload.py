import enum
import os

class QuickloadType(enum.IntEnum):
    TEXT = 1
    BYTES = 2

class ErrorTolerance(enum.StrEnum):
    NONE = "none"
    FILE_NOT_FOUND = "fnf"
    
def quickload(file: str, type: QuickloadType, errorTolerance: ErrorTolerance | None = ErrorTolerance.NONE) -> str | bytes:
    """Return the contents of a file

    Args:
        file (str): The file to read
        type (QuickloadType): What type to return
        errorTolerance (ErrorTolerance): Amount of error tolerance. Defaults to None

    Returns:
        str | bytes: The contents of the file. Will return "fileNotFound" if the file is not found and errorTolerance is set to FILE_NOT_FOUND
    """
    
    if not os.path.exists(file):
        if errorTolerance == ErrorTolerance.FILE_NOT_FOUND:
            return "fileNotFound"
        elif errorTolerance == ErrorTolerance.NONE:
            raise FileNotFoundError(f"File {file} not found.")
    
    with open(file, 'r' if type == QuickloadType.TEXT else 'rb') as f:
        return f.read()
    
    