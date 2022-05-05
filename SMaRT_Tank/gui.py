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

from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import ImageTk, Image
import data_processing as dp

import os
import psutil

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

        self.data = dp.Data()

        # update all arrays
        self.update_arrays((1,1,1))
        plt.ion()

    def update_arrays(self, update_tuple):

        update_live, update_hourly, update_daily = update_tuple

        if update_live:
            self.live_time = self.data.second_data['unixTime'].replace({np.nan: 'NaT'}).to_numpy('datetime64[s]')
            self.live_temp = self.data.second_data['temp'].replace({np.nan: None}).to_numpy()
            self.live_salinity = self.data.second_data['sal'].replace({np.nan: None}).to_numpy()
            self.live_pH = self.data.second_data['pH'].replace({np.nan: None}).to_numpy()

        if update_hourly:
            self.hourly_time = self.data.hourly_data['unixTime'].replace({np.nan: 'NaT'}).to_numpy('datetime64[s]')
            self.hourly_temp = self.data.hourly_data['temp'].replace({np.nan: None}).to_numpy()
            self.hourly_salinity = self.data.hourly_data['sal'].replace({np.nan: None}).to_numpy()
            self.hourly_pH = self.data.hourly_data['pH'].replace({np.nan: None}).to_numpy() 

        if update_daily :
            self.daily_time = self.data.daily_data['unixTime'].replace({np.nan: 'NaT'}).to_numpy('datetime64[s]')
            self.daily_temp = self.data.daily_data['temp'].replace({np.nan: None}).to_numpy()
            self.daily_salinity = self.data.daily_data['sal'].replace({np.nan: None}).to_numpy()
            self.daily_pH = self.data.daily_data['pH'].replace({np.nan: None}).to_numpy()

        self.temp_data = [(self.live_temp, self.live_time), (self.hourly_temp, self.hourly_time), (self.daily_temp, self.daily_time)]
        self.salinity_data = [(self.live_salinity, self.live_time), (self.hourly_salinity, self.hourly_time), (self.daily_salinity, self.daily_time)]
        self.pH_data = [(self.live_pH, self.live_time), (self.hourly_pH, self.hourly_time), (self.daily_pH, self.daily_time)]

    def create_gui(self):
        self.main_menu_frame = Main_menu_frame(self, self.swap_to_graph_frame)

        self.salinity_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.SALINITY_GRAPH_DATA, self.salinity_data)
        self.temperature_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.TEMPERATURE_GRAPH_DATA, self.temp_data)
        self.ph_graph_frame = Graph_frame(self, self.graph_sizing, self.swap_to_main_menu_frame, self.PH_GRAPH_DATA, self.pH_data)

        # Hide the graphs from screen
        self.salinity_graph_frame.forget()
        self.temperature_graph_frame.forget()
        self.ph_graph_frame.forget()

        # set current frame to main menu
        self.current_frame = self.main_menu_frame


    def swap_to_main_menu_frame(self, graph):
        if graph == self.SALINITY_GRAPH_DATA["measurement"]:
            self.salinity_graph_frame.forget()
            
        elif graph == self.TEMPERATURE_GRAPH_DATA["measurement"]:
            self.temperature_graph_frame.forget()

        elif graph == self.PH_GRAPH_DATA["measurement"]:
            self.ph_graph_frame.forget()

        self.current_frame = self.main_menu_frame
        self.main_menu_frame.pack(expand=1, fill="both")

    def swap_to_graph_frame(self, graph):
        self.main_menu_frame.forget()

        if graph == self.SALINITY_GRAPH_DATA["measurement"]:
            self.current_frame = self.salinity_graph_frame
            current_type = self.current_frame.menu_var.get()
            if current_type == self.current_frame.GRAPH_TYPES[0]:
                self.current_frame.graph.plot_data(self.current_frame.live_data, self.current_frame.GRAPH_TYPES[0])
            if current_type == self.current_frame.GRAPH_TYPES[1]:
                self.current_frame.graph.plot_data(self.current_frame.hourly_data, self.current_frame.GRAPH_TYPES[1])
            if current_type == self.current_frame.GRAPH_TYPES[2]:
                self.current_frame.graph.plot_data(self.current_frame.daily_data, self.current_frame.GRAPH_TYPES[2])
            return self.salinity_graph_frame.pack(expand=1, fill="both")
            
        if graph == self.TEMPERATURE_GRAPH_DATA["measurement"]:
            self.current_frame = self.temperature_graph_frame
            current_type = self.current_frame.menu_var.get()
            if current_type == self.current_frame.GRAPH_TYPES[0]:
                self.current_frame.graph.plot_data(self.current_frame.live_data, self.current_frame.GRAPH_TYPES[0])
            if current_type == self.current_frame.GRAPH_TYPES[1]:
                self.current_frame.graph.plot_data(self.current_frame.hourly_data, self.current_frame.GRAPH_TYPES[1])
            if current_type == self.current_frame.GRAPH_TYPES[2]:
                self.current_frame.graph.plot_data(self.current_frame.daily_data, self.current_frame.GRAPH_TYPES[2])
            return self.temperature_graph_frame.pack(expand=1, fill="both")

        if graph == self.PH_GRAPH_DATA["measurement"]:
            self.current_frame = self.ph_graph_frame
            current_type = self.current_frame.menu_var.get()
            if current_type == self.current_frame.GRAPH_TYPES[0]:
                self.current_frame.graph.plot_data(self.current_frame.live_data, self.current_frame.GRAPH_TYPES[0])
            if current_type == self.current_frame.GRAPH_TYPES[1]:
                self.current_frame.graph.plot_data(self.current_frame.hourly_data, self.current_frame.GRAPH_TYPES[1])
            if current_type == self.current_frame.GRAPH_TYPES[2]:
                self.current_frame.graph.plot_data(self.current_frame.daily_data, self.current_frame.GRAPH_TYPES[2])
            return self.ph_graph_frame.pack(expand=1, fill="both")

    def update(self, update_tuple):
            
        self.update_arrays(update_tuple)
        self.salinity_graph_frame.update_data(self.salinity_data)
        self.temperature_graph_frame.update_data(self.temp_data)
        self.ph_graph_frame.update_data(self.pH_data)

        if self.current_frame == self.main_menu_frame:
                return

        current_type = self.current_frame.menu_var.get()
        if current_type == self.current_frame.GRAPH_TYPES[0]:
            self.current_frame.graph.plot_data(self.current_frame.live_data, self.current_frame.GRAPH_TYPES[0])
        if current_type == self.current_frame.GRAPH_TYPES[1]:
            self.current_frame.graph.plot_data(self.current_frame.hourly_data, self.current_frame.GRAPH_TYPES[1])
        if current_type == self.current_frame.GRAPH_TYPES[2]:
            self.current_frame.graph.plot_data(self.current_frame.daily_data, self.current_frame.GRAPH_TYPES[2])


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

        button = ttk.Button(self, text=text, image=image, padding=0, command=lambda: command(text))
        button.image = image
        button.grid(row=row, column=column, sticky="news")
        return button

    def exit(self, _):
        quit()
            
            

