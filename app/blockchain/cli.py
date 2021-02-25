import os
from os import path

from app.blockchain.blockchain.blockchain import BlockChain
from app.blockchain.signature.elgamal import ElGamalSignature
from app.blockchain.signature.rsa import RSASignature
from app.keys_generator.keys_manager.elgamal_keys import ElGamalKeysManager
from app.keys_generator.keys_manager.rsa_keys import RSAKeysManager
from app.utils.file_manager import read_file

path_data = path.join(path.abspath(path.dirname(__file__)), '../../data/')
path_primes = path.join(path_data, 'primes/')


def create_proof_of_work():
    """
    CLI to add a new block to the blockchain
    :return:
    """
    blockchain = BlockChain()
    blockchain.print_cli()
    miner = input('Nom du mineur du bloc : ')
    print("Création d'un nouveau bloc...")
    new_block = blockchain.create_block(miner)
    if new_block is None:
        print('Création de bloc annulée')
    else:
        print("Bloc créé :")
        print(str(new_block))


def check_transaction():
    """
    CLI to check the validity of a transaction
    :return:
    """
    blockchain = BlockChain()
    blockchain.print_cli()

    print("Vérification d'une transaction")
    trans_nb = input("Numéro de la transaction à vérifier : ")
    if trans_nb == 'q':
        return

    trans_nb = int(trans_nb)
    transaction, validated = blockchain.verify_transaction(trans_nb)

    if transaction is None:
        print("La transaction n'existe pas")
        return

    print(transaction)
    if validated:
        print('Cette transaction est valide')
    else:
        print('La transaction a été altérée')


def increment():
    """
    CLI to create a new transaction
    :return:
    """
    blockchain = BlockChain()
    blockchain.print_cli()

    print("\nAjout d'une transaction")
    user_sender = input("Utilisateur à débiter : ")
    if user_sender == 'q':
        return

    user_recipient = input("Utilisateur à créditer : ")
    if user_recipient == 'q':
        return

    amount = input("Montant : ")
    if amount == 'q':
        return

    amount = int(amount)
    transaction = blockchain.add_transaction(user_sender, user_recipient, amount)

    if transaction is None:
        print("La transaction n'a pas pu être effectuée, montant invalide ou fonds insuffisants")
    else:
        print("La transaction suivante a été ajoutée aux transactions en attente :")
        print(transaction)


def check_integrity():
    """
    CLI to check blockchain integrity
    :return:
    """
    blockchain = BlockChain()
    blockchain.print_cli()
    print("Vérification de l'intégrité de la blockchain")
    integrity = blockchain.check_integrity()

    if integrity:
        print("La blockchain est intègre!")
    else:
        print("La blockchain n'est pas intègre!")


def print_blockchain():
    """
    Prints the actual blockchain state
    :return:
    """
    blockchain = BlockChain()
    blockchain.print_cli()


def users_wallets():
    """
    Print the users and the amount of cryptocurrency they have
    :return:
    """
    blockchain = BlockChain()
    u_wallets = blockchain.users_wallets()

    print("Wallets des utilisateurs :")
    for user in u_wallets:
        print(user, ' : ', str(u_wallets[user]))


def all():
    message = read_file(path.join(path_data, 'test.txt'))

    print("Vérification du fonctionnement des signatures")
    print('Signature ElGamal')
    print('Message à signer :\n' + message)
    # Check ElGamal signature
    k_manager = ElGamalKeysManager('key_alice.txt')
    elgamal_sign = ElGamalSignature(k_manager)
    signed_msg_elgamal = elgamal_sign.sign(message)
    print('Message signé\n' + 's1: ' + signed_msg_elgamal[0] + '\ns2: ' + signed_msg_elgamal[1])
    print('Signature valide ? : ' + str(ElGamalSignature.verify(message, signed_msg_elgamal, k_manager.get_public())))

    # Check RSA signature
    print('Signature RSA')
    k_manager = RSAKeysManager('key_rsa_default.txt')
    rsa_sign = RSASignature(k_manager)
    signed_msg_rsa = rsa_sign.sign(message)
    print('Message signé\n' + signed_msg_rsa)
    print('Signature valide ? : ' + str(RSASignature.verify(message, signed_msg_rsa, k_manager.get_public())))

    # Blockchain tests

    print('\nVérification du fonctionnement de la blockchain\n')
    print("Création d'une nouvelle blockchain et ajout de 2 transactions :")

    blockchain = BlockChain('blockchain_test.txt', 'jacques')
    blockchain.add_transaction('jacques', 'ian', 5)
    blockchain.add_transaction('jacques', 'remi', 5)
    blockchain.create_block('jacques')
    blockchain.print_cli()

    print('Ajout de 2 transactions en attente :')
    blockchain.add_transaction('jacques', 'ian', 1)
    blockchain.add_transaction('jacques', 'remi', 1)
    blockchain.print_cli()

    print('Affichage des wallets des utilisateurs :')
    u_wallets = blockchain.users_wallets()
    for user in u_wallets:
        print(user, ' : ', str(u_wallets[user]))

    print("\nVérification de l'intégrité de la transaction 4")
    trans, validated = blockchain.verify_transaction(4)
    if trans is None:
        print("La transaction n'existe pas")
    else:
        print(trans)
        if validated:
            print('Cette transaction est valide')
        else:
            print('La transaction a été altérée')

    print("\nVérification de l'intégrité de la blockchain :")
    blockchain.check_integrity()

    # Remove blockchain files
    os.remove(path.join(path_data, 'blockchain_test.txt'))
    os.remove(path.join(path_data, 'pending_transactions_blockchain_test.txt'))
