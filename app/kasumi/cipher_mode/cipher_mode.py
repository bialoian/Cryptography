import abc
from app.kasumi.kasumi import Kasumi
from app.utils.bit_operation import split_bytes, merge_bytes


class CipherMode(abc.ABC):

    def __init__(self, kasumi: Kasumi):
        self.kasumi = kasumi

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'encrypt') and
                callable(subclass.encrypt) and
                hasattr(subclass, 'decrypt') and
                callable(subclass.decrypt) or
                NotImplemented)

    @staticmethod
    def _string_to_blocks(message: str, is_hex: bool = False) -> list:
        """
        Converts a string into a list of 128-bit blocks
        :param message: The string
        :param is_hex: If the message is an hex string
        :return:
        """
        message_bytes = None
        if is_hex:
            message_bytes = bytearray.fromhex(message)
        else:
            message_bytes = bytearray(message, 'utf-8')

        kasumi_blocks = []
        block_list = []
        for curr_byte in message_bytes:
            if len(block_list) == 8:  # 64 bits
                kasumi_blocks.append(merge_bytes(block_list))  # Creates 64 bits message blocks
                block_list = []
            block_list.append(curr_byte)

        if len(block_list) != 0:  # Make one last block for the remaining bytes
            kasumi_blocks.append(merge_bytes(block_list))

        return kasumi_blocks

    @staticmethod
    def _blocks_to_string(blocks: list, is_hex: bool = False) -> str:
        """
        Converts 128-bit block list to a string
        :param blocks: The block list
        :param is_hex: If the result have to be an hexadecimal string
        :return:
        """
        msg_bytes = bytearray()
        for block in blocks:
            msg_bytes = msg_bytes + split_bytes(block)

        return msg_bytes.hex() if is_hex else msg_bytes.decode().rstrip('\x00')

    @abc.abstractmethod
    def encrypt(self, message: str, key: str, iv: str) -> str:
        """ Encrypt the given message with the key """
        raise NotImplementedError

    @abc.abstractmethod
    def decrypt(self, message: str, key: str, iv: str) -> str:
        """ Decrypt the encrypted message with the key"""
        raise NotImplementedError
