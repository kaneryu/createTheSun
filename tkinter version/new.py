from tkinter import *
from tkinter import ttk

class Notebook:

    def __init__(self,title):
        self.root = Tk()
        self.root.title(title)
        self.notebook = ttk.Notebook(self.root)

    def add_tab(self,title,text):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame,text=title)
        label = ttk.Label(frame,text=text)
        label.grid(column=1,row=1)
        self.notebook.pack()

    def run(self):
        self.root.mainloop()

nb = Notebook('Example')
nb.add_tab('Frame One','This is on Frame One')
nb.add_tab('Frame Two','This is on Frame Two')
nb.run()
