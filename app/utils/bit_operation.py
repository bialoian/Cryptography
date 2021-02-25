def add_mod(x: int, y: int, modulo: int = 32) -> int:
    """
    Modular addition
    :param x:
    :param y:
    :param modulo:
    :return:
    """
    return (x + y) & ((1 << modulo) - 1)


def left_circ_shift(x: int, shift: int, n_bits: int) -> int:
    """
    Does a left binary circular shift on the number x of n_bits bits
    :param x: A number
    :param shift: The number of bits to shift
    :param n_bits: The number of bits of x
    :return: The shifted result
    """
    mask = (1 << n_bits) - 1  # Trick to create a ones mask of n bits
    x_base = (x << shift) & mask  # Keep it in the n_bits range
    return x_base | (x >> (n_bits - shift))  # Add the out of bounds bits


def right_circ_shift(x: int, shift: int, n_bits: int) -> int:
    """
    Does a right binary circular shift on the number x of n_bits bits
    :param x: A number
    :param shift: The number of bits to shift
    :param n_bits: The number of bits of x
    :return: The shifted result
    """
    mask = (1 << n_bits) - 1  # Trick to create a ones mask of n bits
    x_base = x >> shift
    return x_base | (x << (n_bits - shift) & mask)


def merge_bytes(payload_list: list) -> int:
    """
    Gives an 8 bytes value from a byte list
    :param payload_list: Byte list (max size is 8)
    :return:
    """
    while len(payload_list) < 8:
        payload_list.append(0x00)

    result = payload_list[0]
    for i in range(1, 8):
        result = (result << 8) | payload_list[i]

    return result


def split_bytes(payload: int) -> bytearray:
    """
    Gives a byte list of an 8 bytes value
    :param payload: The 8 bytes value
    :return:
    """
    payload_list = bytearray()
    for i in range(8):
        payload_list.insert(0, (payload >> (8 * i)) & 0xFF)  # Extract bytes by shifting right and masking

    return payload_list
