import click
from enum import Enum

API_DOMAIN = ""
FILE_TYPES = Enum("FILE_TYPES",["logtextfile", "binaryfile", "bufferfile" ])

main = click.Group(help="File system api")


@main.command('read', help='read specified component of system')
@click.option('-n', '--name',  'component_name', required=True, type=click.STRING, help='Name of the component')
def read_component(component_name: str):
    pass

@main.command('create', help='create directory into file system')
@click.option('-n', '--name', 'component_name', required=True, type=click.STRING, help='Name of the component')
@click.option('-c', '--capacity', 'capacity', default=10, type=click.INT, help='Amount of inners may be stored')
def create_directory(component_name: str, capacity: int):
    pass

@main.command('move', help='move file/directory into another directory')
@click.option('-f', '--from', required=True, type=click.STRING, help='Source component to move')
@click.option('-t', '--to', required=True,type=click.STRING, help='Destination folder')
def move_from_to():
    pass


@main.command('remove')
@click.option('-n', '--name',  'component_name', required=True, type=click.STRING)
def remove(component_name: str):
    pass


@main.command('writeto')
@click.option('-n', '--name',  'component_name', required=True, type=click.STRING)
@click.option('-l', '--newline',  'new_line', required=True, type=click.STRING)
def writeto():
    pass


@main.command('create-file')
@click.option('-n', '--name',  'component_name', required=True, type=click.STRING)
@click.option('-t', '--type',  'file_type', required=True, type=click.STRING)
def create_file(name: str, file_type: str):
    pass


if __name__ == "__main__":
    exit(main())