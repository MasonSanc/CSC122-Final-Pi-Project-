#

'''
TODO

Make a way to plot data

Figure out if we need a custom DPI / what should DPI be

Make a way to store data in a text file

Be able to read from said text file, and then plot the data

There are two paths to take with vcontroling the frames.
1. Make all frames on init and swap between them in runtime 
    Longer start up, fast swap between frames, do not know how it will work with auto updating graphs
2. Make just menu fame on init and create/destory frames on demand
    Faster start up, slow swap between frames, less demmanding for updating graphs
'''

from ast import AsyncFunctionDef
from tkinter import *
from tkinter import ttk
from turtle import bgcolor
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import ImageTk, Image

class Main_GUI(Tk):

    SALINITY_GRAPH_DATA = {
        "measurement": "Salinity",
        "xlabel": 'Time',
        "ylabel": 'Salinity (ppt)',
        "title": "Salinity vs. Time",
        "ucl": 36.0,
        "lcl": 34.0
    }

    TEMPERATURE_GRAPH_DATA = {
        "measurement": "Temperature",
        "xlabel": 'Time',
        "ylabel": "Temperature (F)",
        "title": "Temperature vs. Time",
        "ucl": 77,
        "lcl": 75
    }

    PH_GRAPH_DATA = {
        "measurement": "pH",
        "xlabel": 'Time',
        "ylabel": "pH",
        "title": "pH vs. Time",
        "ucl": 8.4,
        "lcl": 8.0
    }

    DEBUG = True


    def __init__(self):
        Tk.__init__(self)
        self.attributes('-fullscreen', True)

        self.graph_sizing = {
            "graph_width_in" : (self.winfo_screenmmwidth() / 25.4),
            "graph_height_in" : (self.winfo_screenmmheight() / 25.4) * 0.8
        }   

    def create_gui(self):
        self.main_menu_frame = Main_menu_frame(self, self.swap_to_graph_frame)

        self.salinity_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.SALINITY_GRAPH_DATA)
        self.temperature_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.TEMPERATURE_GRAPH_DATA)
        self.ph_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.PH_GRAPH_DATA)

        # Hide the graphs from screen
        self.salinity_graph_frame.forget()
        self.temperature_graph_frame.forget()
        self.ph_graph_frame.forget()

    def swap_to_main_menu_frame(self, graph):
        if graph == self.SALINITY_GRAPH_DATA["measurement"]:
            self.salinity_graph_frame.forget()
            
        elif graph == self.TEMPERATURE_GRAPH_DATA["measurement"]:
            self.temperature_graph_frame.forget()

        elif graph == self.PH_GRAPH_DATA["measurement"]:
            self.ph_graph_frame.forget()

        self.main_menu_frame.pack(expand=1, fill="both")

    def swap_to_graph_frame(self, graph):
        self.main_menu_frame.forget()

        if graph == self.SALINITY_GRAPH_DATA["measurement"]:
            return self.salinity_graph_frame.pack(expand=1, fill="both")
            
        if graph == self.TEMPERATURE_GRAPH_DATA["measurement"]:
            return self.temperature_graph_frame.pack(expand=1, fill="both")

        if graph == self.PH_GRAPH_DATA["measurement"]:
            return self.ph_graph_frame.pack(expand=1, fill="both")

    def run(self):
        self.create_gui()
        self.mainloop()

