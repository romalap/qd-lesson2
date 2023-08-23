# input is name of the function
import os
from pprint import pprint
import re
from typing import List, Optional

FUNC = "read_file"
DIR = r"C:\python_lesson\qd-lesson2"


def scan_directory(directory: str, exclude: Optional[List[str]] = None) -> List[str]:
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
                files_list.append(root + "\\" + file)
    return files_list


def read_file(filename: str) -> List[str]:
    """ Read file """
    with open(filename, 'r', encoding="utf8") as f:
        return f.readlines()


def find_func(modules: list) -> dict:
    """ Search for all function occurrences in files  
    :param modules: list of paths to modules.
    """
    founded = {}
    for module in modules:
        content = read_file(module)
        for line_number, line in enumerate(content):
            if re.findall(f'{FUNC}(...)', line):
            #if line.find(FUNC) != -1:
                founded[line_number+1] = module
    return founded


if __name__ == '__main__':
    modules_list = scan_directory(
            directory=DIR,
            exclude=["venv", "tests"]
        )

    found_list = find_func(modules_list)
    for line_num, path in found_list.items():
        print(f'File name: {path}. Line number: {line_num}')


    # scan function should return not a filenames but an absolute paths
    # create function that reads a file and check if function is defined in the file https://www.dataquest.io/blog/read-file-python/
