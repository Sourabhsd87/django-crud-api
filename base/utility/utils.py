import os

def confirm_dir_exists(dir_path):
    """
    Makes sure whether the directory path given exists. If it does not,
    then it creates one and returns the path.
    """

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path