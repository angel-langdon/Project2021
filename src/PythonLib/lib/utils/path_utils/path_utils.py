# %%
import os

from utils.list_utils import list_utils


def get_absolute_path(paths: list):
    """ Returns the absolute path of given paths
    Arguments:
        paths (str or list): A str or a list of paths
    Returns:
        Returns a list of absolute paths in case there is 
        more than 1 path, else returns only the path as string
    """
    paths = list_utils.listify(paths)
    paths = [os.path.abspath(path) for path in paths]
    return list_utils.unlistify(paths)


def create_dir_if_necessary(path: str):
    dir_name: str = os.path.dirname(path)
    if dir_name != '' and not os.path.isdir(dir_name):
        os.makedirs(dir_name)


def list_files_recursively(path):
    fs = []
    for root, _, files in os.walk(path):
        for f in files:
            if f != ".DS_Store":
                f = os.path.join(root, f)
                fs.append(f)
    return fs
