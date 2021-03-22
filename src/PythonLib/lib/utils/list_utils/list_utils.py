#%%
from utils.path_utils import path_utils

def listify(list_or_value):
    """ Given a list or a value transforms it to a list
    Arguments:
        list_or_value (str or list): List or a value
    Returns:
        A list
    """
    if isinstance(list_or_value, list):
        return list_or_value
    else:
        return [list_or_value]

def unlistify(list_:list):
    """ Given a list it returns the list or the value if the length is 1
    Arguments:
        list_ (list): List of values
    Returns:
        A list if the length is greater than 1 if not
        returns the first element
    """
    if len(list_) == 1:
        return list_[0]
    else:
        return list_
