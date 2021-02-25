from app.kasumi.galois_field import GaloisField
from app.utils.bit_operation import left_circ_shift


class Kasumi:
    """ Implementation of the KASUMI algorithm as described in the 3GPP specification with a few modifications """

    def __init__(self):
        self.round_keys = []
        self.round_keys_prime = []
        self.sub_keys_KL1 = []
        self.sub_keys_KL2 = []
        self.sub_keys_KO1 = []
        self.sub_keys_KO2 = []
        self.sub_keys_KO3 = []
        self.sub_keys_KI1 = []
        self.sub_keys_KI2 = []
        self.sub_keys_KI3 = []
        self.sbox_fi_1 = []
        self.sbox_fi_2 = []

        self.galois_field = GaloisField()

    def encrypt(self, message: int, key: int) -> int:
        """
        Encrypts the given message with the key
        :param message: 64-bit message block
        :param key: 128-bit key
        :return: Encrypted message block
        """
        self.__key_schedule(key)

        left = message >> 32
        right = message & 0xffffffff

        # Main feistel rounds
        for nb_round in range(0, 8):
            next_right = left
            next_left = right ^ self.__main_f(left, nb_round)

            # Swap left and right
            right = next_right
            left = next_left
        return (left << 32) | right

    def decrypt(self, message: int, key: int) -> int:
        """
        Decrypts the given message with the key
        :param message: 64-bit encrypted message block
        :param key: 128-bit key
        :return: Decrypted message block
        """
        self.__key_schedule(key)

        left = message >> 32
        right = message & 0xffffffff

        # Main Feistel rounds
        for nb_round in range(7, -1, -1):  # In reverse in order to have the key matching with encrypt
            next_left = right
            next_right = self.__main_f(right, nb_round) ^ left

            # Swap left and right
            left = next_left
            right = next_right

        return (left << 32) | right

    def __key_schedule(self, key: int):
        """
        Generate all the subkeys based on the 128bits main key
        :param key: Main key as a string
        :return:
        """

        # Reset the variables (might have been allocated before)
        self.round_keys = []
        self.round_keys_prime = []
        self.sub_keys_KL1 = []
        self.sub_keys_KL2 = []
        self.sub_keys_KO1 = []
        self.sub_keys_KO2 = []
        self.sub_keys_KO3 = []
        self.sub_keys_KI1 = []
        self.sub_keys_KI2 = []
        self.sub_keys_KI3 = []
        self.sbox_fi_1 = []
        self.sbox_fi_2 = []

        key_prime = key ^ 0x0123456789ABCDEFFEDCBA9876543210

        # Split keys in 8 parts
        for i in range(8):
            bit_shift = 16 * i
            # use 0xffff as a mask to extract the lower 16 bits
            self.round_keys.append((key >> bit_shift) & 0xffff)
            self.round_keys_prime.append((key_prime >> bit_shift) & 0xffff)

        # Reverse the keys to be in the right order 1, 2, ..., 8 instead of 8, 7, ..., 1
        self.round_keys.reverse()
        self.round_keys_prime.reverse()

        # Set round subkeys
        for i in range(8):
            self.sub_keys_KL1.append(left_circ_shift(self.round_keys[i], 1, 16))
            self.sub_keys_KL2.append(self.round_keys_prime[(i + 2) % 8])
            self.sub_keys_KO1.append(left_circ_shift(self.round_keys[(i + 1) % 8], 5, 16))
            self.sub_keys_KO2.append(left_circ_shift(self.round_keys[(i + 5) % 8], 8, 16))
            self.sub_keys_KO3.append(left_circ_shift(self.round_keys[(i + 6) % 8], 13, 16))
            self.sub_keys_KI1.append(self.round_keys_prime[(i + 4) % 8])
            self.sub_keys_KI2.append(self.round_keys_prime[(i + 3) % 8])
            self.sub_keys_KI3.append(self.round_keys_prime[(i + 7) % 8])

        # Create the S-boxes (EZ key schedule)
        self.sbox_fi_1 = self.__generate_sbox(key)
        self.sbox_fi_2 = self.__generate_sbox(key_prime)

    @staticmethod
    def __generate_sbox(key_box: int) -> bytearray:
        """
        Generate a 256 x 8 bits Substitution box based on RC4 initialization with a 128-bit key
        :param key_box: The 128-bit key
        :return: The generated S-box
        """

        # Extract bytes from the key in a list
        keys = []
        for i in range(16):
            mask_key = 0xff << (i * 8)
            keys.append((key_box & mask_key) >> (i * 8))

        # RC4 initialization
        sbox = bytearray(256)
        for i in range(256):
            sbox[i] = i

        j = 0
        for i in range(256):
            j = (j + sbox[i] + keys[i % 16]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]  # Swap

        return sbox

    @staticmethod
    def __string_to_int(string: str) -> int:
        """
        Converts a 128-bit string to a 128-bit integer
        :param string: String to convert
        :return: The converted integer
        """
        result = int(string, 16)
        if result.bit_length() > 128:
            raise Exception("The string must be 128 bits or lesser")

        return result

    def __fl(self, input_i: int, round_i: int) -> int:
        """
        Function FL
        :param input_i: 32-bit data input of the ith round
        :param round_i: Number of the current round (between 0 and 7)
        :return: 32-bit output value
        """
        left = input_i >> 16  # shift by 16 to the right to get the big endian
        right = input_i & 0xffff  # Mask to get the right part to extract the little endian

        # With inverse in a Galois field

        right_prime = self.galois_field.inverse(right ^ left_circ_shift(left & self.sub_keys_KL1[round_i], 1, 16))
        left_prime = self.galois_field.inverse(left ^ left_circ_shift(right_prime | self.sub_keys_KL2[round_i], 1, 16))

        return (left_prime << 16) | right_prime

    def __fo(self, input_i: int, round_i: int) -> int:
        """
        Function FO
        :param input_i: 32-bit data input of the ith round
        :param round_i: Number of the current round (between 0 and 7)
        :return: 32-bit output value
        """
        left = input_i >> 16  # shift by 16 to the right to get the big endian
        right = input_i & 0xffff  # Mask to get the right part to extract the little endian

        # Round 1
        right_tmp = self.__fi((left ^ self.sub_keys_KO1[round_i]), self.sub_keys_KI1[round_i]) ^ right
        left_tmp = right
        # Round 2
        right = self.__fi((left_tmp ^ self.sub_keys_KO2[round_i]), self.sub_keys_KI2[round_i]) ^ right_tmp
        left = right_tmp
        # Round 3
        right_tmp = self.__fi((left ^ self.sub_keys_KO3[round_i]), self.sub_keys_KI3[round_i]) ^ right
        left_tmp = right

        return (left_tmp << 16) | right_tmp

    def __fi(self, input_i: int, key_ki: int) -> int:
        """
        Function FI
        :param input_i: 16-bit data input
        :param key_ki: 16-bit KI key
        :return: 16-bit output value
        """
        z1 = key_ki >> 8  # shift by 8 to the right to get the big endian
        z2 = key_ki & 0xff  # Mask to get the right part to extract the little endian
        z_result = (self.sbox_fi_1[z1] << 8) | self.sbox_fi_2[z2]

        return (input_i >> 2) ^ z_result

    def __main_f(self, input_i: int, nb_round: int) -> int:
        """
        Functions block of the main Feistel network
        :param input_i: Input of the round
        :param nb_round: Round number
        :return:
        """

        if nb_round % 2 == 0:  # When even : -> fo -> fl
            tmp = self.__fo(input_i, nb_round)
            result = self.__fl(tmp, nb_round)
        else:  # When odd : -> fl -> fo
            tmp = self.__fl(input_i, nb_round)
            result = self.__fo(tmp, nb_round)

        return result
