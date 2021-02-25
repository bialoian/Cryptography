import random
from app.utils.bit_operation import right_circ_shift, left_circ_shift


class XORShift:
    """
    XORShift 128 bits vanilla implementation
    """

    def __init__(self):
        # Probably not the most secure way to initialize the state but it works
        self.a = random.getrandbits(32)
        self.b = random.getrandbits(32)
        self.c = random.getrandbits(32)
        self.d = random.getrandbits(32)
        self.mask_32bits = mask = (1 << 32) - 1

    def _generate(self) -> int:
        """
        Generate 32 random bits from xorshift
        :return:
        """
        t = self.d
        s = self.a
        self.d = self.c
        self.c = self.b
        self.b = s

        t ^= (t << 11) & self.mask_32bits
        t ^= (t >> 8) & self.mask_32bits
        self.a = t ^ s ^ ((t >> 19) & self.mask_32bits)
        return self.a

    def getrandbits(self, n_bits):
        """
        Returns a n_bits bits random integer using XORShift
        :param n_bits:
        :return: A n_bits bits random integer
        """

        mask = (1 << n_bits) - 1  # n_bits mask

        # Number of 32 bits required to have n_bits random bits
        n_32bits = n_bits // 32
        if n_bits % 32 != 0:
            n_32bits += 1

        result = 0
        for i in range(n_32bits):
            result = (result << 32) | self._generate()

        return result & mask
