#

'''
TODO

Make a way to plot data
Make the graphs look nice
Figure out what should DPI be

Make a way to store data in a text file
Be able to read from said text file, and then plot the data
'''

from  tkinter  import  *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Main_GUI(Tk):
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

    def create_graph(self):
        # Data in here is just to see how things work/look
        g1 = Graph(self, self.screen_width_in / 2, self.screen_height_in / 2)
        g2 = Graph(self, self.screen_width_in / 2, self.screen_height_in / 2)
        g1.graph_setup(500, 100, 0, 0)
        g2.graph_setup(500, 100, 1, 1)

    def run(self):
        self.create_graph()
        self.mainloop()


class Graph(plt.Figure):

    DEBUG = True
    
    def __init__(self, master, graph_width, graph_height):
        plt.Figure.__init__(self, figsize=(graph_width, graph_height), dpi=100)
        self.figure_axes = self.add_subplot()
        self.canvas = FigureCanvasTkAgg(self, master)

    def graph_setup(self, ucl, lcl, row, column):
        self.figure_axes.set_xlabel('x label')
        self.figure_axes.set_ylabel('y label')
        self.figure_axes.set_title("Test Plot")

        # Create UCL and LCL, fake/bad data is being used till I find workaround
        self.figure_axes.plot([0,1], [ucl,ucl], color="red", label="UCL")
        self.figure_axes.plot([0,1], [lcl,lcl], color="blue", label="LCL")
        self.figure_axes.legend()

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=row, column=column, sticky="news")


    


app = Main_GUI()
app.run()
