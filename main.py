import tkinter as tk
from threading import Event, Thread

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src import ArduinoThread, Device, PlotterThread, Simulator

# TODO:
# * zapis wynikow do pliku
# * ulozenie osi wykresu


def main() -> None:
    # simulator = Simulator()  # comment this line when working on actual arduino
    # simulator.simulate_delay = True

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

    events: dict[str, Event] = {
        "terminate_all": Event(),
        "has_draw_data": Event(),
    }

    data: dict[str, str | None] = {
        "draw_data": None,
    }

    plotter_thread = PlotterThread(ax, graph, events=events, data=data)
    arduino_thread = ArduinoThread(
        device, starting_angle=0, ending_angle=0, events=events, data=data
    )

    def reset_thread(thread: Thread) -> None:
        # Kill previous thread and wait for it to join (does not work for some reason)
        if not thread.is_alive():
            return

        print(f"Waiting for thread {thread.name} to join...")
        thread.join()
        print(f"Thread {thread.name} joined.")

    def reset_all_threads() -> None:
        events["terminate_all"].set()

        reset_thread(arduino_thread)
        reset_thread(plotter_thread)

        events["terminate_all"].clear()
        events["has_draw_data"].clear()
        data["draw_data"] = None

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
                reset_all_threads()
                arduino_thread.set_angles(int(args[1]), int((args[2])))

                arduino_thread.start()
                plotter_thread.start()
            case _:
                pass

    send_button = tk.Button(frame, text="Send command", command=gui_handler)
    send_button.grid(row=0, column=2)

    def on_close_callback() -> None:
        events["terminate_all"].set()
        plotter_thread.join()
        arduino_thread.join()
        root.destroy()  # comment this to have fun

    root.protocol("WM_DELETE_WINDOW", lambda: on_close_callback())
    root.mainloop()


if __name__ == "__main__":
    main()
