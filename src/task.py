from abc import abstractmethod
from typing import final


class Task:
    def __init__(self) -> None:
        self._keep_alive: bool = True

    @property
    def keep_alive(self) -> bool:
        return self._keep_alive

    @keep_alive.setter
    def keep_alive(self, value: bool) -> None:
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

        print("Thread killed")
