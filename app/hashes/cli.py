from os import path

from app.hashes.hash.sponge_hash import SpongeHash
from app.utils.file_manager import file_loader, write_file, read_file

path_data = path.join(path.abspath(path.dirname(__file__)), '../../data/')


def generate():
    """
    CLI to generate a hash from a file and store it
    :return:
    """
    message, filename_message, q_pressed = file_loader("Fichier du dossier data à hasher (test.txt par défaut) :",
                                                       "test.txt",
                                                       path_data)
    if q_pressed:
        return

    print("Fichier du dossier data où stocker le hash (test_hash.txt par défaut) :")
    filename_hash = input()

    if filename_hash == 'q':
        return

    if filename_hash == '':
        filename_hash = 'test_hash.txt'

    h = SpongeHash()
    result_hash = h.hash(message)
    print('Hash de ', filename_message, ' :')
    print(result_hash)

    write_file(path.join(path_data, filename_hash), result_hash)


def check():
    """
    CLI to check if a file matches to a hash
    :return:
    """
    message, _, q_pressed = file_loader("Fichier du dossier data à vérifier (test.txt par défaut) :",
                                        "test.txt",
                                        path_data)
    if q_pressed:
        return

    hash_value, _, q_pressed = file_loader("Fichier du dossier data à vérifier (test_hash.txt par défaut) :",
                                           "test_hash.txt",
                                           path_data)
    if q_pressed:
        return

    h = SpongeHash()
    if h.hash(message) == hash_value:
        print('Le hash correspond au message!')
    else:
        print('Le hash ne correspond pas au message!')


def all():
    """
    Does all the possible actions in hash
    :return:
    """
    print('Hash\n')

    message = read_file(path.join(path_data, 'test.txt'))
    print('Texte brut :\n', message)
    h = SpongeHash()
    hash_result = h.hash(message)
    print('Texte hashé :\n', hash_result)

    hash_check_result = h.hash(message)
    print('Hashage du même texte :\n', message)
    if hash_result == hash_check_result:
        print('Hashs identiques!')
    else:
        print('Hashs différents')

    hash_check_result = h.hash('a' + message)
    print('Hashage du texte différent :\n', 'a' + message)
    if hash_result == hash_check_result:
        print('Hashs identiques!')
    else:
        print('Hashs différents')
