import time

from . import Task


class PlotterTask(Task):
    def __init__(self, ax, graph) -> None:
        super().__init__()
        self.ax = ax
        self.graph = graph
        self.input_text: str = ""

    def func(self) -> None:
        self.ax.cla()
        self.ax.grid()
        if self.input_text:
            print(f"plotter_task.func: {self.input_text=}")
            self.data.append(int(self.input_text))
            self.input_text = ""
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()
            self.iter += 1
        else:
            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()
            time.sleep(0.2)

    def prepare(self) -> None:
        self.iter: int = 0
        self.data: list[int] = []

    def set_input_text(self, text: str) -> None:
        self.input_text = text
        print(f"set: {self.input_text=}")
