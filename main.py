import random
import sys
import time
import tkinter as tk
from unittest.mock import Mock

import serial
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


class Plot(tk.Frame):
    def __init__(self):
        super().__init__(background="black", padx=1, pady=1)

        self.canvas = tk.Canvas(self, bg="white")
        self.draw_point(50, 50)
        self.canvas.grid(row=0, column=0)

    def draw_point(self, x: float, y: float, size: float = 6):
        self.canvas.create_oval(
            x - size / 2.0,
            y - size / 2.0,
            x + size / 2.0,
            y + size / 2.0,
            fill="black",
        )


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


class Button(tk.Button):
    def __init__(self, master: tk.Misc, entry: tk.Entry, device: Device):
        super().__init__(master, text="Send", command=self.button_command)
        self.entry = entry
        self.device = device

    def _entry_delete_callback(self):
        self.entry.delete(0, "end")

    def _device_send_command_callback(self, entry_text: str):
        print(self.device.send_command(entry_text))

    def button_command(self):
        entry_text = self.entry.get()
        if entry_text:
            self._device_send_command_callback(entry_text)

        self._entry_delete_callback()


GLOBAL_VALUE: int = 0  # set this in _device_send_command_callback and send to plot


def main() -> None:
    simulator = Simulator()  # comment this line when working on actual arduino
    simulator.simulate_delay = True

    device = Device()

    root = tk.Tk()
    root.geometry("800x400+300+300")

    plot = Plot()
    plot.grid(row=1, column=0)
    frame = tk.Frame()  # container for inputs
    frame.grid(row=0, column=0)

    l1 = tk.Label(frame, text="Command")
    l1.grid(row=0, column=0)

    ent1 = tk.Entry(frame)
    ent1.grid(row=0, column=1)

    send_button = Button(frame, ent1, device)
    send_button.grid(row=0, column=2)

    root.mainloop()


if __name__ == "__main__":
    main()
