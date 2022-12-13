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
            print(f"{next(gen)=}")
            self.events["has_draw_data"].wait()  # wait for the drawing data
            print(f"{next(gen)=}")

            new_plot_point: int = (
                int(self.data["draw_data"]) if self.data["draw_data"] is not None else int("0")
            )
            print(f"{next(gen)=}")
            self.plot_points.append(new_plot_point)
            print(f"{next(gen)=}")

            self.data["draw_data"] = None
            print(f"{next(gen)=}")
            self.events["has_draw_data"].clear()
            print(f"{next(gen)=}")

            self.ax.cla()
            print(f"{next(gen)=}")
            self.ax.grid()
            print(f"{next(gen)=}")

            self.plot_points.append(new_plot_point)
            print(f"{next(gen)=}")
            self.input_text = ""
            print(f"{next(gen)=}")
            self.iter += 1
            print(f"{next(gen)=}")

            self.ax.plot(
                range(0, len(self.plot_points)),
                self.plot_points,
                marker="o",
                color="orange",
            )
            print(f"{next(gen)=}")
            if not self.events["terminate_all"].is_set():
                self.graph.draw()
            print(f"{next(gen)=}")

    # def prepare(self) -> None:
    #     self.iter: int = 0
    #     self.drawing_data: list[int] = []

    # def set_input_text(self, text: str) -> None:
    #     with self.lock:
    #         self.input_text = text
    #         print(f"set: {self.input_text=}")
