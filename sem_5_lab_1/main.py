from typing import List


class InvalidOperation(Exception):
    pass


class Component:
    def __init__(self, name: str, volume: int):
        self.__name = name
        self.__volume = volume  # component size
        self.__content = []

    @property
    def name(self):
        return self.__name

    @property
    def max_size(self):
        return self.__volume

    def push_record(self, record: str):
        raise NotImplementedError()

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    def display(self, ident: int):
        fileExtension: str = ''
        type_of_file = type(self)
        if type_of_file == type(LogTextFile):
            fileExtension += '.txt'
        elif type_of_file == type(BinaryFile):
            fileExtension += '.buff'
        elif type_of_file == type(BufferFile):
            fileExtension += '.bin'

        return f"{' ' * ident}{self.name}{fileExtension} {self.max_size}\n"

    def read_file(self):
        buff: str = f'{self.name}\n'
        for x in self.content:
            buff += f"{x}\n"
        return buff


class BinaryFile(Component):
    def __init__(self, name: str, volume: int):
        Component.__init__(self, name, volume)
        self.content = ['fake content', 'you can look', "but you can't touch"]

    def push_record(self, record: str):
        raise InvalidOperation


class LogTextFile(Component):
    def push_record(self, record: str):
        self.content.append(record)


class BufferFile(Component):
    def push_record(self, record: str):
        if len(self.content) + 1 <= self.max_size:
            self.content.append(record)
        else:
            raise InvalidOperation

    def read_file(self):
        return f'{self.content.pop(0)}\n'


class Composite(Component):
    def __init__(self, name: str, volume: int):
        super().__init__(name, volume)
        self.__components: [Component] = []

    @property
    def children(self):
        return self.__components

    def push_record(self, record: str):
        raise Exception

    def create(self, component: Component):
        if len(self.__components) + 1 <= self.max_size:
            self.__components.append(component)
        else:
            raise InvalidOperation

    def remove(self, component: Component):
        self.__components.remove(component)

    @staticmethod
    def move(to_move_component: Component, destination_composite, root):
        root.remove(to_move_component)
        destination_composite.create(to_move_component)

    def read_file(self):
        raise Exception

    def display(self, ident: int):
        buff: str = f"{' ' * ident}{self.name}>\n"
        ident += 3
        for c in self.__components:
            buff += c.display(ident)
        return buff