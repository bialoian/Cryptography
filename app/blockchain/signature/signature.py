import abc


class Signature(abc.ABC):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'sign') and
                callable(subclass.sign) or
                NotImplemented)

    @abc.abstractmethod
    def sign(self, message: str):
        """
        Signs the message
        :param message:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def verify(message: str, signature, public_key):
        """
        Checks if the signature is valid
        :param message:
        :param signature:
        :param public_key:
        :return:
        """
        raise NotImplementedError
