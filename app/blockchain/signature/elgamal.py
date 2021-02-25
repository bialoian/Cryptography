import random

from app.blockchain.signature.signature import Signature
from app.hashes.hash.sponge_hash import SpongeHash
from app.keys_generator.keys_manager.elgamal_keys import ElGamalKeysManager
from app.utils.modular_arithmetic import square_and_multiply, gcd, inverse


class ElGamalSignature(Signature):
    """
    Implementation of the ElGamal signature using SpongeHash
    """

    __k_manager = None
    __h = None

    def __init__(self, k_manager: ElGamalKeysManager):
        self.__k_manager = k_manager
        self.__h = SpongeHash()

    def sign(self, message: str) -> list:
        """
        Signs the given message with ElGamal signature
        :param message: String of the message to sign
        :return: The signature composed of 2 hexadecimal strings
        """

        # Hash the message to sign
        h_digest = self.__h.hash(message, False)

        # Random parameter for the signature
        while True:
            y = random.randint(1, self.__k_manager.get_prime() - 2)
            if gcd(y, self.__k_manager.get_prime() - 1) == 1:
                break

        inv_y = inverse(y, self.__k_manager.get_prime() - 1)

        s1 = square_and_multiply(self.__k_manager.get_generator(), y, self.__k_manager.get_prime())
        s2 = (inv_y * (h_digest - self.__k_manager.get_private_key() * s1)) % (self.__k_manager.get_prime() - 1)

        return [hex(s1).lstrip('0x'), hex(s2).lstrip('0x')]

    @staticmethod
    def verify(message: str, signature: list, public_key: list) -> bool:
        """
        Checks if the signature is valid
        :param message: String of the message to verify
        :param signature: List composed of the two elements of the ElGamal signature
        :param public_key: List containing the public elements of the signer of the message (public, prime, generator)
        :return: True if the signature is valid, else false
        """

        public = public_key[0]
        prime = public_key[1]
        generator = public_key[2]

        # Convert the signature back to integer
        s1 = int(signature[0], 16)
        s2 = int(signature[1], 16)

        # Hash the message to verify
        h = SpongeHash()
        h_digest = h.hash(message, False)

        hs1 = square_and_multiply(public, s1, prime)
        s1s2 = square_and_multiply(s1, s2, prime)
        check1 = (hs1 * s1s2) % prime
        check2 = square_and_multiply(generator, h_digest, prime)

        return check1 == check2