class Main_menu_frame(ttk.Frame):
    MAIN_MENU_BUTTON_FONT_SIZE = 100
    WIDGET_FONT = 'Helvetica'

    def __init__(self, master, command):
        Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        #self.background = self.set_background()

        self.create_widget_config() 

        self.other_button = self.create_menu_button("Other", self.exit, 0, 0)
        self.salinity_button = self.create_menu_button("Salinity", command, 0, 1)
        self.temperature_button = self.create_menu_button("Temperature", command, 1, 0)
        self.ph_button = self.create_menu_button("pH", command, 1, 1)
    """
    def set_background(self):
        image = None
        bg_image = Image.open('art_assets/bg.jpg').convert('RGBA')
        image = ImageTk.PhotoImage(bg_image)
        background = Label(self, image=image)
        background.place(anchor='center')
        background.image = image
        return background
    """

    def create_widget_config(self):
        self.button_style = ttk.Style()
        self.button_style.configure('TButton', font=(self.WIDGET_FONT, self.MAIN_MENU_BUTTON_FONT_SIZE), foreground='blue')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def create_menu_button(self, text, command, row, column):

        if text == "Other":
            PIL_image = Image.open('./art_assets/settings.png').convert('RGBA')
            image = ImageTk.PhotoImage(PIL_image)

        elif text == "Salinity":
            PIL_image = Image.open('./art_assets/salinity.png').convert('RGBA')
            image = ImageTk.PhotoImage(PIL_image)

        elif text == "Temperature":
            PIL_image = Image.open('./art_assets/temperature.png').convert('RGBA')
            image = ImageTk.PhotoImage(PIL_image)

        elif text == "pH":
            PIL_image = Image.open('./art_assets/ph.png').convert('RGBA')
            image = ImageTk.PhotoImage(PIL_image)

        else:
            image = None

        button = ttk.Button(self, text=text, image=image, command=lambda: command(text))
        button.image = image
        button.grid(row=row, column=column, sticky="news")
        return button

    def exit(self, _):
        quit()
            
            

class Graph_frame(ttk.Frame):

    BACK_BUTTON_FONT_SIZE = 35
    GRAPH_TYPE_MENU_FONT_SIZE = 25
    WIDGET_FONT = 'Helvetica'

    GRAPH_TYPES = ["Live", "Hour", "Day", "Week"]

    def __init__(self, master, graph_sizing ,command, graph_parameters):
        Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        self.create_widget_config()

        self.back_button = ttk.Button(self, text="Back", command=lambda: command(graph_parameters["measurement"]))
        self.back_button.grid(row=0, column=0, sticky="news")
        
        self.create_graph_type_menu()

        self.graph = Graph(self, graph_sizing, graph_parameters)

    # To change the look of the widgets and add weights to the columns and rows
    def create_widget_config(self):
        self.button_style = ttk.Style()
        self.button_style.configure('TButton', font=(self.WIDGET_FONT, self.BACK_BUTTON_FONT_SIZE), foreground='blue')

        self.menu_button_style = ttk.Style()
        self.menu_button_style.configure('TMenubutton', font=(self.WIDGET_FONT, self.GRAPH_TYPE_MENU_FONT_SIZE))

        # have the buttons take free space by giving them weight
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def create_graph_type_menu(self):
        self.menu_button = ttk.Menubutton(self, text="Select Graph Type")
        self.menu = Menu(self.menu_button, tearoff=False)
        self.menu_button["menu"] = self.menu

        for type in self.GRAPH_TYPES:
            self.menu.add_radiobutton(label=type)

        self.menu_button.grid(row=0, column=1, sticky="news")

    def back(self):
        quit()

class Graph(plt.Figure):

    DEBUG = True
    
    def __init__(self, master, graph_sizing, graph_parameters):
        plt.Figure.__init__(self, figsize=(graph_sizing["graph_width_in"], graph_sizing["graph_height_in"]), dpi=100)
        self.figure_axes = self.add_subplot()
        self.canvas = FigureCanvasTkAgg(self, master)
        
        self.graph_setup(graph_parameters)

    def graph_setup(self, graph_parameters):
        # Add graph labels
        self.figure_axes.set_xlabel(graph_parameters["xlabel"])
        self.figure_axes.set_ylabel(graph_parameters["ylabel"])
        self.figure_axes.set_title(graph_parameters["title"])

        # Create UCL and LCL, fake/bad data is being used till I find workaround
        self.figure_axes.axhline(y=graph_parameters["ucl"], color='r', label="UCL")
        self.figure_axes.axhline(y=graph_parameters["lcl"], color='b', label="LCL")
        self.figure_axes.legend()

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="news")

    

app = Main_GUI()
app.run()
