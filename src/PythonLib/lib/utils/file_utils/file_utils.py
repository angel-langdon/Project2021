from typing import Iterable

from utils.path_utils import path_utils


def save_list_in_text_file(file_name: str, iterable: Iterable):
    path_utils.create_dir_if_necessary(file_name)
    with open(file_name, "w") as f:
        f.writelines(l + "\n" for l in iterable)
