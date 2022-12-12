import time

from . import Device, PlotterTask, Task


class ArduinoTask(Task):
    def __init__(
        self,
        device: Device,
        starting_angle: int,
        ending_angle: int,
        plot_task: PlotterTask,
    ) -> None:
        super().__init__()
        self.device: Device = device
        self.starting_angle: int
        self.ending_angle: int
        self.current_angle: int
        self.plot_task: PlotterTask = plot_task

        self.setter(starting_angle, ending_angle)

    def func(self) -> None:
        if (self.current_angle >= 0) and (self.current_angle <= self.ending_angle):
            self.device.send_command(f"rotate {self.angle_step}")
            result = self.device.send_command("measure")
            print(f"arduino_task.func: {result=}")
            self.plot_task.set_input_text(result[10:])
            self.current_angle += 1
        else:
            # print("sleep")
            time.sleep(0.2)

    def prepare(self) -> None:
        self.current_angle = self.starting_angle
        self.angle_step = ((self.ending_angle - self.starting_angle) > 0) * 2 - 1

        self.device.send_command(f"rotate {self.starting_angle}")

    def setter(self, starting_angle: int, ending_angle: int) -> None:
        self.starting_angle = starting_angle % 360
        self.ending_angle = ending_angle % 360
        self.current_angle = starting_angle
