import tkinter as tk
import tkinter as ttk
import game



def purchase(object):
  if object == "quarks":
    game.gameDict["quarks"] = game.gameDict["quarks"] + 1
  else:
    cost = game.evaluateCost(object)
    
    if cost >= game.gameDict[game.gameDict[object + "Cost"][0]]:
      game.gameDict[object] = game.gameDict[object] + 1
      game.gameDict[game.gameDict[object + "Cost"][0]] = game.gameDict[game.gameDict[object + "Cost"][0]] - cost
  print(game.gameDict[object])
       
class creationObject(ttk.Frame):
  def __init__(self, parent, object : str, name : str, *args, **kwargs):
    ttk.Frame.__init__(self, parent, *args, **kwargs)
    
    ttk.Frame.config(self, relief = "ridge", borderwidth = 2)
    #f"You have {game.gameDict[object]} {name}{game.plural(object)}
    self.desc = ttk.Label(self, textvariable = tk.StringVar(value = game.descDict[object + ",String"][0] + game.descDict[object + ",String"][1] + game.descDict[object + ",String"][2]))
    self.desc.pack(side = "left")
    
    if object == "quarks":
      cost = "free"
      self.purchaseButton = ttk.Button(self, text = f"Purchase 1 quark for free", command = lambda: purchase(object))
      self.purchaseButton.pack()
    else:
      print(game.evaluateCost(object))
      cost = game.evaluateCost(object)
      self.purchaseButton = ttk.Button(self, text = f"Purchase 1 {name} for {cost} {game.gameDict[object + "Cost"][0][:-1]}{game.plural(object)}", command = lambda: purchase(object))
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