import abc


class KeysManager(abc.ABC):
    """
    Manages a public / private key pair
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_public') and
                callable(subclass.get_public) and
                hasattr(subclass, 'get_public_key') and
                callable(subclass.get_public_key) and
                hasattr(subclass, 'get_private_key') and
                callable(subclass.get_private_key) or
                NotImplemented)

    @abc.abstractmethod
    def get_public(self):
        """
        Gives the public elements of the keys
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_public_key(self):
        """
        Gives the public key
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_private_key(self):
        """
        Gives the private key
        :return:
        """
        raise NotImplementedError
