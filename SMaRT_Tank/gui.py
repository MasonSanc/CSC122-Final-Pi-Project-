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
        self.screen_width_pixle = self.winfo_screenwidth()
        self.screen_height_pixle = self.winfo_screenheight()     

        # see if we need to calculate dpi
        if self.DEBUG:
            print(f"The screen is {self.screen_width_in}in x {self.screen_height_in}in")
            print(type(self.screen_height_in))

    def create_main_menu_frame(self):
        main_menu = Main_menu_frame(self, self.screen_width_pixle, self.screen_height_pixle)

    def create_graph_frame(self):
        # Data in here is just to see how things work/look
        gw1 = Graph_frame(self, self.screen_width_in, self.screen_height_in * (4/5),'Time','Salinity (ppm)' ,"Salinity vs. Time" , 500, 200)

    def create_gui(self):
        self.main_menu_frame = Main_menu_frame(self, self.screen_width_pixle, self.screen_height_pixle, self.swap_to_graph_frame)
        self.salinity_graph_frame = Graph_frame(self, self.screen_width_in, self.screen_height_in * (4/5), self.swap_to_main_menu_frame, 'Time','Salinity' ,"Salinity vs. Time" , 500, 200)
        self.temperature_graph_frame = Graph_frame(self, self.screen_width_in, self.screen_height_in * (4/5), self.swap_to_main_menu_frame,'Time','Temperature' ,"Temperature vs. Time" , 500, 200)
        self.ph_graph_frame = Graph_frame(self, self.screen_width_in, self.screen_height_in * (4/5), self.swap_to_main_menu_frame, 'Time','Ph' ,"PH vs. Time" , 500, 200)

        self.salinity_graph_frame.forget()
        self.temperature_graph_frame.forget()
        self.ph_graph_frame.forget()

    def swap_to_main_menu_frame(self, graph):
        if graph == "Salinity":
            self.salinity_graph_frame.forget()
            
        elif graph == "Temperature":
            self.temperature_graph_frame.forget()

        elif graph == "Ph":
            self.ph_graph_frame.forget()

        self.main_menu_frame.pack(expand=1, fill="both")

    def swap_to_graph_frame(self, graph):
        self.main_menu_frame.forget()

        if graph == "Salinity":
            return self.salinity_graph_frame.pack(expand=1, fill="both")
            
        if graph == "Temperature":
            return self.temperature_graph_frame.pack(expand=1, fill="both")

        if graph == "Ph":
            return self.ph_graph_frame.pack(expand=1, fill="both")

    def run(self):
        #self.create_main_menu_frame()
        #self.create_graph_frame()
        self.create_gui()
        self.mainloop()

class Main_menu_frame(ttk.Frame):
    MAIN_MENU_BUTTON_FONT_SIZE = 100
    WIDGET_FONT = 'Helvetica'

    def __init__(self, master, screen_width, screen_height, command):
        Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        # Remove if I do not reuse
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.create_widget_config() 

        self.other_button = self.create_menu_button("Other", self.exit, 0, 0)
        self.salinity_button = self.create_menu_button("Salinity", command, 0, 1)
        self.temperature_button = self.create_menu_button("Temperature", command, 1, 0)
        self.ph_button = self.create_menu_button("Ph", command, 1, 1)


    def create_widget_config(self):
        self.button_style = ttk.Style()
        self.button_style.configure('TButton', font=(self.WIDGET_FONT, self.MAIN_MENU_BUTTON_FONT_SIZE), foreground='blue')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


    def create_menu_button(self, text, command, row, column):
        button = ttk.Button(self, text=text, command=lambda: command(text))
        button.grid(row=row, column=column, sticky="news")
        return button

    def exit(self, _):
        quit()
            
            

class Graph_frame(ttk.Frame):

    BACK_BUTTON_FONT_SIZE = 35
    GRAPH_TYPE_MENU_FONT_SIZE = 25
    WIDGET_FONT = 'Helvetica'

    GRAPH_TYPES = ["Live                                                                                                                                                                                                                                                                                                                                    ", "Hour", "Day", "Week"]

    def __init__(self, master, graph_width, graph_height, command, xlabel, ylabel, title, ucl, lcl):
        Frame.__init__(self, master)
        self.pack(expand=1, fill="both")

        self.create_widget_config()

        self.back_button = ttk.Button(self, text="Back", command=lambda: command(ylabel))
        self.back_button.grid(row=0, column=0, sticky="news")
        
        self.create_graph_type_menu()

        self.graph = self.create_graph(self, graph_width, graph_height, xlabel, ylabel, title, ucl, lcl)

    # To change the look of the widgets and add weights to the columns and rows
    def create_widget_config(self):
        self.button_style = ttk.Style()
        self.button_style.configure('TButton', font=(self.WIDGET_FONT, self.BACK_BUTTON_FONT_SIZE), foreground='blue')

        self.menu_button_style = ttk.Style()
        self.menu_button_style.configure('TMenubutton', font=(self.WIDGET_FONT, self.GRAPH_TYPE_MENU_FONT_SIZE))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)


    def create_graph_type_menu(self):
        self.menu_button = ttk.Menubutton(self, text="Select Graph Type")
        self.menu = Menu(self.menu_button, tearoff=False)

        for type in self.GRAPH_TYPES:
            self.menu.add_checkbutton(label=type)

        self.menu_button["menu"] = self.menu

        self.menu_button.grid(row=0, column=1, sticky="news")


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
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="news")

    


app = Main_GUI()
app.run()
