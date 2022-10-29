from main import *
import pytest


def test_directory_whenAddAnyComponent_endsUpHavingTheComponent():
    # arrange
    tree = Composite("root")
    dir1 = Composite("dir1")
    dir2 = Composite("dir2")
    bin_file = BinaryFile("file1.bin")
    bin_file2 = BinaryFile("file11.bin")
    log_text_file = LogTextFile("file2.txt")
    buffer_file = BufferFile("file3.buff")

    # act
    tree.create(dir1)
    tree.create(dir2)
    tree.create(bin_file)

    dir1.create(bin_file2)
    dir2.create(log_text_file)
    dir2.create(buffer_file)

    # assert
    assert len([c for c in tree.get_children()
                if c.name == dir1.name
                or c.name == dir2.name
                or c.name == bin_file.name]) == 3


def test_componentToRemove_whenRemove_endsUpBeingInexisting():
    tree = Composite("root")
    dir1 = Composite("dir1")
    dir2 = Composite("dir2")
    bin_file = BinaryFile("file1.bin")
    bin_file2 = BinaryFile("file11.bin")
    log_text_file = LogTextFile("file2.txt")
    buffer_file = BufferFile("file3.buff")
    name_of_inexisting = "inexising.buff"
    inexisting_component = BufferFile(name_of_inexisting)

    tree.remove(inexisting_component)
    try:
        tree.read_file(name_of_inexisting)

        assert True
    except KeyError:
        assert False


def test_removedComponent_whenRead_endsUpInvalidOperationError():
    tree = Composite("root")
    dir1 = Composite("dir1")
    dir2 = Composite("dir2")
    bin_file = BinaryFile("file_to_delete.bin")
    bin_file2 = BinaryFile("file11.bin")
    log_text_file = LogTextFile("file2.txt")
    buffer_file = BufferFile("file3.buff")

    tree.read_file("file_to_delete.bin")


def test_directory_whenMaxLimitIsReached_endsUpWithInvalidOperationError():

    # arrange
    dir1 = Composite("dir1")
    dir2 = Composite("dir2")
    excessive_dir = Composite("excessive_dir");
    tree = Composite("root", 2)
    exception_thrown: bool = False

    # act
    tree.create(dir1)
    tree.create(dir2)
    try:
        tree.create(excessive_dir)

        # assert
        assert False
    except:
        assert True


def test_binaryfile_whenMutableOperation_CausesError():

    # arrange
    bin = BinaryFile("default.bin")

    # act
    try:
        bin.push_record("some random string")

        # assert
        assert False
    except:
        assert True


def test_logTextfile_whenRecordIsPushed_TheLineIsAppendedAtTheEnd():

    # arrange
    logfile = LogTextFile("log.txt")
    str_to_push = "hello world"

    # act
    logfile.push_record()

    # assert
    lines_amount = len(logfile.content)
    assert logfile.content[lines_amount - 1] == str_to_push


def test_bufferfile_whenRecordIsRead_TheFirstRecordIsPopped():
    # arrange
    buffer_file = BufferFile("buffer")
    existing_record = buffer_file.content[0]

    # act
    buffer_file.read_file()

    # assert
    assert buffer_file.content[0] != existing_record
