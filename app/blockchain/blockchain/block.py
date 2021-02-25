from datetime import datetime

from app.blockchain.blockchain.transaction import Transaction
from app.hashes.hash.sponge_hash import SpongeHash
from app.keys_generator.xorshift import XORShift


class Block:

    proof_complexity = 3
    miner_reward = 10
    proof_bitsize = 128

    def __init__(self, index: int = None, transactions: list = None, previous_hash: str = None, timestamp: datetime = datetime.now(), miner: str = None, block_str: str = None):

        self.__xorshift = XORShift()
        self.__hash = SpongeHash()

        if block_str is not None:
            # Create a block from string
            self.__transactions = []

            block_lines = block_str.splitlines()
            self.__index = int(block_lines[0].split(' ')[1])

            # Add transactions
            for trans_str in block_lines[1:-4]:
                self.__transactions.append(Transaction(transaction_str=trans_str))

            self.__timestamp = datetime.strptime(block_lines[-4], '%Y-%m-%d %H:%M:%S.%f')
            self.__miner = block_lines[-3]
            self.__previous_hash = block_lines[-2]
            self.__proof = block_lines[-1]
        else:
            # Create a block from parameters
            self.__index = index
            self.__transactions = transactions
            self.__previous_hash = previous_hash
            self.__timestamp = timestamp
            self.__miner = miner
            self.__proof = None
            self.__create_proof()

    def hash(self) -> str:
        block_str = ''
        for transaction in self.__transactions:
            block_str += str(transaction)
        block_str += self.__previous_hash
        block_str += self.__proof
        return self.__hash.hash(block_str)

    @property
    def index(self):
        return self.__index

    @property
    def transactions(self):
        return self.__transactions

    @property
    def previous_hash(self):
        return self.__previous_hash

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def miner(self):
        return self.__miner

    @property
    def proof(self):
        return self.__proof

    def __str__(self) -> str:
        block_str = 'block ' + str(self.__index) + '\n'
        for transaction in self.__transactions:
            block_str += str(transaction) + '\n'

        block_str += str(self.__timestamp) + '\n'
        block_str += self.__miner + '\n'
        block_str += self.__previous_hash + '\n'
        block_str += self.__proof + '\n\n'
        return block_str

    def __create_proof(self):
        """
        Creates a proof of work for the block
        :return:
        """

        # Create the block base on which the salt will be concatenated
        base_block_str = ''
        for transaction in self.__transactions:
            base_block_str += str(transaction)
        base_block_str += self.__previous_hash

        # Find a salt that creates the right hash
        while True:
            guess_salt = hex(self.__xorshift.getrandbits(self.proof_bitsize)).lstrip('0x')
            guess = base_block_str + guess_salt
            hash_try = self.__hash.hash(guess)

            if hash_try.endswith('0' * self.proof_complexity):
                self.__proof = guess_salt
                return
