from abc import abstractmethod
from threading import Lock, current_thread
from typing import final


class Task:
    def __init__(self) -> None:
        self._keep_alive: bool = True
        self._keep_alive_lock: Lock = Lock()

    @property
    def keep_alive(self) -> bool:
        with self._keep_alive_lock:
            return self._keep_alive

    @keep_alive.setter
    def keep_alive(self, value: bool) -> None:
        with self._keep_alive_lock:
            self._keep_alive = value

    @abstractmethod
    def func(self) -> None:
        ...

    def prepare(self) -> None:
        pass

    @final
    def run(self) -> None:
        self.prepare()
        while self._keep_alive:
            self.func()

        print(f"Thread {current_thread().getName()} killed")
