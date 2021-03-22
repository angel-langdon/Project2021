#%%
import os
from utils.list_utils import list_utils

def get_absolute_path(paths):
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

# %%
