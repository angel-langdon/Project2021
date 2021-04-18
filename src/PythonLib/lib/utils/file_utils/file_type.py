def is_mobility_pattern(file_path: str) -> bool:
    return "patterns-part" in file_path


def is_brand_info(file):
    return "brand_info" in file


def is_core_poi(file):
    return "core_poi" in file


def get_file_type(file):
    if is_brand_info(file):
        return "brand_info"
    if is_core_poi(file):
        return "core_poi"
    if is_mobility_pattern(file):
        return "mobility_patter"
