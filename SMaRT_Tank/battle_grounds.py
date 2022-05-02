# This is the first python file here, just here to test things.

from tkinter import *

# root = Tk()
# rvar = IntVar(root)
# rvar.set(1)

def change(idx):
    print(idx)

def show_menu(root):
    # global rvar
    try:
        show_menu.rvar
    except:
        show_menu.rvar = IntVar(root)
        show_menu.rvar.set(1)

    menubar = Menu(root)
    settings = Menu(menubar, tearoff=0)
    settings.add_command(label='some 1')
    settings.add_command(label='some 2')
    mDebug = Menu(settings, tearoff=0)

    mDebug.add_radiobutton(label='first', var = show_menu.rvar, value = 0, command=lambda idx=0: change(idx))
    mDebug.add_radiobutton(label='second', var = show_menu.rvar, value = 1, command=lambda idx=1: change(idx))
    mDebug.add_radiobutton(label='third', var = show_menu.rvar, value = 2, command=lambda idx=2: change(idx))

    settings.add_cascade(label='radio options', menu = mDebug)
    settings.add_separator()
    settings.add_command(label='quit')
    menubar.add_cascade(label="Menu", menu=settings)
    root.config(menu=menubar)

root = Tk()
show_menu(root)

root.mainloop()