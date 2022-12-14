from . import CustomThread, Device


class ArduinoThread(CustomThread):
    def __init__(
        self,
        device: Device,
        starting_angle: int,
        ending_angle: int,
        *args,
        **kwargs,
    ) -> None:
        CustomThread.__init__(self, *args, **kwargs)
        self.device: Device = device
        self.starting_angle: int = starting_angle % 360
        self.ending_angle: int = ending_angle % 360
        self.current_angle: int = self.starting_angle

        self.angle_step = ((self.ending_angle - self.starting_angle) > 0) * 2 - 1

        self.device.send_command(f"rotate {self.starting_angle}")

    def run(self) -> None:
        while (self.current_angle >= 0) and (self.current_angle <= self.ending_angle):
            if self.events["terminate_all"].is_set():
                break

            self.device.send_command(f"rotate {self.angle_step}")
            result = self.device.send_command("measure")
            print(f"arduino_task.func: {result=}")
            self.current_angle += 1

            self.data["draw_data"] = result[10:]
            self.events["has_draw_data"].set()

    def set_angles(self, starting_angle: int, ending_angle: int):
        self.starting_angle = starting_angle
        self.ending_angle = ending_angle

        self.current_angle = self.starting_angle
