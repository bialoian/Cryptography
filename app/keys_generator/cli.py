from app.keys_generator.keys_manager.elgamal_keys import ElGamalKeysManager
from app.keys_generator.keys_manager.rsa_keys import RSAKeysManager
from app.keys_generator.prime import Prime
from os import path

path_data = path.join(path.abspath(path.dirname(__file__)), '../../data/')
path_primes = path.join(path_data, 'primes/')


def generate_elgamal_keys():
    """
    CLI to generate an ElGamal key pair
    :return:
    """

    print("Génération d'un couple de clés ElGamal")

    # Prime number
    print("Fichier du nombre premier à utiliser. Si inexistant, il sera généré. (prime_default.txt par défaut)")
    prime_filename = input()

    if prime_filename == 'q':
        return

    if prime_filename == '':
        prime_filename = 'prime_default.txt'

    # Keys
    print("Nom des fichiers des clés publique / privée à utiliser. Si inexistant, il sera généré. (key_default.txt "
          "par défaut)")
    keys_filename = input()

    if keys_filename == 'q':
        return

    if keys_filename == '':
        keys_filename = 'key_default.txt'

    prime = Prime(path.join(path_primes, prime_filename))
    key_mngmt = ElGamalKeysManager(keys_filename, prime.get_prime(), prime.get_generator())

    print("Clé publique")
    print(key_mngmt.get_public_key())
    print("Clé privée")
    print(key_mngmt.get_private_key())


def generate_rsa_keys():
    """
    CLI to generate an RSA key pair
    :return:
    """

    print("Génération d'un couple de clés RSA")

    # Prime number p
    print("Fichier du nombre premier p à utiliser. Si inexistant, il sera généré. (prime_p.txt par défaut)")
    prime_p_filename = input()

    if prime_p_filename == 'q':
        return

    if prime_p_filename == '':
        prime_p_filename = 'prime_p.txt'

    # Prime number q
    print("Fichier du nombre premier q à utiliser. Si inexistant, il sera généré. (prime_q.txt par défaut)")
    prime_q_filename = input()

    if prime_q_filename == 'q':
        return

    if prime_q_filename == '':
        prime_q_filename = 'prime_q.txt'


    # Keys
    print("Nom des fichiers des clés publique / privée à utiliser. Si inexistant, il sera généré. (key_rsa_default.txt "
          "par défaut)")
    keys_filename = input()

    if keys_filename == 'q':
        return

    if keys_filename == '':
        keys_filename = 'key_rsa_default.txt'

    prime_p = Prime(path.join(path_primes, prime_p_filename), with_generator=False)
    prime_q = Prime(path.join(path_primes, prime_q_filename), with_generator=False)
    key_mngmt = RSAKeysManager(keys_filename, [prime_p.get_prime(), prime_q.get_prime()])

    print("Clé publique")
    print(key_mngmt.get_public_key())
    print("Clé privée")
    print(key_mngmt.get_private_key())

def dh_key_exchange():
    """
    CLI to perform a Diffie-Hellman key exchange
    :return:
    """

    # Prime number
    print("Fichier du nombre premier à utiliser. Si inexistant, il sera généré. (prime_default.txt par défaut)")
    prime_filename = input()

    if prime_filename == 'q':
        return

    if prime_filename == '':
        prime_filename = 'prime_default.txt'

    # Keys Alice
    print("Nom des fichiers des clés publique / privée d'Alice. Si inexistant, il sera généré. (key_alice.txt "
          "par défaut)")
    keys_a_filename = input()

    if keys_a_filename == 'q':
        return

    if keys_a_filename == '':
        keys_a_filename = 'key_alice.txt'

    # Keys Bob
    print("Nom des fichiers des clés publique / privée de Bob. Si inexistant, il sera généré. (key_bob.txt "
          "par défaut)")
    keys_b_filename = input()

    if keys_b_filename == 'q':
        return

    if keys_b_filename == '':
        keys_b_filename = 'key_bob.txt'

    prime = Prime(path.join(path_primes, prime_filename))
    key_mgmt_a = ElGamalKeysManager(keys_a_filename, prime.get_prime(), prime.get_generator())
    key_mgmt_b = ElGamalKeysManager(keys_b_filename, prime.get_prime(), prime.get_generator())
    shared_key_a = key_mgmt_a.generate_shared_key(key_mgmt_b.get_public_key())
    shared_key_b = key_mgmt_b.generate_shared_key(key_mgmt_a.get_public_key())

    print("Alice:")
    print("Clé publique : ", key_mgmt_a.get_public_key())
    print("Clé privée : ", key_mgmt_a.get_private_key())
    print("Clé secrète partagée : ", shared_key_a)

    print("\nBob:")
    print("Clé publique : ", key_mgmt_b.get_public_key())
    print("Clé privée : ", key_mgmt_b.get_private_key())
    print("Clé secrète partagée : ", shared_key_b)

    if shared_key_a == shared_key_b:
        print("\nLes clés secrètes sont égales!")
    else:
        print("\nLes clés secrètes ne correspondent pas!")


