from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from . import CustomThread


class PlotterThread(CustomThread):
    def __init__(
        self,
        ax: Axes,
        graph: FigureCanvasTkAgg,
        *args,
        **kwargs,
    ) -> None:
        CustomThread.__init__(self, *args, **kwargs)
        self.ax: Axes = ax
        self.graph: FigureCanvasTkAgg = graph
        self.input_text: str = ""
        self.iter: int = 0
        self.plot_points: list[int] = []

    def debug_iter(self):
        iter = 0
        while True:
            yield iter
            iter += 1

    def run(self) -> None:
        while not self.events["terminate_all"].is_set():
            gen = self.debug_iter()
            self.events["has_draw_data"].wait()  # wait for the drawing data

            new_plot_point: int = (
                int(self.data["draw_data"]) if self.data["draw_data"] is not None else int("0")
            )

            self.data["draw_data"] = None
            self.events["has_draw_data"].clear()

            self.ax.cla()
            self.ax.grid()

            self.plot_points.append(new_plot_point)
            self.input_text = ""
            self.iter += 1

            self.ax.plot(
                range(0, len(self.plot_points)),
                self.plot_points,
                marker="o",
                color="orange",
            )
            if not self.events["terminate_all"].is_set():
                self.graph.draw()
