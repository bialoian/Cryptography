import random
from os import path

from app.keys_generator.keys_manager.keys_manager import KeysManager
from app.utils.file_manager import write_file, read_file
from app.utils.modular_arithmetic import gcd, inverse

path_data = path.join(path.abspath(path.dirname(__file__)), '../../../data/')
path_keys = path.join(path_data, 'keys/')
path_public = path.join(path_keys, 'public/')
path_private = path.join(path_keys, 'private/')


class RSAKeysManager(KeysManager):
    """
    Manages RSA public / private key pair
    """

    def __init__(self, keys_filename: str, prime_couple: list = None):

        if path.exists(path.join(path_public, keys_filename)) and path.exists(path.join(path_private, keys_filename)):
            public = read_file(path.join(path_public, keys_filename)).splitlines()
            if public[0] != 'RSA':
                raise Exception('Les clés stockées dans ' + keys_filename + ' ne sont pas des clés RSA')
            self.__e = int(public[1])
            self.__n = int(public[2])

            self.__d = int(read_file(path.join(path_private, keys_filename)).splitlines()[1])
        else:
            if prime_couple is None:
                raise Exception(
                    "Le fichier " + keys_filename + " n'existe pas et les nombres premiers ne sont pas renseignés. Impossible de générer un couple de clés publique / privée!")
            p = prime_couple[0]
            q = prime_couple[1]
            self.__n = p * q

            # Euler's totient function
            phi_n = (p - 1) * (q - 1)

            # Find e coprime with phi(n)
            while True:
                self.__e = random.randint(2, phi_n)
                if gcd(self.__e, phi_n) == 1:
                    break

            # Calculate the inverse of e in phi(n) such as e*d = 1 mod(phi(n))
            self.__d = inverse(self.__e, phi_n)
            # print((self.__e * self.__d) % phi_n)

            # Write new keys to file
            write_file(path.join(path_private, keys_filename), 'RSA\n' + str(self.__d))
            write_file(path.join(path_public, keys_filename), 'RSA\n' +
                       str(self.__e) + '\n' +
                       str(self.__n))

    def get_public_key(self):
        return self.__e

    def get_public(self):
        return [self.__e, self.__n]

    def get_private_key(self):
        return self.__d
