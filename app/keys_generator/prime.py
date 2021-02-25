from os import path
import random
from app.keys_generator.xorshift import XORShift
from app.utils.file_manager import read_file, write_file
from app.utils.modular_arithmetic import square_and_multiply


def _generate_possible_prime(n_bits: int = 128) -> int:
    """
    Generate an odd random number of n_bits bits
    :param n_bits: Number of bits of the random number
    :return:
    """
    xorshift = XORShift()
    possible_prime = xorshift.getrandbits(n_bits)

    # Make sure it is at least of the size n_bits bits
    possible_prime |= (1 << (n_bits - 1))

    # Make sure it is odd
    possible_prime |= 1

    return possible_prime


def _check_is_prime(possible_prime: int, test_rounds: int = 40) -> bool:
    """
    Checks if the given number is a prime with Miller-Rabin test
    :param possible_prime: The number to check
    :param test_rounds: Number of test rounds for Miller-Rabin, it is the accuracy level. Internet says it should be 40
    :return: True if prime
    """

    # 2^s * d = n - 1
    d = possible_prime - 1
    s = 0
    while (d & 1) == 0:  # d is even
        s += 1
        d >>= 1  # division by 2 of even number

    for i in range(test_rounds):
        if not _miller_rabin_test(possible_prime, d):
            return False

    return True


def _miller_rabin_test(possible_prime: int, d: int) -> bool:
    """
    Performs a Rabin-Miller test on a possible prime
    :param d: As 2^s * d = n - 1
    :param possible_prime:
    :return: True if possible prime, else false
    """
    a = random.randint(2, possible_prime - 2)
    adn = square_and_multiply(a, d, possible_prime)

    if adn == 1 or adn == possible_prime - 1:
        return True

    while d != possible_prime - 1:
        adn = square_and_multiply(adn, 2, possible_prime)
        d *= 2

        if adn == 1:
            return False

        if adn == possible_prime - 1:
            return True

    return False


def get_prime(n_bits: int) -> int:
    """
    Creates a safe prime of n_bits bits
    :param n_bits: The number of bits of the generated safe prime
    :return: The generated safe prime
    """
    prime = None
    while True:
        prime = _generate_possible_prime(n_bits)
        if _check_is_prime(prime) and _check_is_prime((prime - 1) >> 1):  # Safe prime
            break

    return prime


def find_generator(prime: int) -> int:
    """
    Finds a generator element to the given safe prime
    :param prime:
    :return:
    """
    generator = 0
    while True:
        generator = random.randint(2, prime - 2)
        if square_and_multiply(generator, (prime - 1) >> 1, prime) != 1:
            break

    return generator


class Prime:
    """
    Handles a prime and its generator
    """

    def __init__(self, prime_path: path, n_bits: int = 512, with_generator: bool = True):
        self.__generator = 0

        if path.exists(prime_path):
            # Load existing prime
            prime_lines = read_file(prime_path).splitlines()
            self.__prime = int(prime_lines[0])
            if len(prime_lines) > 1:
                self.__generator = int(prime_lines[1])
        else:
            # Generate a new prime
            self.__prime = get_prime(n_bits)
            if with_generator:
                self.__generator = find_generator(self.__prime)
                write_file(prime_path, str(self.__prime) + '\n' + str(self.__generator))
            else:
                write_file(prime_path, str(self.__prime))

    def get_prime(self) -> int:
        return self.__prime

    def get_generator(self) -> int:
        return self.__generator
