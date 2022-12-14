import sys

import serial


class Device:
    _device: serial.Serial

    def __init__(self) -> None:
        try:
            self._device = serial.Serial(port="COM3", baudrate=9600, timeout=2)
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

    def __del__(self) -> None:
        self._device.close()

    def send_command(self, command: str) -> str:
        self._device.write(command.encode())

        return self._device.readline().decode()
