from flask import Flask, request
from main import Composite

app = Flask(__name__)
root = Composite("root", 1000)


# lists all inner objects
@app.get('/directory')
def get():
    pass


# create directory
# 204
@app.post('/directory/<dir_name>/')
def post(dir_name):
    pass


# move file or directory to subdirectory
# 204 or 404
@app.put('/directory/<from_dir_name>/<to_dir_name>')
def put(from_dir_name, to_dir_name):
    pass


# remove directory
# 204 or 404
@app.delete('/directory/<dir_name>')
def delete(dir_name):
    pass


"""File endpoints"""


# readfile
@app.get('/file/<file_name>')
def get():
    pass


# create file
# body: volume
@app.post('/file/<file_type>/<file_name>')
def post(file_type, file_name):
    pass


# remove file
@app.delete('/file/<file_name>')
def delete(file_name):
    pass


# move file
@app.put('/file/<file_name>/<destination_dir>')
def put(file_name, destination_dir):
    pass


# append a line
# body: new_line_value
@app.patch('/file/<file_name>')
def patch():
    pass


