import re

VERSIONREGEX = re.compile(r"^v?\d+.\d+.\d+(-a\d*|-b\d*)?$")

class Version:
    def __init__(self, versionStr: str):
        """Version constructor

        Args:
            versionStr (str): A version string such as "1.2.3", or "v1.2.3" or "1.2.3b1" etc.
        
        ### Versions System
        
        Versions have 3 main parts, separated by ".": Major.Minor.Patch
        
        You can also have appendages, such as, "1.1.1-b#", "1.1.1-a#", "1.1.1-b", etc. (where # is the number)
        
        Release types are Beta, Alpha, and Release (Release is the default, and  is only specified by a lack of beta or alpha in the version string)
        """
        if not VERSIONREGEX.match(versionStr):
            raise ValueError("Invalid version string")
        
        # Remove the "v" if it exists
        if versionStr[0] == "v":
            versionStr = versionStr[1:]
        
        # Split the version string into its parts
        parts = versionStr.split(".")
        self.major = int(parts[0])
        self.minor = int(parts[1])
        if not "-" in parts[2]:
            self.patch = int(parts[2])
        else:
            self.patch = int(parts[2].split("-")[0])
        
        # Check for appendages
        if "-" in parts[2]:
            appendage = parts[2].split("-")
            self.patch = int(appendage[0])
            self.appendage = appendage[1]
            self.releaseType = "b" if self.appendage[0] == "b" else "a"
            self.releaseTypeNumber = int(appendage[1][1:]) if appendage[1][1:] else 0
        else:
            self.appendage = None
            self.releaseType = "r"
            self.releaseTypeNumber = 0
        
        self.setWarningStr({})
        
    def __str__(self):
        """Converts the version object to a string"""
        return f"Version {self.major}.{self.minor}.{self.patch}" + (f"-{self.appendage}" if self.appendage else "")

    def __eq__(self, other):
        """Checks if two versions are equal"""
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch and self.appendage == other.appendage
    
    def __lt__(self, other):
        """Checks if the version is less than another version"""
        if self.major < other.major:
            return True
        elif self.major == other.major:
            if self.minor < other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch < other.patch:
                    return True
                elif self.patch == other.patch:
                    if self.appendage and not other.appendage:
                        return True
                    elif self.appendage and other.appendage:
                        if self.appendage < other.appendage:
                            return True
                        elif self.appendage == other.appendage:
                            if self.releaseTypeNumber < other.releaseTypeNumber:
                                return True
        return False
    
    def __gt__(self, other):
        """Checks if the version is greater than another version"""
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch > other.patch:
                    return True
                elif self.patch == other.patch:
                    if not self.appendage and other.appendage:
                        return True
                    elif self.appendage and other.appendage:
                        if self.appendage > other.appendage:
                            return True
                        elif self.appendage == other.appendage:
                            if self.releaseTypeNumber > other.releaseTypeNumber:
                                return True
        return False
    
    def __le__(self, other):
        """Checks if the version is less than or equal to another version"""
        return self == other or self < other
    
    def __ge__(self, other):
        """Checks if the version is greater than or equal to another version"""
        return self == other or self > other
    
    def __ne__(self, other):
        """Checks if the version is not equal to another version"""
        return not self == other
    
    def __repr__(self):
        """Returns a string representation of the object"""
        return f"{str(self).split(' ')[1]}"
    
    def __hash__(self):
        """Returns a hash of the object"""
        return hash(str(self))

    def toDict(self):
        """Converts the version object to a dictionary"""
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "appendage": self.appendage
        }
    
    @staticmethod
    def fromDict(d: dict):
        """Converts a dictionary to a version object"""
        return Version(f"{d['major']}.{d['minor']}.{d['patch']}{f'-{d['appendage']}' if d['appendage'] else ''}")
    
    def toTuple(self):
        """Converts the version object to a tuple"""
        return (self.major, self.minor, self.patch, self.appendage)
    
    @staticmethod
    def fromTuple(t: tuple):
        """Converts a tuple to a version object"""
        return Version(f"{t[0]}.{t[1]}.{t[2]}{f'-{t[3]}' if t[3] else ''}")
    
    def toList(self):
        """Converts the version object to a list"""
        return [self.major, self.minor, self.patch, self.appendage]
    
    @staticmethod
    def fromList(l: list):
        """Converts a list to a version object"""
        return Version(f"{l[0]}.{l[1]}.{l[2]}{f'-{l[3]}' if l[3] else ''}")
    
    def getWarning(self, other) -> str:
        if self > other:
            return self.tooNewWarning.replace("%CURRENT", repr(self)).replace("%OLD", repr(other))
        elif self < other:
            return self.tooOldWarning.replace("%CURRENT", repr(self)).replace("%OLD", repr(other))
        elif self.releaseType != other.releaseType:
            return self.diffReleaseWarning.replace("%CURRENT", repr(self)).replace("%OLD", repr(other))
        else:
            return ""
        
    def setWarningStr(self, strs: dict) -> None:
        """Sets warning strings for the version object

        Args:
            strs (dict): The warning strings to set, must contain "tooNew", "tooOld", and "diffRelease" keys

        Raises:
            ValueError: If the warning strings are invalid
        
        Use the following placeholders in the warning strings:
        
        %CURRENT - The current version
        
        %OLD - The version being compared to
        """
        
        if not strs:
            strs = {}
        
        
        if strs == {}:
            self.tooNewWarning = "Version %CURRENT is newer than %OLD"
            self.tooOldWarning = "Version %CURRENT is older than %OLD"
            self.diffReleaseWarning = "Version %CURRENT is a different release type than %OLD"
        else:
            try:
                self.tooNewWarning = strs["tooNew"]
                self.tooOldWarning = strs["tooOld"]
                self.diffReleaseWarning = strs["diffRelease"]
            except KeyError:
                raise ValueError("Invalid warning strings, must contain 'tooNew', 'tooOld', and 'diffRelease' keys")
