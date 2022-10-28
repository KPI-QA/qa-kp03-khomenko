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

    @property
    def name(self):
        return self.__name__

    @property
    def max_size(self):
        return self.__max_size


class BinaryFile(Component):
    pass


class LogTextFile(Component):
    pass


class BufferFile(Component):
    pass


class Composite:
    def __init__(self):
        self.__components: List[Component] = []
        self.__outputIdent = 3

    def create(self):
        pass

    def remove(self):
        pass

    def move(self, source: Component, destination: Component):
        pass

    def get_children(self):
        return self.__components
