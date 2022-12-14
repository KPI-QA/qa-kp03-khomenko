from main import *
import pytest


def test_directory_whenAddAnyComponent_endsUpHavingTheComponent():
    # arrange
    anySize = 10
    tree = Composite("root", anySize)
    dir1 = Composite("dir1", anySize)
    dir2 = Composite("dir2", anySize)
    bin_file = BinaryFile("file1.bin", anySize)
    bin_file2 = BinaryFile("file11.bin", anySize)
    log_text_file = LogTextFile("file2.txt", anySize)
    buffer_file = BufferFile("file3.buff", anySize)

    # act
    tree.create(dir1)
    tree.create(dir2)
    tree.create(bin_file)
    componentsAmountAtTree: int = 3

    dir1.create(bin_file2)
    componentsAmountAtDir1: int = 1

    dir2.create(log_text_file)
    dir2.create(buffer_file)
    componentsAmountAtDir2: int = 2

    # assert
    assert len([c for c in tree.children
                if c.name == dir1.name
                or c.name == dir2.name
                or c.name == bin_file.name
                ]) == componentsAmountAtTree

    assert len([c for c in dir1.children
                if c.name == bin_file2.name
                ]) == componentsAmountAtDir1

    assert len([c for c in dir2.children
                if c.name == log_text_file.name
                or c.name == buffer_file.name
                ]) == componentsAmountAtDir2


def test_directory_whenMaxLimitReached_endsUpWithError():

    # arrange
    dirDefaultSize: int = 10
    tree = Composite("root", 2)
    dir1 = Composite("dir1", dirDefaultSize)
    dir2 = Composite("dir2", dirDefaultSize)
    excessive_component = Composite("excessive_dir", 5)

    # act
    tree.create(dir1)
    tree.create(dir2)
    try:
        tree.create(excessive_component)

        # assert
        assert False
    except InvalidOperation:
        assert True


def test_directory_whenSourceIsMoveInto_endUpHavingSourceInto():
    dir_default_size: int = 10
    root = Composite("root", 2)
    source = Composite("source", dir_default_size) # to lab fix branch
    destination = Composite("destination", dir_default_size)
    root.create(source)
    root.create(destination)

    Composite.move(source, destination, root)

    assert len(list(filter(lambda c: c.name == source.name, destination.children))) == 1


def test_componentToRemove_whenRemove_endsUpBeingInexisting():
    # arrange
    anySize = 10
    tree = Composite("root", anySize)
    dir1 = Composite("dir1", anySize)
    dir2 = Composite("dir2", anySize)
    bin_file = BinaryFile("file1.bin", anySize)
    bin_file2 = BinaryFile("file11.bin", anySize)
    log_text_file = LogTextFile("file2.txt", anySize)
    buffer_file = BufferFile("file3.buff", anySize)

    tree.create(dir1)
    tree.create(dir2)
    tree.create(bin_file)
    componentsAmountAtTree: int = 3

    dir1.create(bin_file2)
    dir2.create(log_text_file)
    dir2.create(buffer_file)

    # act
    tree.remove(dir1)
    tree.remove(bin_file)

    # assert
    assert len(tree.children) == componentsAmountAtTree - 2
    assert len([c for c in tree.children
                if c.name == dir1.name
                or c.name == bin_file.name]) == 0


def test_binaryfile_whenMutableOperation_CausesError():

    # arrange
    file1 = BinaryFile("default.bin", 5)

    # act
    try:
        file1.push_record("some random string")

        # assert
        assert False
    except InvalidOperation:
        assert True


def test_logTextfile_whenRecordIsPushed_theLineAppendedToEnd():

    # arrange
    logfile = LogTextFile("log.txt", 5)
    str_to_push = "hello world"

    # act
    logfile.push_record(str_to_push)

    # assert
    lines_amount = len(logfile.content)
    assert logfile.content[lines_amount - 1] == str_to_push


def test_bufferfile_whenRecordIsRead_TheFirstRecordIsPopped():
    # arrange
    file1 = BufferFile("buffer", 5)
    file1.push_record("hello world1")
    file1.push_record("hello world2")
    file1.push_record("hello world3")
    the_first_record = file1.content[0]
    the_second_record = file1.content[1]

    # act
    file1.read_file()

    # assert
    assert file1.content[0] != the_first_record
    assert file1.content[0] == the_second_record

def test_bufferfile_whenLimitReached_causesError():

    # arrange
    file1 = BufferFile("file1", 3)

    # act
    for i in range(3):
        file1.push_record(f"hello{i}")
    try:
        file1.push_record("excessive record")
    # assert
        assert False
    except InvalidOperation:
        assert True
