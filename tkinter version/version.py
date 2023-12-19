import json

with open("project.version", "r") as file:
    temp = file.read()
    tempDict = json.loads(temp)

version = tempDict["v"]
build = tempDict["b"]
type = tempDict["t"]
#Github Copilot said : self.author = "Nathan Klapstein"
contributors = tempDict["c"]

build += 1
print(f"Version {version}, Build {build}, {type}")

file = open("project.version", 'w')
file.write(json.dumps({"v" : version, "b": build, "t" : type, "c" : contributors}))
file.close()        

BLANK_SAVE = {"noSave" : True, "gameVersion" : str(version) + "." + str(build)}