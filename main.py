import threading
import time
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src import Device, PlotterTask, Simulator, Task

# def command(device, rotate_steps: int) -> list[int]:
#     results: list[int] = []
#     for i in range(rotate_steps):
#         send_command(device, "rotate 1")
#         results.append(int(send_command(device, "measure")[11:]))
#     return results


# def command2(device, starting_angle: int, ending_angle: int):
#     starting_angle = starting_angle % 360
#     print(starting_angle)
#     ending_angle = ending_angle % 360
#     print(ending_angle)
#     angle_step = ((ending_angle - starting_angle) > 0) * 2 - 1
#     send_command(device, f"rotate {starting_angle}")
#     plt.axis([starting_angle, ending_angle, 0, 5])
#     for i in range(starting_angle, ending_angle):
#         print(
#             f"i ={i}, starting_angle={starting_angle}, "
#             f"ending_angle={ending_angle}, angle_step={angle_step}"
#         )
#         send_command(device, f"rotate {angle_step}")
#         result = send_command(device, "measure")
#         plt.scatter(i, int(result[11:]) / 100)
#         plt.pause(0.05)
#     plt.show()


# TODO:
# * zapis wynikow do pliku
# * wprowadzanie komend do arduino przez gui input
# * ulozenie osi wykresu
# * rysowanie odleglosci w czasie na wykresie (w czasie rzeczywistym)
# * dodac command2() do Device


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

    task = PlotterTask(ax, graph)

    def reset_task(task: PlotterTask) -> None:
        # Kill previous thread and wait for it to join (does not work for some reason)
        task.keep_alive = False
        task.set_input_text("")
        time.sleep(1)

        task.keep_alive = True

    def gui_handler(task: PlotterTask) -> None:
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
            case ["multimeasure", *_]:
                print("ohno")
                reset_task(task)
                threading.Thread(target=task.run).start()
            case _:
                pass

    send_button = tk.Button(frame, text="Send command", command=lambda: gui_handler(task))
    send_button.grid(row=0, column=2)

    def on_close_callback(task: Task) -> None:
        task.keep_alive = False
        print("bajo jajo")
        time.sleep(1)
        root.destroy()  # comment this to have fun

    root.protocol("WM_DELETE_WINDOW", lambda: on_close_callback(task))
    root.mainloop()


if __name__ == "__main__":
    main()
