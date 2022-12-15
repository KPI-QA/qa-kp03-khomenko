import http
import logging
from api import app

LOGGER = logging.getLogger(__name__)


def test_get_directory_initially():
    expected_response: str = (' ' * 5) + 'root>\n'
    response = app.test_client().get('/directory')
    result = response.data.decode('utf-8')

    assert type(result) is str
    assert result == expected_response
    assert response.status_code == 200


def test_create_directory():
    response = app.test_client().post('/directory/testDir-create', json={"volume": "10"})
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_move_dir1_to_dir2():
    # arrange
    app.test_client().post('/directory/testDir-move-dir1', json={"volume": "10"})
    app.test_client().post('/directory/testDir-move-dir2', json={"volume": "10"})
    from_dir_name = "testDir-move-dir1"
    to_dir_name = "testDir-move-dir2"
    # act
    response = app.test_client().put(f'/directory/{from_dir_name}/{to_dir_name}')

    # assert
    assert response.status_code == 204


def test_move_inexisting_dir_to_another_dir():
    # arrange
    app.test_client().post('/directory/testDir-inex-move-dir1')

    # act
    response = app.test_client().put('/directory/inexisting/testDir-inex-move-dir1')

    # assert
    assert response.status_code == 400


def test_move_dir_to_another_inexisting():
    # arrange
    app.test_client().post('/directory/testDir-inex-move-dir2', json={"volume": "10"})

    # act
    response = app.test_client().put('/directory/testDir-inex-move-dir2/inexisting')

    # assert
    assert response.status_code == 400


def test_remove_existing_dir():
    # arrange
    app.test_client().post('/directory/testDir-remove-dir1', json={"volume": "10"})
    # act
    response = app.test_client().delete('/directory/testDir-remove-dir1')
    # assert
    assert response.status_code == 204


def test_remove_inexisting_dir():
    # arrange
    # act
    response = app.test_client().delete('/directory/inexisting')
    # assert
    assert response.status_code == 400


def test_directory_whenLimitIsReached_addAnotherFile():
    # arrange
    app.test_client().post('/directory/test-limit-directory', json={"volume": "1"})
    app.test_client().post('/directory/notExcessive', json={"volume": "10"})
    app.test_client().post('/file/bufferfile/excessiveComponent', json={"volume": "10"})
    app.test_client().put('/directory/notExcessive/test-limit-directory')
    # act
    response = app.test_client().put('/file/excessiveComponent/test-limit-directory')

    # assert
    assert response.status_code == 400


def test_directory_whenLimitIsReached_addAnotherDirectory():
    # arrange
    app.test_client().post('/directory/test-limit-directory-addDir', json={"volume": "1"})
    app.test_client().post('/directory/notExcessive', json={"volume": "10"})
    app.test_client().post('/directory/excessiveComponent', json={"volume": "10"})
    app.test_client().put('/directory/notExcessive/test-limit-directory-addDir')

    # act
    response = app.test_client().put('/directory/excessiveComponent/test-limit-directory-addDir')

    # assert
    assert response.status_code == 400


# # file

def test_read_bin_file():
    # arrange
    app.test_client().post('/file/binaryfile/testFile-read-binfile', json={"volume": "10"})

    # act
    response = app.test_client().get('/file/testFile-read-binfile')

    # assert
    result = response.data.decode('utf-8')
    assert response.status_code == 200
    assert result == "testFile-read-binfile\nfake content\nyou can look\nbut you can't touch\n"


def test_read_log_file():
    # arrange
    app.test_client().post('/file/logtextfile/testFile-read-logfile', json={"volume": "10"})
    app.test_client().patch('/file/testFile-read-logfile', json={"new_line_value": "first value"})
    app.test_client().patch('/file/testFile-read-logfile', json={"new_line_value": "last value"})
    # act
    response = app.test_client().get('file/testFile-read-logfile')
    # assert
    result = response.data.decode('utf-8')
    assert result == 'testFile-read-logfile\nfirst value\nlast value\n'


def test_read_buffer_file():
    # arrange
    app.test_client().post('/file/bufferfile/testFile-read-bufffile', json={"volume": "10"})
    app.test_client().patch('/file/testFile-read-bufffile', json={"new_line_value": "first value"})
    app.test_client().patch('/file/testFile-read-bufffile', json={"new_line_value": "last value"})
    # act
    response = app.test_client().get('file/testFile-read-bufffile')
    # assert
    result = response.data.decode('utf-8')
    assert result == 'first value\n'


def test_create_binary_file():
    # arrange
    # act
    response = app.test_client().post('/file/binaryfile/testFile-create-binfile', json={"volume": "10"})
    # assert
    assert response.status_code == 200


def test_create_logtext_file():
    # arrange
    # act
    response = app.test_client().post('/file/logtextfile/testFile-create-logtextfile', json={"volume": "10"})
    # assert
    assert response.status_code == 200


def test_create_buffer_file():
    # arrange
    # act
    response = app.test_client().post('/file/bufferfile/testFile-create-bufferfile', json={"volume": "10"})
    # assert
    assert response.status_code == 200


def test_remove_file():
    # arrange
    app.test_client().post('/file/logtextfile/testFile-remove-logtextfile', json={"volume": "10"})
    # act
    response = app.test_client().delete('/file/testFile-remove-logtextfile')
    # assert
    assert response.status_code == 204


def test_move_file_to_directory():
    # arrange
    app.test_client().post('/file/logtextfile/test_move_file_to_directory', json={"volume": "10"})
    app.test_client().post('/directory/test_move_file_to_directory', json={"volume": "10"})
    # act
    response = app.test_client().put('/file/test_move_file_to_directory/test_move_file_to_directory')
    # assert
    assert response.status_code == 204


def test_move_file_to_file():
    # arrange
    app.test_client().post('/file/logtextfile/test_move_file_to_file1', json={"volume": "10"})
    app.test_client().post('/file/logtextfile/test_move_file_to_file2', json={"volume": "10"})
    # act
    response = app.test_client().put('/file/test_move_file_to_file1/test_move_file_to_file2')
    # assert
    assert response.status_code == 404
    assert response.data.decode('utf-8') == 'no such directory'


def test_add_newLine_to_binary():
    # arrange
    app.test_client().post('/file/binaryfile/testFile-patch-bin', json={"volume": "10"})
    # act
    response = app.test_client().patch('/file/testFile-patch-bin', json={"new_line_value": "value that won't be added"})
    # assert
    assert response.status_code == 400


def test_add_newLine_to_log():
    # arrange
    app.test_client().post('/file/logtextfile/testFile-patch-logtextfile', json={"volume": "10"})
    # act
    response = app.test_client().patch('/file/testFile-patch-logtextfile', json={"new_line_value": "hello world"})
    # assert
    assert response.status_code == 204


def test_add_newLine_to_buffer():
    # arrange
    app.test_client().post('/file/bufferfile/testFile-patch-bufferfile', json={"volume": "10"})
    # act
    response = app.test_client().patch('/file/testFile-patch-bufferfile', json={"new_line_value": "hello world"})
    # assert
    assert response.status_code == 204


def test_add_newLine_to_buffer_when_limit_reached():
    # arrange
    app.test_client().post('/file/bufferfile/test-limit-bufferfile', json={"volume": "1"})
    app.test_client().patch('/file/test-limit-bufferfile', json={"new_line_value": "hello world"})
    # act
    response = app.test_client().patch('/file/test-limit-bufferfile', json={"new_line_value": "excessive record"})
    # assert
    assert response.status_code == 400
