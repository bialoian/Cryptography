from collections import Counter


def prime_decomposition(n: int) -> (list, list):
    """
    Decompose a number in prime factors
    :param n: The number to decompose
    :return: List of prime factors and list of occurrences of prime factors
    """
    prime_factors = []

    while n % 2 == 0:  # Check if divisible by 2
        prime_factors.append(2)
        n /= 2

    factor = 3

    while (factor * factor) <= n:
        if n % factor == 0:
            prime_factors.append(factor)
            n /= factor
        else:
            factor += 2  # Next possible factor

    if n != 0:
        prime_factors.append(n)  # Add last prime

    prime_factors_count = Counter(prime_factors).values()  # Count prime factors occurrences
    prime_factors = list(set(prime_factors))  # Remove duplicates
    return prime_factors, prime_factors_count


def square_and_multiply(a: int, power: int, modulo: int) -> int:
    """
    Fast technique for exponentiation of a base to a power with a modulo
    :param a:
    :param power:
    :param modulo:
    :return:
    """
    result = 1

    while power > 0:
        if (power & 1) == 1:
            result = (result * a) % modulo

        power //= 2
        a = (a * a) % modulo

    return result


def products(el: list) -> list:
    """
    Generates all possible multiplication combinations of given numbers
    :param el: List of numbers
    :return: List of the combinations
    """

    result = []
    bit_size = len(el)
    for i in range(2 ** bit_size):
        cur_num = 1
        for j in range(bit_size):
            if i & (1 << j):  # If the bit is on for this position then multiply by the number at that index
                cur_num *= el[j]

        result.append(int(cur_num))

    return result


def gcd_extended(a: int, b: int) -> list:
    """
    Calculates the greatest common divisor of a and b and gives the bezout coefficients
    :param a:
    :param b:
    :return:
    """
    # Bezout coefficients
    u_prev = v = 1
    v_prev = u = 0
    round_nb = 1

    while True:
        quotient, remains = divmod(a, b)

        if remains == 0:
            if round_nb & 1:
                return [b, -u, v]
            return [b, u, -v]

        # updating coefficients
        u_tmp = u
        v_tmp = v
        u = u * quotient + u_prev
        v = v * quotient + v_prev
        u_prev = u_tmp
        v_prev = v_tmp

        # updating remains
        a = b
        b = remains

        # Increment round number
        round_nb += 1


def gcd(a: int, b: int) -> int:
    """
    Calculates the greatest common divisor of a and b
    :param a:
    :param b:
    :return:
    """
    while True:
        quotient, remains = divmod(a, b)
        if remains == 0:
            return b

        # updating remains
        a = b
        b = remains


def inverse(a: int, b: int) -> int:
    """
    Calculates the modular inverse of a in b
    :param a:
    :param b:
    :return:
    """
    _, inv, _ = gcd_extended(a, b)
    return inv % b
