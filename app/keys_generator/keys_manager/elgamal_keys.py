from os import path

from app.keys_generator.keys_manager.keys_manager import KeysManager
from app.keys_generator.xorshift import XORShift
from app.utils.file_manager import read_file, write_file
from app.utils.modular_arithmetic import square_and_multiply

path_data = path.join(path.abspath(path.dirname(__file__)), '../../../data/')
path_keys = path.join(path_data, 'keys/')
path_public = path.join(path_keys, 'public/')
path_private = path.join(path_keys, 'private/')


class ElGamalKeysManager(KeysManager):
    """
    Manages ElGamal public / private key pair
    """

    def __init__(self, keys_filename: str, prime: int = None, generator: int = None):
        self.__prime = prime
        self.__generator = generator

        if path.exists(path.join(path_public, keys_filename)) and path.exists(path.join(path_private, keys_filename)):
            # Load existing keys

            public = read_file(path.join(path_public, keys_filename)).splitlines()
            if public[0] != 'ElGamal':
                raise Exception('Les clés stockées dans ' + keys_filename + ' ne sont pas des clés ElGamal')
            self.__public_key = int(public[1])
            self.__prime = int(public[2])
            self.__generator = int(public[3])

            self.__private_key = int(read_file(path.join(path_private, keys_filename)).splitlines()[1])
        else:
            if prime is None or generator is None:
                raise Exception('Le fichier ', keys_filename, " n'existe pas et le nombrer premier et son générateur "
                                                              "ne sont pas renseignés. Impossible de générer un "
                                                              "couple de clés publique / privée!")

            # Generate new keys
            xorshift = XORShift()
            self.__private_key = xorshift.getrandbits(512)
            self.__public_key = square_and_multiply(generator, self.__private_key, prime)

            # Write new keys to files
            write_file(path.join(path_private, keys_filename), 'ElGamal\n' + str(self.__private_key))
            write_file(path.join(path_public, keys_filename), 'ElGamal\n' +
                       str(self.__public_key) + '\n' +
                       str(prime) + '\n' +
                       str(generator))

    def get_public_key(self) -> int:
        return self.__public_key

    def get_public(self) -> list:
        """
        Gives the public elements of the key
        :return:
        """
        return [self.__public_key, self.__prime, self.__generator]

    def get_private_key(self) -> int:
        return self.__private_key

    def get_prime(self) -> int:
        return self.__prime

    def get_generator(self) -> int:
        return self.__generator

    def generate_shared_key(self, gb: int):
        """
        Generate the Diffie-Hellman shared key using g^b
        Alice -> g^b ^ a = g^ba
        Bob -> g^a ^ b = g^ab
        In order for it to work Alice and Bob must have the same prime and generator
        :param gb: Public key of the other person
        :return:
        """

        # Check if the other person's public key is valid
        if 2 <= gb <= self.__prime - 2:  # Check boundaries
            return square_and_multiply(gb, self.__private_key, self.__prime)  # Shared secret key!

        else:
            raise Exception("La clé publique donnée n'est pas valide!!!")
