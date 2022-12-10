import random
import time
from unittest.mock import Mock

import serial
from pytest import MonkeyPatch

from . import Device


class Simulator:
    monkeypatch = MonkeyPatch()
    simulate_delay: bool = False

    def __init__(self) -> None:
        self._mock_serial()
        self._mock_device()

    def _mock_serial(self) -> None:
        self.mock_serial = Mock(serial.Serial)
        self.mock_serial.is_open = True
        self.mock_serial.name = "Serial Simulator"

        self.mock_serial.call = Mock(serial.Serial)
        self.mock_serial.call.return_value = self.mock_serial
        self.monkeypatch.setattr("serial.Serial", self.mock_serial.call)

    def _mock_device(self) -> None:
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

    def _readline_simulator(self) -> bytes:
        return b"simulated response"
