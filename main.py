import random
import sys
import threading
import time
import tkinter as tk
from abc import abstractmethod
from unittest.mock import Mock

import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pytest import MonkeyPatch

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


class Device:
    _device: serial.Serial

    def __init__(self) -> None:
        try:
            self._device = serial.Serial(port="COM4", baudrate=9600, timeout=2)
        except serial.SerialException as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        else:
            device_good: bool = self._device.is_open
            print(
                f"device name: '{self._device.name}', port open: {'yes' if device_good else 'no'}"
            )

            if not device_good:
                raise RuntimeError("Device port could not be opened")

            self._device.readline()
            # send_command(device, "measure")
            # send_command(device, "rotate 10")

    def __del__(self):
        self._device.close()

    def send_command(self, command: str) -> str:
        self._device.write(command.encode())

        return self._device.readline().decode()


class Simulator:
    monkeypatch = MonkeyPatch()
    simulate_delay: bool = False

    def __init__(self):
        self._mock_serial()
        self._mock_device()

    def _mock_serial(self):
        self.mock_serial = Mock(serial.Serial)
        self.mock_serial.is_open = True
        self.mock_serial.name = "Serial Simulator"

        self.mock_serial.call = Mock(serial.Serial)
        self.mock_serial.call.return_value = self.mock_serial
        self.monkeypatch.setattr("serial.Serial", self.mock_serial.call)

    def _mock_device(self):
        def simulator(command: str) -> str:
            def random_delay() -> int:
                return random.randint(1, 4)

            def random_distance() -> int:
                return random.randint(0, 5000)

            if self.simulate_delay:
                time.sleep(random_delay())

            match command.split():
                case ["measure", *_]:
                    return f"distance: {random_distance()}"
                case ["rotate", *_]:
                    return "Rotating..."
                case ["speed", *_] as args:
                    return f"New Speed = {args[1]}"
                case _:
                    return ""

        self.mock_send_command = Mock()
        self.mock_send_command.side_effect = simulator
        self.monkeypatch.setattr(Device, "send_command", self.mock_send_command)

    def _readline_simulator(self):
        return b"simulated response"


class Task:
    def __init__(self) -> None:
        self._keep_alive: bool = True

    @property
    def keep_alive(self):
        return self._keep_alive

    @keep_alive.setter
    def keep_alive(self, value: bool):
        self._keep_alive = value

    @abstractmethod
    def func(self):
        ...

    def prepare(self):
        pass

    def run(self):
        self.prepare()
        while self._keep_alive:
            self.func()

        print("Thread killed")


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


class Button(tk.Button):
    def __init__(self, master: tk.Misc, entry: tk.Entry, device: Device) -> None:
        super().__init__(master, text="Send", command=self.button_command)
        self.entry = entry
        self.device = device

    def _entry_delete_callback(self) -> None:
        self.entry.delete(0, "end")

    def _device_send_command_callback(self, entry_text: str) -> None:
        print(self.device.send_command(entry_text))

    def button_command(self) -> None:
        entry_text: str = self.entry.get()
        if entry_text:
            self._device_send_command_callback(entry_text)

        self._entry_delete_callback()


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

    def gui_handler(task: Task):
        # continue_plotting = not continue_plotting
        threading.Thread(target=task.run).start()

    # send_button = tk.Button(frame, text="Send command", command=lambda: gui_handler(task))
    send_button = tk.Button(frame, text="Send command", command=lambda: gui_handler(task))
    send_button.grid(row=0, column=2)

    def on_close_callback(task: Task) -> None:
        task.keep_alive = False
        print("bajo jajo")
        time.sleep(0.5)
        root.destroy()  # comment this to have fun

    root.protocol("WM_DELETE_WINDOW", lambda: on_close_callback(task))
    root.mainloop()


if __name__ == "__main__":
    main()
