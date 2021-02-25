from app.hashes.hash.hash import Hash
from app.hashes.hash.sha256 import SHA256


class SpongeHash(Hash):
    __message_part_size = 256  # Size of of the messages parts in bits (chosen arbitrarily)
    __message_count_size = 64  # Size of the allocated part for message payload size in bits (chosen arbitrarily)

    def hash(self, message: str, to_hex: bool = True):
        """
        Calculate the hash of the message with SHA-256 encapsulated in a sponge function
        :param message:
        :param to_hex: If true, returns an hexadecimal string of the hash else an integer
        :return: String or integer format of the hash
        """
        message_parts = self.__split_message(message)
        state = self.__absorb(message_parts)
        hash_parts = self.__squeeze(state)
        raw_hash = self.__merge_hash(hash_parts)

        if to_hex:
            return hex(raw_hash).lstrip('0x')

        return raw_hash

    def __absorb(self, message_parts: list) -> int:
        """
        Absorb the message parts and gives the final state
        :param message_parts:
        :return: The final state of the absorb phase
        """

        # State is composed of the bitrate and capacity parts
        # |         State       |
        # | capacity  | bitrate |

        state = 0
        f_hash = SHA256()

        for msg_part in message_parts:
            state ^= msg_part
            state = f_hash.hash(state, to_hex=False, pad_message=False)

        if len(message_parts) < 2:  # Following the constraint to apply the function at least twice
            state = f_hash.hash(state, to_hex=False, pad_message=False)

        return state

    def __squeeze(self, state: int) -> list:
        """
        Extract the final hash from the squeezed states
        :param state: The last state of the absorb process
        :return: The final hash as a list
        """
        bitrate_mask = (1 << self.__message_part_size) - 1
        hash_parts = []
        f_hash = SHA256()
        for i in range(f_hash.get_block_size() // self.__message_part_size):
            hash_parts.insert(0, state & bitrate_mask)
            state = f_hash.hash(state, to_hex=False, pad_message=False)

        return hash_parts

    def __split_message(self, message: str) -> list:
        """
        Splits the message into a list of integers to be processed by the absorption phase
        :param message: Given message as a string
        :return: The list of integers representing the message
        """
        # String to integer
        message_bytes = bytearray(message, 'utf-8')  # String to byte array

        message_length = len(message_bytes) * 8

        if message_length >= (1 << self.__message_count_size):
            raise Exception('Message size must be lower than 2^', self.__message_count_size, ' bits')

        message_int = message_bytes[0]
        for i in range(1, len(message_bytes)):
            message_int = (message_int << 8) | message_bytes[i]

        # Padding

        nb_blocks = (message_length // self.__message_part_size) + 1
        remaining_bits = message_length % self.__message_part_size
        if remaining_bits + 1 + self.__message_count_size <= self.__message_part_size:  # Enough space in the last block
            nb_padding_zeros = self.__message_part_size - remaining_bits - 1 - self.__message_count_size
        else:  # Not enough place in the last block so we will create one more
            nb_padding_zeros = (2 * self.__message_part_size) - remaining_bits - 1 - self.__message_count_size
            nb_blocks += 1

        message_int = (message_int << 1) | 1  # End of message separator
        message_int = message_int << nb_padding_zeros  # Padding of the message to fit the blocks size
        message_int = (message_int << self.__message_count_size) | message_length  # Message bit length at the end

        # Parsing
        mask_block = (1 << self.__message_part_size) - 1

        message_payload = []
        for i in range(nb_blocks):
            message_payload.append((message_int >> ((nb_blocks - i - 1) * self.__message_part_size)) & mask_block)

        return message_payload

    def __merge_hash(self, hash_parts):

        final_hash = 0

        for i in range(len(hash_parts)):
            final_hash = (final_hash << self.__message_part_size) | hash_parts[i]

        return final_hash
