import click
from enum import Enum
import requests
import http

API_DOMAIN = "http://localhost:5000/"
FILE_TYPES = Enum("FILE_TYPES",["logtextfile", "binaryfile", "bufferfile" ])

main = click.Group(help="File system api")


@main.command('read', help='read specified component of system')
@click.option('-n', '--name',  'component_name', type=click.STRING, help='Name of the component')
def read_component(component_name: str):
    if component_name == None:
        response = requests.get(f"{API_DOMAIN}directory")
        click.echo(response.text)
    else:
        response = requests.get(f"{API_DOMAIN}/file/{component_name}")
        if response.status_code == http.HTTPStatus.BAD_REQUEST and response.text == 'No such file':
            click.echo('There is no file with such name!')
        elif response.status_code == http.HTTPStatus.OK:
            click.echo(response.text)
        else:
            click.echo('Failed to read!')

    
@main.command('create-dir', help='create directory into file system')
@click.option('-n', '--name', 'component_name', required=True, type=click.STRING, help='Name of the component')
@click.option('-c', '--capacity', 'capacity', default=10, type=click.INT, help='Amount of inners may be stored')
def create_directory(component_name: str, capacity: int):
    response = requests.post(f'{API_DOMAIN}directory/{component_name}', json={"volume": f"{capacity}"})
    if response.status_code == http.HTTPStatus.NO_CONTENT:
        click.echo("Directory is created!")
    else:
        click.echo("Failed to create directory!")


@main.command('move-dir', help='move directory into another directory')
@click.option('-f', '--from', 'fromm', required=True, type=click.STRING, help='Source directory to move')
@click.option('-t', '--to', 'to', required=True,type=click.STRING, help='Destination folder')
def movedir_from_to(fromm: str, to: str):
    response = requests.put(f'{API_DOMAIN}directory/{fromm}/{to}')
    if response.status_code == http.HTTPStatus.BAD_REQUEST:
        click.echo(f'Filed to move directory! {response.text}')
    else:
        click.echo('Directory moved successfully!')



@main.command('move-file', help='move file into another directory')
@click.option('-f', '--from', 'fromm', required=True, type=click.STRING, help='Source file to move')
@click.option('-t', '--to', 'to', required=True,type=click.STRING, help='Destination folder')
def movefile_from_to(fromm: str, to: str):
    response = requests.put(f'{API_DOMAIN}file/{fromm}/{to}')
    if response.status_code == http.HTTPStatus.NO_CONTENT:
        click.echo('File moved successfully!')
    elif response.status_code == http.HTTPStatus.NOT_FOUND or response.status_code == http.HTTPStatus.BAD_REQUEST:
        click.echo(f'Failed to move file! {response.text}')



@main.command('remove-dir')
@click.option('-n', '--name',  'name', required=True, type=click.STRING)
def remove_dir(name: str):
    response = requests.delete(f'{API_DOMAIN}directory/{name}')
    if response.status_code == http.HTTPStatus.NO_CONTENT:
        click.echo('File removed successfully!')
    else:
        click.echo(f'Failed to remove directory! {response.text}')


@main.command('remove-file')
@click.option('-n', '--name',  'name', required=True, type=click.STRING)
def remove_file(name: str):
    response = requests.delete(f'{API_DOMAIN}file/{name}')
    if response.status_code == http.HTTPStatus.NO_CONTENT:
        click.echo('File removed successfully!')
    elif response.status_code == http.HTTPStatus.BAD_REQUEST:
        click.echo('There is no such file!')
    else:
        click.echo('Failed to remove!')


@main.command('writeto')
@click.option('-n', '--name',  'file_name', required=True, type=click.STRING)
@click.option('-l', '--newline',  'new_line', required=True, type=click.STRING)
def writeto(file_name: str, new_line: str):
    response = requests.patch(f'{API_DOMAIN}file/{file_name}', json={"new_line_value": "first value"})
    if response.status_code == http.HTTPStatus.NO_CONTENT:
        click.echo('Record has been written!')
    elif response.status_code == http.HTTPStatus.NOT_FOUND:
        click.echo('File not found!')
    elif response.status_code == http.HTTPStatus.BAD_REQUEST:
        click.echo('Invalid action!')
    else:
        click.echo('Failed to write!')



@main.command('create-file')
@click.option('-n', '--name',  'name', required=True, type=click.STRING)
@click.option('-t', '--type',  'file_type', required=True, type=click.STRING)
@click.option('-c', '--capacity',  'capacity', required=True, type=click.INT)
def create_file(name: str, file_type: str, capacity: int):
    response = requests.post(f'{API_DOMAIN}file/{file_type}/{name}', json={"volume": f"{capacity}"})
    if response.status_code == http.HTTPStatus.OK:
        click.echo(f'File of type ({file_type}) created successfully!')
    elif response.status_code == http.HTTPStatus.BAD_REQUEST:
        click.echo(f'Creation is failed! {response.text}')
    else:
        click.echo('Failed to create!')



if __name__ == "__main__":
    exit(main())