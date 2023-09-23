import os
import shutil
from typing import Any
import json

from utils import assert_parameter


def does_directory_exist(path: str) -> bool:
    """Checks if the directory exists"""
    return os.path.isdir(path)


def does_file_exist(path: str) -> bool:
    """Checks if the file exists"""
    return os.path.isfile(path)


def delete_directory(directory: str) -> None:
    """Deletes a folder"""
    assert_parameter(directory, str, "directory")

    if not does_directory_exist(directory):
        raise NotADirectoryError(f"{directory} does not exist!")

    shutil.rmtree(directory)


def create_directory(directory: str) -> None:
    """Creates a folder"""
    assert_parameter(directory, str, "directory")
    os.makedirs(directory)


def list_dirs_in_directory(directory: str) -> list[str]:
    """Lists folders in directory"""
    assert_parameter(directory, str, "directory")

    if not does_directory_exist(directory):
        raise NotADirectoryError(f"{directory} does not exist!")

    return [
        dir
        for dir in os.listdir(directory)
        if does_directory_exist(os.path.join(directory, dir))
    ]


def list_files_in_directory(directory: str) -> list[str]:
    """Lists files in directory"""
    assert_parameter(directory, str, "directory")
    return [
        file
        for file in os.listdir(directory)
        if does_file_exist(os.path.join(directory, file))
    ]


def create_json_file(path: str, data: Any, overwrite: bool = True):
    """Creates a file"""
    assert_parameter(path, str, "path")

    if not path.endswith(".json"):
        raise ValueError(f"{path} is not a valid json filename")

    if not overwrite and does_file_exist(path):
        raise FileExistsError(f"File already exists: {path}")

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def read_json_file(path: str) -> dict:
    """Creates a file"""
    assert_parameter(path, str, "directory")

    if not path.endswith(".json"):
        raise ValueError(f"{path} is not a valid json filename")

    if not does_file_exist(path):
        raise FileNotFoundError(f"File does not exist: {path}")

    with open(path, "r", encoding="utf-8") as file:
        res = json.load(file)
    return res
