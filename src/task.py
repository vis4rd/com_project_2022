from abc import abstractmethod


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
