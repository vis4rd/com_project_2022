import time

from . import Device, Task


class PlotterTask(Task):
    def __init__(self, ax, graph) -> None:
        super().__init__()
        self.ax = ax
        self.graph = graph

    def func(self) -> None:
        # input text should be a string with number
        # if not self.input_text: # uncomment when plotting measured values
        #     time.sleep(0.5)  # check for new input values every 0.5 second
        #     return

        self.ax.cla()
        self.ax.grid()
        if self.iter < 10:  # change this condition in future
            self.data.append(self.iter)  # add input number to the graph (not done)
            self.input_text = ""  # clear input for the next iteration
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()
            time.sleep(0.1)
            self.iter += 1
        else:
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()

    def prepare(self) -> None:
        self.iter: int = 0
        self.data: list[int] = []

    def set_input_text(self, text: str) -> None:
        self.input_text = text
