from os import path

from app.blockchain.signature.rsa import RSASignature
from app.keys_generator.keys_manager.rsa_keys import RSAKeysManager
from app.utils.file_manager import read_file, write_file

path_data = path.join(path.abspath(path.dirname(__file__)), '../../../data/')
path_wallet = path.join(path_data, 'wallets/')
path_keys = path.join(path_data, 'keys/')
path_public = path.join(path_keys, 'public/')
path_private = path.join(path_keys, 'private/')


class Wallet:
    def __init__(self, wallet_filename: str = None):

        if path.exists(path.join(path_wallet, wallet_filename)):  # Load user wallet from file
            wallet_lines = read_file(path.join(path_wallet, wallet_filename)).splitlines()
            self.__user = wallet_lines[0]
            self.__keys_filename = wallet_lines[1]

            self.__keys_mngr = RSAKeysManager(self.__keys_filename)
        else:  # Create user wallet from keys
            keys_filename = 'key_' + wallet_filename.split('_')[0] + '.txt'
            self.__keys_mngr = RSAKeysManager(keys_filename)
            self.__user = keys_filename.split('.')[0].split('_')[1]  # Use filename as username
            self.__keys_filename = keys_filename

            # Checks if user already exists
            if path.exists(path.join(path_wallet, self.__user + '_wallet.txt')):
                raise Exception("Le wallet de cet utilisateur existe déjà")

            self.__save()  # Write the new wallet file

    def execute_transaction(self, recipient: "Wallet", amount: int) -> str:
        """
        Signs a transaction
        :param recipient:
        :param amount: The amount of currency the sender will give and the recipient will receive
        :return: Signature of the transaction
        """

        # Sign the transaction
        rsa_signer = RSASignature(self.__keys_mngr)
        trans_signature = rsa_signer.sign(self.__user + recipient.user + str(amount))

        self.__save()

        return trans_signature

    def __save(self):
        """
        Saves the Wallet into a file
        :return:
        """

        write_file(path.join(path_wallet, self.__user + '_wallet.txt'),
                   self.__user + '\n'
                   + self.__keys_filename)

    @property
    def user(self):
        return self.__user

    @property
    def public_key(self):
        return self.__keys_mngr.get_public()
