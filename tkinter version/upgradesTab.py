import tkinter as tk
import tkinter as ttk

class upgradesTab(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        
        self.container = tk.Frame(self.master)
        label = tk.Label(self.container, text="Main Tab")
        
        