available_cmds = {
    1: generate_elgamal_keys,
    2: generate_rsa_keys,
    3: dh_key_exchange
}


def generate_keys():
    """
    CLI to choose which action to do in Keys generator
    :return:
    """
    while True:
        print("Génération de couples de clés publiques / privées")
        print("->1<- Générer un couple de clés ElGamal")
        print("->2<- Générer un couple de clés RSA")
        print("->3<- Partage de clé privé Diffie-Hellman")
        cmd = input()

        if cmd == 'q':
            break

        cmd_nb = 0
        try:
            cmd_nb = int(cmd)
        except ValueError:
            print('La commande entrée doit être un nombre')

        if cmd_nb in available_cmds:
            func_to_run = available_cmds.get(cmd_nb)
            func_to_run()
            break
        else:
            print("La commande n'est pas disponible")


def all():
    """
    Performs all possible options of keys generator
    :return:
    """

    # Keys generation
    print("Génération d'un couple de clés ElGamal publique / privée")
    prime = Prime(path.join(path_primes, "prime_default.txt"))
    key_mngmt = ElGamalKeysManager("key_default.txt", prime.get_prime(), prime.get_generator())
    print("\nClé publique :")
    print(key_mngmt.get_public_key())
    print("Clé privée :")
    print(key_mngmt.get_private_key())

    print("\nGénération d'un couple de clés RSA publique / privée")
    prime_p = Prime(path.join(path_primes, "prime_p.txt"))
    prime_q = Prime(path.join(path_primes, "prime_q.txt"))
    key_mngmt = RSAKeysManager("key_rsa_default.txt", [prime_p.get_prime(), prime_q.get_prime()])
    print("\nClé publique :")
    print(key_mngmt.get_public_key())
    print("Clé privée :")
    print(key_mngmt.get_private_key())

    # Diffie-Hellman key exchange
    print("\nPartage de clé secrète Diffie-Hellman")
    key_mgmt_a = ElGamalKeysManager("key_alice.txt", prime.get_prime(), prime.get_generator())
    key_mgmt_b = ElGamalKeysManager("key_bob.txt", prime.get_prime(), prime.get_generator())
    shared_key_a = key_mgmt_a.generate_shared_key(key_mgmt_b.get_public_key())
    shared_key_b = key_mgmt_b.generate_shared_key(key_mgmt_a.get_public_key())

    print("Alice:")
    print("Clé publique : ", key_mgmt_a.get_public_key())
    print("Clé privée : ", key_mgmt_a.get_private_key())
    print("Clé secrète partagée : ", shared_key_a)

    print("\nBob:")
    print("Clé publique : ", key_mgmt_b.get_public_key())
    print("Clé privée : ", key_mgmt_b.get_private_key())
    print("Clé secrète partagée : ", shared_key_b)

    if shared_key_a == shared_key_b:
        print("\nLes clés secrètes sont égales!\n")
    else:
        print("\nLes clés secrètes ne correspondent pas!\n")
