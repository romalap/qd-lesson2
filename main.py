# input is name of the function
import argparse
import os
from random import choice
from typing import List, Optional
import ast

DIR = r"C:\python_lesson\qd-lesson2"

def parsed_args():
    """ Parse args. """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--func', required=True, type=str, default=None, help='Please provide function name.')
    return parser.parse_args()


def scan_directory(directory: str, exclude: Optional[List[str]] = None) -> List[str]:
    """ Find all python files. """
    files_list = []
    for root, _, files in os.walk(directory):
        found_exclude = False
        for exclude_dir in exclude:
            if exclude_dir in root:
                found_exclude = True
                break
        if found_exclude:
            continue
        for file in files:
            if file.endswith(".py"):
                files_list.append(os.path.join(root, file))
    return files_list


def read_file(filename: str) -> str:
    """ Read file """
    with open(filename, "r", encoding="utf8") as file:
        return file.read()


def find_func_def(modules: list) -> dict:
    """ Search for all function occurrences in files.
    :param modules: list of paths to modules.
    """
    founded = {}
    for module in modules:
        content = read_file(module)
        file_content = ast.parse(content)
        for item in ast.walk(file_content):
            if isinstance(item, ast.FunctionDef):
                founded[item.name] = module
    return founded


def find_func_calls(modules: list) -> List[List[str]]:
    """ Search for all calls occurrences in files.
    :param modules: list of paths to modules.
    """
    founded = []
    for module in modules:
        content = read_file(module)
        file_content = ast.parse(content)
        for item in ast.walk(file_content):
            if isinstance(item, ast.FunctionDef):
                function_name = item.name
                for item in ast.walk(item):
                    if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
                        list_ = [item.func.id, module, function_name]
                        founded.extend([list_ for _ in range(len(list_))])
    return founded


if __name__ == '__main__':
    args = parsed_args()
    modules_list = scan_directory(
            directory=DIR,
            exclude=["venv", "tests"]
        )
    found_def = find_func_def(modules_list)
    found_calls = find_func_calls(modules_list)
    print(found_calls)

    # leson 3
    # two separate functions to get func defenitions and func calls.
