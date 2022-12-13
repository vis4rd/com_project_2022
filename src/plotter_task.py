import time
from threading import Lock

from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from . import Task


class PlotterTask(Task):
    def __init__(self, ax: Axes, graph: FigureCanvasTkAgg) -> None:
        super().__init__()
        self.ax: Axes = ax
        self.graph: FigureCanvasTkAgg = graph
        self.input_text: str = ""
        self.lock: Lock = Lock()

    def func(self) -> None:
        self.ax.cla()
        self.ax.grid()
        with self.lock:
            local_input_text: str = self.input_text

        if local_input_text:
            print(f"plotter_task.func: {local_input_text=}")
            self.data.append(int(local_input_text))
            with self.lock:
                self.input_text = ""
            self.iter += 1
        else:
            time.sleep(0.2)

            self.ax.plot(range(0, len(self.data)), self.data, marker="o", color="orange")
            self.graph.draw()

    def prepare(self) -> None:
        self.iter: int = 0
        self.data: list[int] = []

    def set_input_text(self, text: str) -> None:
        with self.lock:
            self.input_text = text
            print(f"set: {self.input_text=}")
