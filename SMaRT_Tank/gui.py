#

'''
TODO

Make a way to plot data
Make the graphs look nice
Figure out what should DPI be

Make a way to store data in a text file
Be able to read from said text file, and then plot the data
'''

from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Main_GUI(Tk):

    SALINITY_GRAPH_DATA = {
        "xlabel": 'Time',
        "ylabel": 'Salinity (ppm)',
        "title": "Salinity vs. Time",
        "ucl": 500,
        "lcl": 200
    }

    TEMPERATURE_GRAPH_DATA = {
        "xlabel": 'Time',
        "ylabel": "Temperature",
        "title": "Temperature vs. Time",
        "ucl": 500,
        "lcl": 200
    }

    PH_GRAPH_DATA = {
        "xlabel": 'Time',
        "ylabel": "PH",
        "title": "PH vs. Time",
        "ucl": 500,
        "lcl": 200
    }

    DEBUG = True



    def __init__(self):
        Tk.__init__(self)
        self.attributes('-fullscreen', True)
        self.screen_width_in = self.winfo_screenmmwidth() / 25.4
        self.screen_height_in = self.winfo_screenmmheight() / 25.4
        # see if we need to calculate dpi
        if self.DEBUG:
            print(f"The screen is {self.screen_width_in}in x {self.screen_height_in}in")
            print(type(self.screen_height_in))

    def create_graph_frame(self):
        # Data in here is just to see how things work/look
        gw1 = Graph_frame(self.master, self.screen_width_in, self.screen_height_in * (4/5),'Time','Salinity (ppm)' ,"Salinity vs. Time" , 500, 200)

    def run(self):
        self.create_graph_frame()
        self.mainloop()

class Graph_frame(Frame):

    GRAPH_TYPES = ["Live", "Hour", "Day", "Week"]

    def __init__(self, master, graph_width, graph_height, xlabel, ylabel, title, ucl, lcl):
        Frame.__init__(self, master)
        self.grid(row=0, column=0)

        self.back_button = ttk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=0, column=0, sticky="sw")
        
        self.create_graph_type_menu()

        self.graph = self.create_graph(self, graph_width, graph_height, xlabel, ylabel, title, ucl, lcl)

    def create_graph_type_menu(self):
        self.menu_button = ttk.Menubutton(self, text="Select Graph Type")
        self.menu = Menu(self.menu_button, tearoff=False)

        for type in self.GRAPH_TYPES:
            self.menu.add_checkbutton(label=type)

        self.menu_button["menu"] = self.menu

        self.menu_button.grid(row=0, column=1, sticky="ne")

    def create_graph(self, master, graph_width, graph_height, xlabel, ylabel, title, ucl, lcl):

        graph = Graph(master, graph_width, graph_height)
        graph.graph_setup(xlabel, ylabel, title, ucl, lcl)
        return graph

    def back(self):
        quit()


class Graph(plt.Figure):

    DEBUG = True
    
    def __init__(self, master, graph_width, graph_height):
        plt.Figure.__init__(self, figsize=(graph_width, graph_height), dpi=100)
        self.figure_axes = self.add_subplot()
        self.canvas = FigureCanvasTkAgg(self, master)

    def graph_setup(self, xlabel, ylabel, title, ucl, lcl):
        # Add graph labels
        self.figure_axes.set_xlabel(xlabel)
        self.figure_axes.set_ylabel(ylabel)
        self.figure_axes.set_title(title)

        # Create UCL and LCL, fake/bad data is being used till I find workaround
        self.figure_axes.plot([0,1], [ucl,ucl], color="red", label="UCL")
        self.figure_axes.plot([0,1], [lcl,lcl], color="blue", label="LCL")
        self.figure_axes.legend()

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="ews")

    


app = Main_GUI()
app.run()
