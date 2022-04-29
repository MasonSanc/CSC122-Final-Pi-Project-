# This is the first python file here, just here to test things.

#
from multiprocessing.sharedctypes import Value
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("400x400")

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()

GRAPH_TYPES = [("Live", var1), ("Hour", var2), ("Day", var3), ("Week", var4)]

menu_button = ttk.Menubutton(root, text="Select Graph Type")
menu = Menu(menu_button, tearoff=False)

for type, var in GRAPH_TYPES:
    menu.add_radiobutton(label=type, variable=var)

menu_button["menu"] = menu

menu_button.grid(row=0, column=1, sticky="news")

root.mainloop()