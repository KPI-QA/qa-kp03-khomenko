import http
import logging

from flask import Flask, request, make_response
from main import Composite, Component, LogTextFile, BinaryFile, BufferFile, InvalidOperation
import logging

LOGGER = logging.getLogger()

app = Flask(__name__)
root = Composite("root", 1000)


# lists all inner objects
@app.get('/directory')
def get_dir():
    return root.display(5), 200


# create directory
# 204
@app.post('/directory/<dir_name>')
def post_dir(dir_name):
    root.create(Composite(dir_name, int(request.json.get('volume'))))
    return "", http.HTTPStatus.NO_CONTENT


# move file or directory to subdirectory
# 204 or 404
@app.put('/directory/<from_dir_name>/<to_dir_name>')
def put_dir(from_dir_name, to_dir_name):
    try:
        to_move_component = list(filter(lambda c: c.name == from_dir_name and isinstance(c, Composite), root.children))[
            0]
        to_instance = list(filter(lambda c: c.name == to_dir_name, root.children))[0]
    except IndexError:
        return 'Either source or destination not found', http.HTTPStatus.BAD_REQUEST

    try:
        Composite.move(to_move_component, to_instance, root)
    except InvalidOperation:
        return 'The operation cannot be applied', http.HTTPStatus.BAD_REQUEST

    return '', http.HTTPStatus.NO_CONTENT


# remove directory
# 204 or 400
@app.delete('/directory/<dir_name>')
def delete_dir(dir_name):
    found_dirs = list(filter(lambda c: c.name == dir_name and isinstance(c, Composite), root.children))

    if len(found_dirs) == 0:
        return 'No such directory', http.HTTPStatus.BAD_REQUEST

    root.remove(found_dirs[0])
    return "", http.HTTPStatus.NO_CONTENT


"""File endpoints"""


# readfile
@app.get('/file/<file_name>')
def get_file(file_name):
    found_files = list(filter(lambda c: c.name == file_name and not isinstance(c, Composite), root.children))
    LOGGER.info(found_files)
    if len(found_files) == 0:
        return 'No such file', http.HTTPStatus.BAD_REQUEST

    return found_files[0].read_file(), http.HTTPStatus.OK


# create file
# body: volume
@app.post('/file/<file_type>/<file_name>')
def post_file(file_type, file_name):
    if file_type == 'binaryfile':
        root.create(BinaryFile(file_name, 0))
    elif file_type == 'logtextfile':
        root.create(LogTextFile(file_name, int(request.json.get('volume'))))
    elif file_type == 'bufferfile':
        root.create(BufferFile(file_name, int(request.json.get('volume'))))
    else:
        return 'No such file format', http.HTTPStatus.BAD_REQUEST

    return '', http.HTTPStatus.OK


# remove file
@app.delete('/file/<file_name>')
def delete_file(file_name):
    LOGGER.info(root.display(5))
    found_files = list(filter(lambda c: c.name == file_name and not isinstance(c, Composite), root.children))
    if len(found_files) == 0:
        return '', http.HTTPStatus.BAD_REQUEST

    root.remove(found_files[0])
    return '', http.HTTPStatus.NO_CONTENT


# move file
@app.put('/file/<file_name>/<destination_dir_name>')
def put_file(file_name, destination_dir_name):
    found_files = list(filter(lambda c: c.name == file_name and not isinstance(c, Composite), root.children))
    found_dirs = list(filter(lambda c: c.name == destination_dir_name and isinstance(c, Composite), root.children))

    if len(found_files) == 0:
        return 'no such file', http.HTTPStatus.NOT_FOUND
    source_file: Component = found_files[0]

    if len(found_dirs) == 0:
        return 'no such directory', http.HTTPStatus.NOT_FOUND
    destination_dir: Composite = found_dirs[0]

    try:
        Composite.move(source_file, destination_dir, root)
    except InvalidOperation:
        return 'The operation cannot be applied', http.HTTPStatus.BAD_REQUEST

    return '', http.HTTPStatus.NO_CONTENT


# append a lineS
# body: new_line_value
@app.patch('/file/<file_name>')
def patch_file(file_name):
    found_files = list(filter(lambda c: c.name == file_name and not isinstance(c, Composite), root.children))
    if len(found_files) == 0:
        return '', http.HTTPStatus.NOT_FOUND

    file_to_patch: Component = found_files[0]

    try:
        file_to_patch.push_record(str(request.json.get('new_line_value')))
    except InvalidOperation:
        return '', http.HTTPStatus.BAD_REQUEST

    return '', http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
