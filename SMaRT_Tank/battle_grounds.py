# This is the first python file here, just here to test things.

#old graph __init__, just incase if I have to revive it
    def __init__(self, master, graph_width, graph_height, ucl, lcl, row, column):
        self.master = master
        self.graph_width = graph_width
        self.graph_height = graph_height
        self.ucl = ucl
        self.lcl = lcl
        self.row = row
        self.column = column
        plt.Figure.__init__(self, figsize=(graph_width, graph_height), dpi=100)
        self.figure_axes = self.add_subplot()
        self.canvas = FigureCanvasTkAgg(self, self.master)