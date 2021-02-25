from app.hashes.hash.hash import Hash
from app.utils.bit_operation import right_circ_shift, add_mod


class SHA256(Hash):
    """
    Implementation of SHA-256 according to the FIPS 180-4
    """

    __block_size = 64  # SHA-256 block size in bytes (64 bytes = 512 bits)
    __message_count_size = 64  # Size of the allocated part for message size in bits
    __message_schedule_size = 64  # Size of the message schedule array

    # SHA-256 constants
    __k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    __initial_h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    def __init__(self, verbose: bool = False):
        self.__verbose = verbose
        self.__message = None
        self.__payload = None
        self.__h = []
        self.__message_blocks = []
        self.__message_schedule = []
        self.__pad_message = None

    def hash(self, message, to_hex: bool = True, pad_message: bool = True):
        """
        Calculates the SHA-256 of the given message
        :param message:
        :param to_hex: If true, returns an hexadecimal string of the hash else an integer
        :param pad_message: Pad the message with its size if true
        :return: String or integer format of the hash
        """
        self.__pad_message = pad_message
        self.__payload = None
        self.__message_blocks = []
        self.__message_schedule = []
        self.__message = message
        self.__h = []

        if self.__verbose:
            print('Preprocessing')

        self.__preprocessing()

        if self.__verbose:
            print('Compute hash')
        raw_hash = self.__compute_hash()

        if to_hex:
            return hex(raw_hash).lstrip('0x')

        return raw_hash

    def __preprocessing(self):
        """
        Section 5
        Preprocessing operations required to do SHA-256
        :return:
        """

        # String to payload
        if isinstance(self.__message, str):
            message_bytes = bytearray(self.__message, 'utf-8')  # String to byte array

            message_length = len(message_bytes) * 8

            if message_length >= (1 << self.__message_count_size):
                raise Exception('Message size must be lower than 2^', self.__message_count_size, ' bits')

            self.__payload = message_bytes[0]
            for i in range(1, len(message_bytes)):
                self.__payload = (self.__payload << 8) | message_bytes[i]

        elif isinstance(self.__message, int):
            self.__payload = self.__message
            message_length = self.__payload.bit_length()
        else:
            raise Exception('Unsupported type for message')

        if self.__verbose:
            print('Payload: \n', bin(self.__payload).lstrip('0b'))

        if self.__pad_message:
            nb_blocks = self.__padding(message_length)
        else:  # If the message must not be padded, the message is unchanged and its size is the size of 1 block
            nb_blocks = 1

        if self.__verbose:
            print('\nPadded payload:\n', bin(self.__payload).lstrip('0b'))

        self.__parsing(nb_blocks)

        # Section 5.3 : Initial hash values
        self.__h.append([])
        self.__h[0] = self.__initial_h

    def __padding(self, message_length: int) -> int:
        """
        Section 5.1: Ensures that the message fits into 512-bit blocks
        :param message_length: Raw length of the message
        :return: Number of blocks after padding
        """

        nb_blocks = (message_length // (self.__block_size * 8)) + 1
        nb_remaining_bits = message_length % (self.__block_size * 8)  # Number of bits that do not fit in the blocks

        if nb_remaining_bits + 1 + self.__message_count_size <= (
                self.__block_size * 8):  # Enough space in the last block
            nb_padding_zeros = (self.__block_size * 8) - nb_remaining_bits - 1 - self.__message_count_size
        else:  # Not enough place in the last block so we will create one more
            nb_padding_zeros = (2 * (self.__block_size * 8)) - nb_remaining_bits - 1 - self.__message_count_size
            nb_blocks += 1

        self.__payload = (self.__payload << 1) | 1  # End of message separator
        self.__payload = self.__payload << nb_padding_zeros  # Padding of the message to fit the blocks size
        self.__payload = (self.__payload << self.__message_count_size) | message_length  # Message bit length at the end

        return nb_blocks

    def __parsing(self, nb_blocks: int):
        """
        Section 5.3: Splits the message into 512-bit blocks
        :param nb_blocks: Number of blocks to parse
        :return:
        """

        mask_block = (1 << (self.__block_size * 8)) - 1

        for i in range(nb_blocks):
            self.__message_blocks.append((self.__payload >> ((nb_blocks - i - 1) * 512)) & mask_block)

            if self.__verbose:
                print('Block ', str(i), '\n', bin(self.__message_blocks[i]).lstrip('0b'))

    def __compute_hash(self) -> int:
        """
        Compute the hash and return it as an integer
        :return:
        """

        mask = (1 << 32) - 1

        # Compression of the message
        for i in range(len(self.__message_blocks)):
            curr_message_block = self.__message_blocks[i]

            # Prepare the message schedule
            self.__prepare_message_schedule(curr_message_block)

            # Initialize the 8 working variables
            a, b, c, d, e, f, g, h = self.__h[i]

            for t in range(64):
                t1 = h + self.__sigma_maj1(e) + self.__ch(e, f, g) + self.__k[t] + self.__message_schedule[t]
                t2 = self.__sigma_maj0(a) + self.__maj(a, b, c)
                h = g
                g = f
                f = e
                e = (d + t1) & mask
                d = c
                c = b
                b = a
                a = (t1 + t2) & mask

            # Compute the intermediate hash value
            self.__h.append([
                (a + self.__h[i][0]) & mask,
                (b + self.__h[i][1]) & mask,
                (c + self.__h[i][2]) & mask,
                (d + self.__h[i][3]) & mask,
                (e + self.__h[i][4]) & mask,
                (f + self.__h[i][5]) & mask,
                (g + self.__h[i][6]) & mask,
                (h + self.__h[i][7]) & mask,
            ])

        final_hash = 0

        for hi in self.__h[len(self.__message_blocks)]:
            final_hash = (final_hash << 32) | hi

        return final_hash

    def __prepare_message_schedule(self, curr_message_block: int):
        """
        Prepare the message schedule of the block to hash
        :param curr_message_block:
        :return:
        """
        # Split the 512-bit block in 16*32
        block_parts = self.__split_block(curr_message_block)

        # The first 16 words of the message schedule are the block in 32-bits
        self.__message_schedule = block_parts

        # The message schedule is expanded to 64 words using the previous values
        for t in range(16, self.__message_schedule_size):
            # σ1(W[t - 2]) + W[t - 7] + σ0(W[t - 15]) + W[t - 16]
            self.__message_schedule.append(
                add_mod(
                    self.__sigma1(self.__message_schedule[t - 2]) + self.__message_schedule[t - 7],
                    self.__sigma0(self.__message_schedule[t - 15]) + self.__message_schedule[t - 16]
                )
            )

        if self.__verbose:
            print('\nMessage schedule:')
            for i in range(64):
                print(format(i, ' 3'), ' ', format(self.__message_schedule[i], '032b'))

    @staticmethod
    def __ch(x: int, y: int, z: int) -> int:
        """
        Section 4.1.2: Ch function
        Choice function that takes the bit from y if x is 1 and z if x is 0 (bitwise)
        :param x: 32-bit integer
        :param y: 32-bit integer
        :param z: 32-bit integer
        :return: 32-bit integer
        """

        # ~ bitwise not operator works with 32 bits so it is fine here
        return (x & y) ^ (~x & z)

    @staticmethod
    def __maj(x: int, y: int, z: int) -> int:
        """
        Section 4.1.2: Maj function
        Gives the majority of x, y and z bitwise
        :param x: 32-bit integer
        :param y: 32-bit integer
        :param z: 32-bit integer
        :return: 32-bit integer
        """
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def __sigma_maj0(x: int) -> int:
        """
        Section 4.1.2: ∑0 function
        :param x: 32-bit integer
        :return: 32-bit integer
        """
        return right_circ_shift(x, 2, 32) ^ right_circ_shift(x, 13, 32) ^ right_circ_shift(x, 22, 32)

    @staticmethod
    def __sigma_maj1(x: int) -> int:
        """
        Section 4.1.2: ∑1 function
        :param x: 32-bit integer
        :return: 32-bit integer
        """
        return right_circ_shift(x, 6, 32) ^ right_circ_shift(x, 11, 32) ^ right_circ_shift(x, 25, 32)

    @staticmethod
    def __sigma0(x: int) -> int:
        """
        Section 4.1.2: σ0 function
        :param x: 32-bit integer
        :return: 32-bit integer
        """
        return right_circ_shift(x, 7, 32) ^ right_circ_shift(x, 18, 32) ^ (x >> 3)

    @staticmethod
    def __sigma1(x: int) -> int:
        """
        Section 4.1.2 σ1 function
        :param x: 32-bit integer
        :return: 32-bit integer
        """
        return right_circ_shift(x, 17, 32) ^ right_circ_shift(x, 19, 32) ^ (x >> 10)

    @staticmethod
    def __split_block(curr_message_block) -> list:
        """
        Splits a 512-bit message block into a list of 16 32-bit elements
        :param curr_message_block:
        :return: The list of 16 32-bit elements
        """
        block_parts = []
        mask = (1 << 32) - 1
        for i in range(16):
            block_parts.insert(0, (curr_message_block >> (i * 32)) & mask)

        return block_parts

    def get_block_size(self) -> int:
        """
        Give the hash block size in bits
        :return:
        """
        return self.__block_size * 8
