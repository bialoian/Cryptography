import os
from os import path
from typing import Optional

from app.blockchain.blockchain.block import Block
from app.blockchain.blockchain.transaction import Transaction
from app.blockchain.blockchain.wallet import Wallet
from app.hashes.hash.sponge_hash import SpongeHash
from app.utils.file_manager import read_file, write_file

path_data = path.join(path.abspath(path.dirname(__file__)), '../../../data/')


class BlockChain:
    def __init__(self, blockchain_file: str = None, satoshi_nakamoto: str = None):
        """
        Creates a new or loads an existing blockchain
        :param blockchain_file:
        :param satoshi_nakamoto: Genesis block miner
        """
        self.__blocks = []
        self.__pending_transactions = []

        if blockchain_file is None:
            blockchain_file = 'blockchain.txt'  # Default blockchain file

        self.__blockchain_file = blockchain_file

        if path.exists(path.join(path_data, blockchain_file)):
            # Load blockchain
            self.__load_blockchain(blockchain_file)
            self.__load_pending_transactions()

        else:  # The blockchain file does not exist
            # Create a new blockchain

            # Create a genesis block
            if satoshi_nakamoto is None:
                satoshi_nakamoto = input('Mineur du block genesis : ')
            genesis_block = Block(index=0, transactions=[], previous_hash=SpongeHash().hash('The Times 03/Jan/2009 '
                                                                                            'Chancellor on brink of '
                                                                                            'second bailout for '
                                                                                            'banks.'),
                                  miner=satoshi_nakamoto)
            self.__blocks.append(genesis_block)
            self.__save_blockchain()

    def __load_blockchain(self, blockchain_file: str):
        """
        Load a blockchain from a filename
        :param blockchain_file:
        :return:
        """
        blockchain_blocks_text = read_file(path.join(path_data, blockchain_file)).split('\n\n')

        for bc_block_text in blockchain_blocks_text:
            if bc_block_text != '':
                self.__blocks.append(Block(block_str=bc_block_text))

    def __save_blockchain(self):
        """
        Save the current blockchain to a file
        :return:
        """
        blockchain_text = ''
        for block in self.__blocks:
            blockchain_text += str(block)
        write_file(path.join(path_data, self.__blockchain_file), blockchain_text)

    def add_transaction(self, user_sender: str, user_recipient: str, amount: int) -> Optional[Transaction]:
        """
        Adds a transaction to the blockchain pending transactions
        :param user_sender:
        :param user_recipient:
        :param amount:
        :return: Return the transaction if it is possible
        """
        sender = Wallet(wallet_filename=user_sender + '_wallet.txt')

        # Check if the given amount makes sense
        if amount < 1:
            return None

        # Check if the sender as enough currency
        if self.__get_user_currency(sender) < amount:
            return None

        recipient = Wallet(wallet_filename=user_recipient + '_wallet.txt')
        self.__pending_transactions.append(Transaction(sender, recipient, amount))
        self.__save_pending_transactions()
        return self.__pending_transactions[-1]

    def verify_transaction(self, transaction_nb: int) -> (Transaction, bool):
        """
        Checks the validity of the signature of the nth transaction of the blockchain
        :param transaction_nb:
        :return:
        """
        trans_count = 0
        for block in self.__blocks:
            if len(block.transactions) + trans_count < transaction_nb:
                trans_count += len(block.transactions)
            else:
                return block.transactions[transaction_nb - trans_count - 1], \
                       block.transactions[transaction_nb - trans_count - 1].verify()

        if len(self.__pending_transactions) + trans_count >= transaction_nb:
            return self.__pending_transactions[transaction_nb - trans_count - 1], \
                   self.__pending_transactions[transaction_nb - trans_count - 1].verify()
        return None, False

    def __save_pending_transactions(self):
        """
        Saves the pending transactions in a file
        :return:
        """
        if len(self.__pending_transactions):
            trans_text = ''
            for trans in self.__pending_transactions:
                trans_text += str(trans) + '\n'

            write_file(path.join(path_data, 'pending_transactions_' + self.__blockchain_file), trans_text)
        else:  # No pending transactions -> delete the file
            if path.exists(path.join(path_data, 'pending_transactions_' + self.__blockchain_file)):
                os.remove(path.join(path_data, 'pending_transactions_' + self.__blockchain_file))

    def __load_pending_transactions(self):
        """
        Loads the pending transactions from a file
        :return:
        """
        path_transactions = path.join(path_data, 'pending_transactions_' + self.__blockchain_file)

        if path.exists(path_transactions):
            trans_lines = read_file(path_transactions).splitlines()
            for trans_text in trans_lines:
                self.__pending_transactions.append(Transaction(transaction_str=trans_text))

    def create_block(self, user: str) -> Optional[Block]:
        """
        Creates a new block with the pending transactions
        :return:
        """

        if not path.exists(path.join(path_data, 'wallets/' + user + '_wallet.txt')):
            print("Le mineur n'a pas de wallet !")
            return None

        if len(self.__pending_transactions) == 0:
            print("Pas de transactions en attente pour créer un nouveau block")
            return None

        # Create a new block
        self.__blocks.append(Block(len(self.__blocks), self.__pending_transactions, self.__blocks[-1].hash(), miner=user))
        self.__pending_transactions = []  # Remove the inserted transactions
        self.__save_blockchain()
        self.__save_pending_transactions()
        return self.__blocks[-1]

    def print_cli(self):
        """
        Prints the current status of the blockchain
        :return:
        """
        str_print = 'Blockchain (' + self.__blockchain_file + ')\n\n'

        # Blocks
        trans_count = 1
        for block in self.__blocks:
            str_print += '___________________________________________\n'
            str_print += 'Block ' + str(block.index) + ' (' + str(len(block.transactions)) + ' transactions)\n'
            if len(block.transactions):
                str_print += 'Transactions:\n'
            for trans in block.transactions:
                str_print += str(trans_count) + ': ' + str(trans) + '\n'
                trans_count += 1

            str_print += 'Date          : ' + str(block.timestamp) + '\n'
            str_print += 'Miner         : ' + block.miner + '\n'
            str_print += 'Hash précédent: ' + block.previous_hash + '\n'
            str_print += 'Salt          : ' + block.proof + '\n'
            str_print += '___________________________________________\n'

        # Pending transactions
        if len(self.__pending_transactions):
            str_print += 'Transactions en attente :\n'
            for trans in self.__pending_transactions:
                str_print += str(trans_count) + ': ' + str(trans) + '\n'
                trans_count += 1

        print(str_print)

    def __get_user_currency(self, user: Wallet) -> int:
        """
        Calculates the given user currency in the blockchain
        :param user:
        :return:
        """
        user_currency = 0

        # Check in the blockchain
        for block in self.__blocks:
            # Reward for the mined block
            if block.miner == user.user:
                user_currency += block.miner_reward

            # Check user transactions
            for transaction in block.transactions:
                if transaction.sender.user == user.user:  # User sent currency
                    user_currency -= transaction.amount
                elif transaction.recipient.user == user.user:  # User received currency
                    user_currency += transaction.amount

        # Take into account the pending transactions
        for transaction in self.__pending_transactions:
            if transaction.sender.user == user.user:
                user_currency -= transaction.amount
            elif transaction.recipient.user == user.user:
                user_currency += transaction.amount

        return user_currency

    def check_integrity(self, verbose: bool = True) -> bool:
        """
        Checks the integrity of the blockchain
        :param verbose:
        :return:
        """
        integrity = True

        # Check genesis block
        if self.__blocks[0].hash().endswith('0' * Block.proof_complexity):
            if verbose:
                print("Hash du bloc genesis correspond à la preuve de travail requise :")
                print(self.__blocks[0].hash())
        else:
            integrity = False
            if verbose:
                print("!!! Hash du bloc genesis ne correspond pas à la preuve de travail requise :")
                print(self.__blocks[0].hash())

        # Check the other blocks
        for i in range(1, len(self.__blocks)):

            # Check if block i - 1 hash matches block i previous hash
            if self.__blocks[i].previous_hash == self.__blocks[i - 1].hash():
                if verbose:
                    print("Hash du bloc " + str(i - 1) + " correspond au hash précédent du bloc " + str(i))
            else:
                integrity = False
                if verbose:
                    print("!!! Hash du bloc " + str(i - 1) + " ne correspond pas au hash précédent du bloc " +
                          str(i) + ":")
                    print(str(self.__blocks[i - 1]))

            # Check if block i starts with n zeros
            if self.__blocks[i].hash().endswith('0' * Block.proof_complexity):
                if verbose:
                    print("Hash du bloc " + str(i) + " correspond à la preuve de travail requise :")
                    print(str(self.__blocks[i]))
            else:
                integrity = False
                if verbose:
                    print("!!! Hash du bloc " + str(i) + " ne correspond pas à la preuve de travail requise :")
                    print(str(self.__blocks[i]))

            # Check transactions of the block
            for transaction in self.__blocks[i].transactions:
                if not transaction.verify():
                    integrity = False
                    if verbose:
                        print('La transaction suivante a été altérée :')
                        print(str(transaction))

        return integrity

    def users_wallets(self):
        """
        Gives a dictionary of the users and the currency in their wallets
        :return:
        """
        users = {}

        for block in self.__blocks:
            # Miners reward
            if block.miner not in users.keys():
                users[block.miner] = 0
            users[block.miner] = users.get(block.miner) + Block.miner_reward

            # Transactions in blocks
            for trans in block.transactions:
                if trans.sender.user not in users.keys():
                    users[trans.sender.user] = 0
                users[trans.sender.user] = users.get(trans.sender.user) - trans.amount

                if trans.recipient.user not in users.keys():
                    users[trans.recipient.user] = 0
                users[trans.recipient.user] = users.get(trans.recipient.user) + trans.amount

        # Pending transactions
        for trans in self.__pending_transactions:
            if trans.sender.user not in users.keys():
                users[trans.sender.user] = 0
            users[trans.sender.user] = users.get(trans.sender.user) - trans.amount

            if trans.recipient.user not in users.keys():
                users[trans.recipient.user] = 0
            users[trans.recipient.user] = users.get(trans.recipient.user) + trans.amount

        return users

