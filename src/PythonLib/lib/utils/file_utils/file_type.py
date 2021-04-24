def is_mobility_pattern(file_path: str) -> bool:
    return "patterns-part" in file_path


def is_brand_info(file):
    return "brand_info" in file


def is_core_poi(file):
    return "core_poi" in file


def is_census_data(file):
    return any(t in file for t in ["cbg_b", "cbg_c"])


def is_census_metadata(file):
    return all(t in file for t in ["metadata", "cbg"])


def is_home_panel_summary(file):
    return "home_panel_summary/" in file


def get_file_type(file):
    if is_brand_info(file):
        return "brand_info"
    if is_core_poi(file):
        return "core_poi"
    if is_mobility_pattern(file):
        return "mobility_pattern"
    if is_home_panel_summary(file):
        return "home_panel_summary"
