import tkinter as tk
import tkinter as ttk
import itemGameLogic



def purchase(object):
  if object == "quarks":
    itemGameLogic.gameDict["quarks"] = itemGameLogic.gameDict["quarks"] + 1
  else:
    cost = itemGameLogic.evaluateCost(object)
    
    if cost >= itemGameLogic.gameDict[itemGameLogic.gameDict[object + "Cost"][0]]:
      itemGameLogic.gameDict[object] = itemGameLogic.gameDict[object] + 1
      itemGameLogic.gameDict[itemGameLogic.gameDict[object + "Cost"][0]] = itemGameLogic.gameDict[itemGameLogic.gameDict[object + "Cost"][0]] - cost
  print(itemGameLogic.gameDict[object])
       
class creationObject(ttk.Frame):
  def __init__(self, parent, object : str, name : str, *args, **kwargs):
    ttk.Frame.__init__(self, parent, *args, **kwargs)
    
    ttk.Frame.config(self, relief = "ridge", borderwidth = 2)
    #f"You have {game.gameDict[object]} {name}{game.plural(object)}
    self.desc = ttk.Label(self, textvariable = tk.StringVar(value = itemGameLogic.descDict[object + ",String"][0] + itemGameLogic.descDict[object + ",String"][1] + itemGameLogic.descDict[object + ",String"][2]))
    self.desc.pack(side = "left")
    
    if object == "quarks":
      cost = "free"
      self.purchaseButton = ttk.Button(self, text = f"Purchase 1 quark for free", command = lambda: purchase(object))
      self.purchaseButton.pack()
    else:
      print(itemGameLogic.evaluateCost(object))
      cost = itemGameLogic.evaluateCost(object)
      self.purchaseButton = ttk.Button(self, text = f"Purchase 1 {name} for {cost} {itemGameLogic.gameDict[object + "Cost"][0][:-1]}{itemGameLogic.plural(object)}", command = lambda: purchase(object))
      self.purchaseButton.pack()




class mainTab(ttk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    shell_frame = ttk.Frame(parent)
    
    #label = ttk.Label(shell_frame, text=f"You have {game.gameDict["quarks"]} quarks")
    #label.pack()
    creationList = [
      ["quarks", "Quark"],
      ["protons", "Proton"]
    ]
    

    
    self.purchaseList = []
    
    for i in creationList:
      self.purchaseList.append(creationObject(shell_frame, i[0], i[1]))
      self.purchaseList[len(self.purchaseList) - 1].pack(side = "top")
    
    shell_frame.pack(fill="both", expand = True, pady = 25)