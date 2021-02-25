from app.kasumi.cipher_mode.cipher_mode import CipherMode
from app.kasumi.galois_field import multiply_galois_64
from app.kasumi.kasumi import Kasumi


class GCM(CipherMode):

    def __init__(self, kasumi: Kasumi):
        super().__init__(kasumi)

    def encrypt(self, message: str, key: str, iv: str) -> str:
        """
        Encrypts message with key using Galois Counter Mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message)
        key = int(key, 16)
        iv = int(iv, 16)

        tag = 0
        h = self.kasumi.encrypt(0, key)

        zero_count_block = self.kasumi.encrypt(iv, key)

        # Galois Counter Mode
        for i in range(len(kasumi_blocks)):
            # i is used as the counter (iv is supposed to be concatenated instead of xored but this is fine)
            kasumi_blocks[i] = self.kasumi.encrypt((iv + i + 1) % 2**128, key) ^ kasumi_blocks[i]
            tag = multiply_galois_64(tag ^ kasumi_blocks[i], h)

        tag = multiply_galois_64(tag ^ len(kasumi_blocks), h)
        tag ^= zero_count_block
        kasumi_blocks.append(tag)

        return super()._blocks_to_string(kasumi_blocks, True)

    def decrypt(self, message: str, key: str, iv: str) -> str:
        """
        Decrypts message with key using Galois Counter Mode
        :param message:
        :param key:
        :param iv:
        :return:
        """

        kasumi_blocks = super()._string_to_blocks(message, True)
        key = int(key, 16)
        iv = int(iv, 16)

        tag = 0
        h = self.kasumi.encrypt(0, key)

        zero_count_block = self.kasumi.encrypt(iv, key)

        # Galois Counter Mode
        for i in range(len(kasumi_blocks) - 1):
            tag = multiply_galois_64(tag ^ kasumi_blocks[i], h)
            # i is used as the counter (iv is supposed to be concatenated instead of xored but this is fine)
            kasumi_blocks[i] = self.kasumi.encrypt((iv + i + 1) % 2 ** 128, key) ^ kasumi_blocks[i]

        tag = multiply_galois_64(tag ^ (len(kasumi_blocks) - 1), h)
        tag ^= zero_count_block

        if tag == kasumi_blocks[len(kasumi_blocks) - 1]:
            print("Message GCM intègre!")
        else:
            print("problème d'intégrité  du message!")

        return super()._blocks_to_string(kasumi_blocks[:len(kasumi_blocks) - 1])
