import time

from . import Task


class PlotterTask(Task):
    def __init__(self, ax, graph) -> None:
        super().__init__()
        self.ax = ax
        self.graph = graph

    def func(self):
        self.ax.cla()
        self.ax.grid()
        if self.iter < 10:
            self.data.append(self.iter)
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()
            time.sleep(1)
            self.iter += 1
        else:
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()

    def prepare(self):
        self.iter = 0
        self.data = []
