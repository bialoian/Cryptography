from os import path
import random
from pyfinite import ffield  # TODO Create our own implementation !


def multiply_galois_64(a: int, b: int):
    """
    Multiplies a and b in a Galois Field of 2^64
    :param a:
    :param b:
    :return:
    """
    galois_128 = ffield.FField(64, 2**64 + 2**63 + 2**62 + 2**60 + 2**59 + 2**57 + 2**54 + 2**53 + 2**52 + 2**51 +
                               2**46 + 2**44 + 2**43 + 2**42 + 2**41 + 2**40 + 2**39 + 2**38 + 2**34 + 2**31 + 2**0)
    return galois_128.Multiply(a, b)


class GaloisField:
    """
    Manages a Galois Field of the form GF(2^n)
    """

    def __init__(self, bit_length: int = 16, fn_poly: str = 'polynomial.txt'):
        self.irr_polys_8 = [
            2 ** 8 + 2 ** 4 + 2 ** 3 + 2 ** 2 + 2 ** 0,
            2 ** 8 + 2 ** 5 + 2 ** 3 + 2 ** 1 + 2 ** 0,
            2 ** 8 + 2 ** 6 + 2 ** 4 + 2 ** 3 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 8 + 2 ** 6 + 2 ** 5 + 2 ** 1 + 2 ** 0,
            2 ** 8 + 2 ** 6 + 2 ** 5 + 2 ** 2 + 2 ** 0,
            2 ** 8 + 2 ** 6 + 2 ** 5 + 2 ** 3 + 2 ** 0,
            2 ** 8 + 2 ** 7 + 2 ** 6 + 2 ** 1 + 2 ** 0,
            2 ** 8 + 2 ** 7 + 2 ** 6 + 2 ** 5 + 2 ** 2 + 2 ** 1 + 2 ** 0
        ]

        self.irr_polys_16 = [
            2 ** 16 + 2 ** 9 + 2 ** 8 + 2 ** 7 + 2 ** 6 + 2 ** 4 + 2 ** 3 + 2 ** 2 + 2 ** 0,
            2 ** 16 + 2 ** 12 + 2 ** 3 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 12 + 2 ** 7 + 2 ** 2 + 2 ** 0,
            2 ** 16 + 2 ** 13 + 2 ** 12 + 2 ** 10 + 2 ** 9 + 2 ** 7 + 2 ** 6 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 13 + 2 ** 12 + 2 ** 11 + 2 ** 7 + 2 ** 6 + 2 ** 3 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 13 + 2 ** 12 + 2 ** 11 + 2 ** 10 + 2 ** 6 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 14 + 2 ** 10 + 2 ** 8 + 2 ** 3 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 14 + 2 ** 13 + 2 ** 12 + 2 ** 6 + 2 ** 5 + 2 ** 3 + 2 ** 2 + 2 ** 0,
            2 ** 16 + 2 ** 14 + 2 ** 13 + 2 ** 12 + 2 ** 10 + 2 ** 7 + 2 ** 0,
            2 ** 16 + 2 ** 15 + 2 ** 10 + 2 ** 6 + 2 ** 5 + 2 ** 3 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 15 + 2 ** 11 + 2 ** 9 + 2 ** 8 + 2 ** 7 + 2 ** 5 + 2 ** 4 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 15 + 2 ** 11 + 2 ** 10 + 2 ** 7 + 2 ** 6 + 2 ** 5 + 2 ** 3 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 15 + 2 ** 11 + 2 ** 10 + 2 ** 9 + 2 ** 6 + 2 ** 2 + 2 ** 1 + 2 ** 0,
            2 ** 16 + 2 ** 15 + 2 ** 11 + 2 ** 10 + 2 ** 9 + 2 ** 8 + 2 ** 6 + 2 ** 4 + 2 ** 2 + 2 ** 1 + 2 ** 0
        ]
        self.polynomial = 0
        self.generator = 0
        self.bit_length = bit_length
        self.path_poly = path.join(path.join(path.abspath(path.dirname(__file__)), '../../data/'), fn_poly)
        self.galois_field = None

        if path.exists(self.path_poly):
            # Open previously written polynomial setting
            with open(self.path_poly, 'r') as file_poly:
                line_elems = file_poly.readline().split(' ')
                if int(line_elems[0]) == self.bit_length:
                    self.polynomial = int(line_elems[1])
                    self.generator = int(line_elems[2])
                    self.galois_field = ffield.FField(self.bit_length, self.polynomial)

        if self.polynomial == 0:
            self.__generate_polynomial()

    def __generate_polynomial(self):
        """ Generates a generator element in the polynomial """

        power = 0
        res = 1

        # Select a random generator possibility
        # primes_field, _ = _prime_factorize(2 ** self.bit_length - 1)
        # possibilities = _products(primes_field)
        possibilities = [i for i in range(2, 2 ** self.bit_length - 1)]

        # Select a random irreducible polynomial according to the degree
        if self.bit_length == 16:
            self.polynomial = self.irr_polys_16[random.randint(0, len(self.irr_polys_16) - 1)]
        elif self.bit_length == 8:
            self.polynomial = self.irr_polys_8[random.randint(0, len(self.irr_polys_8) - 1)]
        else:
            # TODO select an irreducible polynomial for degrees other than 16 (not required for now)
            print('Oups')

        self.galois_field = ffield.FField(self.bit_length, self.polynomial)
        while True:
            # Select one random polynomial to check if it is a generator
            elem = possibilities[random.randint(0, len(possibilities) - 1)]
            possibilities.remove(elem)  # Remove it from remaining possibilities

            for power in range(2 ** self.bit_length):
                res = self.galois_field.Multiply(res, elem)

                if res == 1:
                    break

            if power == (2 ** self.bit_length) - 2:  # Generator !!!
                break

        self.generator = elem

        with open(self.path_poly, 'w+') as file_poly:
            file_poly.write(str(self.bit_length) + ' ' + str(self.polynomial) + ' ' + str(self.generator))

    def inverse(self, a: int) -> int:
        """
        Gives the inverse of 'a' in the irreducible polynomial
        :param a: The number to get inverse off of it
        :return: The inverse of 'a'
        """

        return self.galois_field.DoInverseForSmallField(a)
