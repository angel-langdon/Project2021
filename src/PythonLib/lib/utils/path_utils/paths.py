# %%
import os

datasets_folder_name = "datasets"
max_recursion_limit = 30


def get_datasets_path(dir: str = ".", recursion_level: int = 0) -> str:
    possible_path: str = os.path.join(dir, datasets_folder_name)
    if os.path.isdir(possible_path):
        return os.path.abspath(possible_path)
    if recursion_level > max_recursion_limit:
        raise BaseException(f"Datasets path not found {datasets_folder_name}")
    return get_datasets_path(os.path.join("..", dir), recursion_level + 1)


DATASETS = get_datasets_path()
