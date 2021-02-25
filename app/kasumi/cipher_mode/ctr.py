from app.kasumi.cipher_mode.cipher_mode import CipherMode
from app.kasumi.kasumi import Kasumi


class CTR(CipherMode):

    def __init__(self, kasumi: Kasumi):
        super().__init__(kasumi)

    def encrypt(self, message: str, key: str, iv: str) -> str:
        """
        Encrypts message with key using Counter mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message)
        key = int(key, 16)
        iv = int(iv, 16)

        # Counter
        for i in range(len(kasumi_blocks)):
            # i is used as the counter (iv is supposed to be concatenated instead of xored but this is fine)
            kasumi_blocks[i] = self.kasumi.encrypt((iv + i) % 2**128, key) ^ kasumi_blocks[i]

        return super()._blocks_to_string(kasumi_blocks, True)

    def decrypt(self, message: str, key: str, iv: str) -> str:
        """
        Decrypts message with key using Counter mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message, True)
        key = int(key, 16)
        iv = int(iv, 16)

        # Counter
        for i in range(len(kasumi_blocks)):
            # i is used as the counter (iv is supposed to be concatenated instead of xored but this is fine)
            kasumi_blocks[i] = self.kasumi.encrypt((iv + i) % 2 ** 128, key) ^ kasumi_blocks[i]

        return super()._blocks_to_string(kasumi_blocks)
