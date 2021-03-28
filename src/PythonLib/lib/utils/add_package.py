import os
import site

def add_packages(paths_to_add:list)->None:
    
    """ Adds a list of paths to the environment

    Adds a list of paths to the environment in order to be
    available in other packages

    Arguments:
        paths_to_add (list): list of paths to add to current environment
     
    """
    paths_to_add = [os.path.abspath(path) for path in paths_to_add]
    custom_user_packages_path = os.path.join(site.getsitepackages()[0],
                                             "custom_user_packages.pth")
    with open(custom_user_packages_path, "w") as f:
        print("Creating .pth file: "+custom_user_packages_path)
        print("************************************")
        f.writelines(paths_to_add)
    for path in paths_to_add:
        print("Adding path to environment: "+path)
        
        
PATHS_TO_ADD = [".."]
        
if __name__ == "__main__":
    add_packages(PATHS_TO_ADD)

