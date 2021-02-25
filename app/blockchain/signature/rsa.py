from app.blockchain.signature.signature import Signature
from app.hashes.hash.sponge_hash import SpongeHash
from app.keys_generator.keys_manager.rsa_keys import RSAKeysManager
from app.utils.modular_arithmetic import square_and_multiply


class RSASignature(Signature):

    def __init__(self, k_manager: RSAKeysManager):
        self.__k_manager = k_manager
        self.__h = SpongeHash()

    def sign(self, message: str) -> str:
        """
        Signs the given message with RSA signature
        :param message: String of the message to sign
        :return: The signature of the message as an hexadecimal string
        """
        h_digest = self.__h.hash(message, to_hex=False)
        n = self.__k_manager.get_public()[1]  # n is public in RSA
        signature = square_and_multiply(h_digest, self.__k_manager.get_private_key(), n)

        return hex(signature).lstrip('0x')

    @staticmethod
    def verify(message: str, signature: str, public_key: list) -> bool:
        """
        Checks if the signature is valid
        :param message: String of the message to verify
        :param signature: Signature of the message in hexadecimal string
        :param public_key: List composed of e and n
        :return: True if the signature is valid, else false
        """

        # Convert the signature back to integer
        signature = int(signature, 16)

        # Hash the message to verify
        h = SpongeHash()
        h_digest = h.hash(message, to_hex=False)

        # Get the values from the public key
        e = public_key[0]
        n = public_key[1]

        hash_verify = square_and_multiply(signature, e, n)

        # (H(m))^(e*d) mod n = H(m)
        return h_digest == hash_verify
