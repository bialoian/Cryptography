from app.blockchain.blockchain.wallet import Wallet
from app.blockchain.signature.rsa import RSASignature


class Transaction:
    def __init__(self, sender: Wallet = None, recipient: Wallet = None, amount: int = None, transaction_str: str = None):
        if transaction_str is not None:
            transaction_elems = transaction_str.split(' ')
            self.__sender = Wallet(transaction_elems[0].lstrip('{') + '_wallet.txt')
            self.__recipient = Wallet(transaction_elems[2] + '_wallet.txt')
            self.__amount = int(transaction_elems[4].rstrip('}'))
            self.__signature = transaction_elems[-1]
        else:
            self.__sender = sender
            self.__recipient = recipient
            self.__amount = amount
            self.__signature = self.__sender.execute_transaction(recipient, amount)

    def verify(self) -> bool:
        valid = RSASignature.verify(self.__sender.user + self.__recipient.user + str(self.__amount),
                                    self.__signature,
                                    self.__sender.public_key)
        return valid

    @property
    def sender(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient

    @property
    def amount(self):
        return self.__amount

    def __str__(self):
        return '{' + self.__sender.user + ' -> ' + self.__recipient.user + ' :: ' + str(self.__amount) + '} -> ' + self.__signature
