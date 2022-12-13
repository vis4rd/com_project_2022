import threading
import time
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src import ArduinoTask, Device, PlotterTask, Simulator, Task

# TODO:
# * zapis wynikow do pliku
# * ulozenie osi wykresu


def main() -> None:
    simulator = Simulator()  # comment this line when working on actual arduino
    simulator.simulate_delay = True

    device = Device()

    root = tk.Tk()
    root.geometry("800x400+300+300")

    frame = tk.Frame()  # container for inputs
    frame.grid(row=0, column=0)

    l1 = tk.Label(frame, text="Command")
    l1.grid(row=0, column=0)

    ent1 = tk.Entry(frame)
    ent1.grid(row=0, column=1)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().grid(row=1, column=0)

    plotter_task = PlotterTask(ax, graph)
    arduino_task = ArduinoTask(device, 0, 0, plotter_task)

    plotter_thread = threading.Thread(name="PlotterThread", target=plotter_task.run)
    arduino_thread = threading.Thread(name="ArduinoThread", target=arduino_task.run)

    def reset_task(task: Task, thread: threading.Thread) -> None:
        # Kill previous thread and wait for it to join (does not work for some reason)
        if not thread.is_alive():
            return

        task.keep_alive = False
        thread.join()
        task.keep_alive = True

    def gui_handler() -> None:
        input_text: str = ent1.get()
        ent1.delete(0, "end")
        if not input_text:
            return

        match input_text.split():
            case ["measure", *_]:
                print(device.send_command(input_text))
            case ["rotate", *_]:
                print(device.send_command(input_text))
            case ["speed", *_] as args:
                print(device.send_command(input_text))
            case ["multimeasure", *_] as args:  # multimeasure 20 30
                reset_task(arduino_task, arduino_thread)
                arduino_task.setter(int(args[1]), int(args[2]))

                reset_task(plotter_task, plotter_thread)
                plotter_task.set_input_text("")

                arduino_thread.start()
                plotter_thread.start()
            case _:
                pass

    send_button = tk.Button(frame, text="Send command", command=gui_handler)
    send_button.grid(row=0, column=2)

    def on_close_callback(task: Task) -> None:
        task.keep_alive = False
        arduino_task.keep_alive = False
        print("bajo jajo")
        plotter_thread.join()
        arduino_thread.join()
        root.destroy()  # comment this to have fun

    root.protocol("WM_DELETE_WINDOW", lambda: on_close_callback(plotter_task))
    root.mainloop()


if __name__ == "__main__":
    main()