class Graph_frame(ttk.Frame):

    BACK_BUTTON_FONT_SIZE = 35
    GRAPH_TYPE_MENU_FONT_SIZE = 25
    WIDGET_FONT = 'Helvetica'

    GRAPH_TYPES = ["Live", "Hour", "Day"]

    def __init__(self, master, graph_sizing ,command, graph_parameters, data):

        # set data
        self.live_data = data[0]
        self.hourly_data = data[1]
        self.daily_data = data[2]

        Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        self.create_widget_config()

        self.graph = Graph(self, graph_sizing, graph_parameters)

        self.back_button = ttk.Button(self, text="Back", command=lambda: command(graph_parameters["measurement"]))
        self.back_button.grid(row=0, column=0, sticky="news")
        
        self.create_graph_type_menu()


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

    def swap_type(self, type, data):
        if type == self.GRAPH_TYPES[0]:
             self.graph.plot_data(data, type)
             return

        if type == self.GRAPH_TYPES[1]:
            self.graph.plot_data(data, type)
            return

        if type == self.GRAPH_TYPES[2]:
            self.graph.plot_data(data, type)
            return

    def create_graph_type_menu(self):
        self.menu_button = ttk.Menubutton(self, text="Select Graph Type")
        self.menu = Menu(self.menu_button, tearoff=False)
        self.menu_button["menu"] = self.menu
        self.menu_var = StringVar()

        for type in self.GRAPH_TYPES:
            
            if type == self.GRAPH_TYPES[0]:
                self.menu.add_radiobutton(label=type, variable=self.menu_var, value=type, command=lambda type=type: self.swap_type(type, self.live_data))
                continue

            if type == self.GRAPH_TYPES[1]:
                self.menu.add_radiobutton(label=type, variable=self.menu_var, value=type, command=lambda type=type: self.swap_type(type, self.hourly_data))
                continue

            if type == self.GRAPH_TYPES[2]:
                self.menu.add_radiobutton(label=type, variable=self.menu_var, value=type, command=lambda type=type: self.swap_type(type, self.daily_data))
                continue

        self.menu.invoke(0)
        self.menu_var.set("Live")

        self.menu_button.grid(row=0, column=1, sticky="news")

    def update_data(self, data):
        self.live_data = data[0]
        self.hourly_data = data[1]
        self.daily_data = data[2]

class Graph(plt.Figure):

    DEBUG = True
    
    def __init__(self, master, graph_sizing, graph_parameters):
        plt.Figure.__init__(self, figsize=(graph_sizing["graph_width_in"], graph_sizing["graph_height_in"]), dpi=100)
        self.figure_axes = self.add_subplot()
        self.canvas = FigureCanvasTkAgg(self, master)
        self.graph_parameters = graph_parameters

        self.graph_setup(graph_parameters)

    def graph_setup(self, graph_parameters):
        # Add graph labels
        self.figure_axes.set_xlabel(self.graph_parameters["xlabel"])
        self.figure_axes.set_ylabel(self.graph_parameters["ylabel"])
        self.figure_axes.set_title(self.graph_parameters["title"])

        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="news")

    def plot_data(self, data, label):
        y_data, x_data = data 

        # clear canvas
        self.figure_axes.clear()

        # create UCL and LCL
        self.figure_axes.axhline(y=self.graph_parameters["ucl"], color='r', label="UCL")
        self.figure_axes.axhline(y=self.graph_parameters["lcl"], color='b', label="LCL")

        # plot new data
        self.figure_axes.plot(x_data, y_data, label=label)
        self.figure_axes.set_xlim(x_data[1], x_data[-1])

        # add legend
        self.figure_axes.legend()

        # update canvas
        self.canvas.draw()
