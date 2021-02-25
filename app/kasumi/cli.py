from app.kasumi.cipher_mode.cbc import CBC
from app.kasumi.cipher_mode.cfb import CFB
from app.kasumi.cipher_mode.ctr import CTR
from app.kasumi.cipher_mode.gcm import GCM
from app.kasumi.cipher_mode.ofb import OFB
from app.kasumi.cipher_mode.ecb import ECB
from app.kasumi.cipher_mode.pcbc import PCBC
from app.kasumi.kasumi import Kasumi
from os import path
from app.utils.file_manager import file_loader, add_to_filename, write_file, read_file

path_data = path.join(path.abspath(path.dirname(__file__)), '../../data/')
path_keys = path.join(path_data, 'keys/')
path_ivs = path.join(path_data, 'iv/')

available_ciphermodes = {
    "ECB": ECB,
    "CBC": CBC,
    "PCBC": PCBC,
    "CFB": CFB,
    "OFB": OFB,
    "CTR": CTR,
    "GCM": GCM,
}


def encrypt():
    """
    CLI to encrypt a file using Kasumi
    :return:
    """

    # Message
    message, filename, q_pressed = file_loader("Fichier du dossier data à chiffrer (kasumi.txt par défaut) :",
                                               "kasumi.txt",
                                               path_data)
    if q_pressed:
        return

    # Key (128 bits in hexadecimal)
    key, _, q_pressed = file_loader("Clé du dossier data/keys à utiliser (kasumi_key.txt par défaut) :",
                                    "kasumi_key.txt",
                                    path_keys)
    if q_pressed:
        return

    # Cipher mode
    cipher_name, q_pressed = _get_cipher_name()
    if q_pressed:
        return

    # Initialization vector (64 bits in hexadecimal)
    iv, _, q_pressed = file_loader("Vecteur d'initialisation du dossier data/iv à utiliser (iv.txt par défaut, "
                                   "entrée pour ECB) :",
                                   "iv.txt",
                                   path_ivs)

    # Creates cipher the desired cipher mode
    cipher_mode = available_ciphermodes.get(cipher_name)
    cipher = cipher_mode(Kasumi())

    encrypted = cipher.encrypt(message, key, iv)

    # Add '-encrypted' to the filename
    filename = add_to_filename(filename, '-encrypted')

    write_file(path.join(path_data, filename), encrypted)

    print('Chiffré :')
    print(encrypted)


def decrypt():
    """
    CLI to decrypt a file using Kasumi
    :return:
    """

    # Message
    message, filename, q_pressed = file_loader(
        "Fichier du dossier data à déchiffrer (kasumi-encrypted.txt par défaut) :",
        "kasumi-encrypted.txt",
        path_data
    )
    if q_pressed:
        return

    # Key
    key, _, q_pressed = file_loader("Clé du dossier data/keys à utiliser (kasumi_key.txt par défaut) :",
                                    "kasumi_key.txt",
                                    path_keys)
    if q_pressed:
        return

    # Cipher mode
    cipher_name, q_pressed = _get_cipher_name()
    if q_pressed:
        return

    # Initialization vector (64 bits in hexadecimal)
    iv, _, q_pressed = file_loader("Vecteur d'initialisation du dossier data/iv à utiliser (iv.txt par défaut, "
                                   "entrée pour ECB) :",
                                   "iv.txt",
                                   path_ivs)

    # Creates cipher the desired cipher mode
    cipher_mode = available_ciphermodes.get(cipher_name)
    cipher = cipher_mode(Kasumi())

    decrypted = cipher.decrypt(message, key, iv)

    # Add '-decrypted' to the filename
    filename = add_to_filename(filename, '-decrypted')

    write_file(path.join(path_data, filename), decrypted)

    print('Déchiffré :')
    print(decrypted)


def all():
    """
    Does all the possible actions in Kasumi
    :return:
    """

    print('Kasumi\n')

    cleartext = read_file(path.join(path_data, "kasumi.txt"))
    key = read_file(path.join(path_keys, "kasumi_key.txt"))
    iv = read_file(path.join(path_ivs, "iv.txt"))
    kasumi = Kasumi()

    # ECB
    ecb = ECB(kasumi)
    if ecb.decrypt(ecb.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi ECB\n')
    else:
        print('ECB ok!\n')

    # CBC
    cbc = CBC(kasumi)
    if cbc.decrypt(cbc.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi CBC\n')
    else:
        print('CBC ok!\n')

    # PCBC
    pcbc = PCBC(kasumi)
    if pcbc.decrypt(pcbc.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi PCBC\n')
    else:
        print('PCBC ok!\n')

    # CFB
    cfb = CFB(kasumi)
    if cfb.decrypt(cfb.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi CFB\n')
    else:
        print('CFB ok!\n')

    # OFB
    ofb = OFB(kasumi)
    if ofb.decrypt(ofb.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi OFB\n')
    else:
        print('OFB ok!\n')

    # CTR
    ctr = CTR(kasumi)
    if ctr.decrypt(ctr.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi CTR\n')
    else:
        print('CTR ok!\n')

    # GCM
    gcm = GCM(kasumi)
    if gcm.decrypt(gcm.encrypt(cleartext, key, iv), key, iv) != cleartext:
        print('Erreur Kasumi GCM\n')
    else:
        print('GCM ok!\n')


def _get_cipher_name() -> (str, bool):
    """
    Get the desired cipher name from the user input
    :return: cipher name and quit boolean
    """
    cipher_name = None
    while True:
        print("Mode de chiffrement à utiliser (ECB (défaut), CBC, PCBC, CFB, OFB, CTR, GCM) :")
        cipher_name = input().upper()
        if cipher_name == 'q':
            return '', True

        if len(cipher_name) == 0:
            cipher_name = 'ECB'

        if cipher_name in available_ciphermodes:
            break
        else:
            print("Ce mode de chiffrement n'est pas dans la liste")

    return cipher_name, False
