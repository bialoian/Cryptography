from app.kasumi.cipher_mode.cipher_mode import CipherMode
from app.kasumi.kasumi import Kasumi


class ECB(CipherMode):

    def __init__(self, kasumi: Kasumi):
        super().__init__(kasumi)

    def encrypt(self, message: str, key: str, iv: str) -> str:
        """
        Encrypts message with key using ECB mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message)
        key = int(key, 16)

        # ECB
        for i in range(len(kasumi_blocks)):
            kasumi_blocks[i] = self.kasumi.encrypt(kasumi_blocks[i], key)

        return super()._blocks_to_string(kasumi_blocks, True)

    def decrypt(self, message: str, key: str, iv: str) -> str:
        """
        Decrypts message with key using ECB mode
        :param message:
        :param key:
        :param iv:
        :return:
        """
        kasumi_blocks = super()._string_to_blocks(message, True)
        key = int(key, 16)

        # ECB
        for i in range(len(kasumi_blocks)):
            kasumi_blocks[i] = self.kasumi.decrypt(kasumi_blocks[i], key)

        return super()._blocks_to_string(kasumi_blocks)
