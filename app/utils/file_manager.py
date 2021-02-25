from os import path


def add_to_filename(filename: str, to_add: str) -> str:
    """
    Adds 'to_add' text to the filename
    :param filename:
    :param to_add:
    :return:
    """
    fn_list = filename.split('.')
    fn = '.'.join([fn_list[i] for i in range(len(fn_list) - 1)])
    return fn + to_add + '.' + fn_list[len(fn_list) - 1]


def read_file(path_file: path) -> str:
    """
    Reads the content of the file at path_file
    :param path_file:
    :return:
    """
    content = None
    with open(path_file, 'r') as file:
        content = file.read()

    return content


def write_file(file_path: path, content: str):
    """
    Writes (or overwrite) the content into the file_path
    :param file_path:
    :param content:
    :return:
    """
    with open(file_path, 'w+') as file:
        file.write(content)


def file_loader(text: str, default_file: str, dir_path: path) -> (str, str, bool):
    """
    Loads a file into a string
    :param text: Text outputted to the user
    :param default_file: Default file to load if none is given
    :param dir_path: The directory in which the file is
    :return: The loaded file, the filename and a boolean to quit
    """
    loaded_text = ''
    while True:
        print(text)
        filename = input()
        if filename == 'q':
            return '', '', True

        if len(filename) == 0:
            filename = default_file

        path_file = path.join(dir_path, filename)

        if path.exists(path_file):
            loaded_text = read_file(path_file)

        if len(loaded_text) == 0:
            print('Erreur dans la lecture du fichier')
        else:
            break

    print('Fichier ', filename, ' chargé!')
    return loaded_text, filename, False
