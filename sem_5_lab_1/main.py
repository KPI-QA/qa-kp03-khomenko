from typing import List


class Component:
    def __init__(self, name: str):
        self.__name__ = name
        self.__max_size = -1

    def is_composite(self) -> bool:
        return False

    def push_record(self, record: str):
        raise NotImplementedError()

    def read_file(self, name: str):
        raise NotImplementedError()


class BinaryFile(Component):
    pass


class LogTextFile(Component):
    pass


class BufferFile(Component):
    pass


class Composite:
    def __init__(self):
        self._components: List[Component] = []

    def create(self):
        pass

    def remove(self):
        pass

    def move(self, source: Component, destination: Component):
        pass


