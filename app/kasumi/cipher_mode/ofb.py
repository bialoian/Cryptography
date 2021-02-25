from app.kasumi.cipher_mode.cipher_mode import CipherMode
from app.kasumi.kasumi import Kasumi


class OFB(CipherMode):

    def __init__(self, kasumi: Kasumi):
        super().__init__(kasumi)

    def encrypt(self, message: str, key: str, iv: str) -> str:
        """
        Encrypts message with key using OFB mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message)
        key = int(key, 16)
        prev_block = int(iv, 16)

        # OFB
        for i in range(len(kasumi_blocks)):
            prev_block = self.kasumi.encrypt(prev_block, key)
            kasumi_blocks[i] = prev_block ^ kasumi_blocks[i]

        return super()._blocks_to_string(kasumi_blocks, True)

    def decrypt(self, message: str, key: str, iv: str) -> str:
        """
        Decrypts message with key using OFB mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message, True)
        key = int(key, 16)
        prev_block = int(iv, 16)

        # OFB
        for i in range(len(kasumi_blocks)):
            prev_block = self.kasumi.encrypt(prev_block, key)
            kasumi_blocks[i] = prev_block ^ kasumi_blocks[i]

        return super()._blocks_to_string(kasumi_blocks)
