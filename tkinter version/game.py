import threading
import version
from sympy import sympify

BLANK_SAVE = version.BLANK_SAVE

def game():
    global running, hasEverBeenTrue, descDict, gameDict
    while running and hasEverBeenTrue:
        for i in descDict:
            list = descDict[i]
            descDict[i] = [list[0], str(gameDict[i.split(',')[0]]), list[2]]
            print(descDict[i])

#class gameVariables:
#    def __init__(self):
#        pass
#    def initalize(self, dict):
#        global gameDict
#        if dict["noSave"]:
#            
#            tempDict = BLANK_SAVE
#            
#            tempdict2 = {
#                "quarks" : 0,
#                "protons" : 0,
#                "electrons" : 0,
#                "hydrogen" : 0,
#                "stars" : 0,
#                "galaxies" : 0,
#                "superClusters" : 0,
#                
#                #Costs
#                "quarksCost" : "free", 
#                "protonsCost" : 6,
#                "hydrogenCost" : 1,
#                "starsCost" : 1e57,
#                "galaxiesCost" : 3e11,
#                "superClustersCost" : 100000,
#                
#                #Upgrades
#                "quarksPerClick" : 1,
#                "protonsPerClick" : 2,
#                "hydrogensPerClick" : 1,
#                "starsPerClick" : 1,
#                "galaxiesPerClick" : 1,
#                "superClustersPerClick" : 1,
#                
#                #Upgrade Costs
#                "quarksPerClickCost" : "pow(%currentUpgrade%, 2)"
#                }
#            self.varDict = tempDict | tempdict2
#            
#            gameDict = self.varDict
#            
#        self.varDict = dict
#        gameDict = self.varDict
        


tempDict = BLANK_SAVE

tempdict2 = {
"quarks" : 0,
"protons" : 0,
"electrons" : 0,
"hydrogen" : 0,
"stars" : 0,
"galaxies" : 0,
"superClusters" : 0,

#Costs ["what it costs", "equasion"]
"quarksCost" : "free", 
"protonsCost" : ["quarks", "* 0 + 6"],
"hydrogenCost" : ["protons", "* 0 + 1"],
"starsCost" : ["hydrogen", "* 0 + 1e57"],
"galaxiesCost" : ["stars", "* 0 + 1e11"],
"superClustersCost" : ["galaxies", "* 0 + 100000"],

#Upgrades
"quarksPerClick" : 1,
"protonsPerClick" : 1,
"hydrogensPerClick" : 1,
"starsPerClick" : 1,
"galaxiesPerClick" : 1,
"superClustersPerClick" : 1,

#Upgrade Costs [""what it costs", "equasion""]
"quarksPerClickCost" : ["quarks", "free"],
"protonsPerClickCost" : ["quarks", "* 1.5 / 50"]
}

descDict = {
"quarks,String" :  ["You have ", "0"," quarks"],
"protons,String" : ["You have ", "0"," protons"],
"hydrogen,String" :  ["You have ", "0"," hydrogen"],
"stars,String" :  ["You have ", "0"," stars"],
"galaxies,String" :  ["You have ", "0"," galaxies"],
"superClusters,String" :  ["You have ", "0"," super clusters"]
}
def evaluateCost(object):
    global gameDict
    item = gameDict[object + "Cost"]
    get =  item[0]
    needs = gameDict[get]
    
    return sympify(str(needs) + item[1])
def plural(object):
    global gameDict
    return "" if abs(gameDict[object]) == 1 else "s"
gameDict = tempDict | tempdict2

hasEverBeenTrue = False
running = False
