import os


def store_keystore_file_on_the_path(file_path, json_string):
    """Stores a created keystore string data which is JSON format on the file path.

    :param file_path: The path where the file will be saved. type(str)
    :param json_string: Contents of the keystore.
    """
    if os.path.isfile(file_path):
        raise FileExistsError

    with open(file_path, 'wt') as f:
        f.write(json_string)
