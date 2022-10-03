# Test case for In Memory File System
from main import Drive, Entity, EntityType, File, PathNotFound
import pytest


def test_create():
    """

    We assert if a drive is created "/drive1
    We assert if a folder is created "/drive1/folder1"
    We assert if a text file is created "/drive1/folder1/text_file1"
    We assert if a zipfile is created "/drive1/zipfile1"

    """
    drive1 = Drive()
    assert drive1.create(EntityType.DRIVE, "drive1", "/") == \
            "********************EntityType.DRIVE created********************"
    folder1 = Entity()
    assert folder1.create(EntityType.FOLDER, "folder1", "/drive1")[0] == \
           "********************EntityType.FOLDER created********************"
    text_file = File()
    assert text_file.create(EntityType.TEXTFILE, "text_file1", "/drive1/folder1", "Hello World")[0]\
           == "********************EntityType.TEXTFILE created********************"

    zipfile1 = Entity()
    assert zipfile1.create(EntityType.ZIPFILE, "zipfile1", "/drive1")[0] == \
           "********************EntityType.ZIPFILE created********************"


def test_delete():
    """
    Assert delete function works as expected
    :return:
    """
    drive1 = Drive()
    drive1.create(EntityType.DRIVE, "drive2", "/")
    folder1 = Entity()
    folder1.create(EntityType.FOLDER, "folder1", "/drive2")
    assert folder1.delete("/drive2/folder1")[0] == "!!folder1 is deleted!!"
    # Raise path not found while trying to create a text file under folder1
    with pytest.raises(PathNotFound):
        text_file = File()
        text_file.create(EntityType.TEXTFILE, "text_file1", "/drive2/folder1", "Hello World")


def test_write_to_file():
    """
    Assert write to a file works as expected
    """
    drive1 = Drive()
    drive1.create(EntityType.DRIVE, "drive3", "/")
    folder1 = Entity()
    folder1.create(EntityType.FOLDER, "folder1", "/drive3")
    text_file = File()
    text_file.create(EntityType.TEXTFILE, "text_file1", "/drive3/folder1", "Hello World")
    assert text_file.write_to_file("/drive3/folder1/text_file1", "Hello World!") == "!Current file content updated!"
    # Delete the folder and write to it
    text_file.delete("/drive3/folder1/text_file1")
    with pytest.raises(PathNotFound):
        text_file.write_to_file("/drive3/folder1/text_file1", "Hello World!")


def test_move():
    """
    Create /drive1/folder1/text_file1
    Move folder1 and its contents to /drive2/folder1/text_file1
    :return:
    """
    drive1 = Drive()
    drive1.create(EntityType.DRIVE, "drivetest", "/")
    folder1 = Entity()
    folder1.create(EntityType.FOLDER, "folder1", "/drivetest")
    text_file = File()
    text_file.create(EntityType.TEXTFILE, "text_file1", "/drivetest/folder1", "Hello World")
    drive1.create(EntityType.DRIVE, "drivetest2", "/")
    folder1.move("/drivetest/folder1", "/drivetest2/folder1")
    text_file.write_to_file("/drivetest2/folder1/text_file1", "Hello World!!")
    with pytest.raises(PathNotFound):
        text_file.write_to_file("/drivetest/folder1/text_file1", "Hello World!!")


