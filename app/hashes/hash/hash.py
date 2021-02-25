import abc


class Hash(abc.ABC):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'hash') and
                callable(subclass.hash) or
                NotImplemented)

    @abc.abstractmethod
    def hash(self, message: str, to_hex: bool):
        """
        Creates a hash of the message
        :param message:
        :param to_hex:
        :return:
        """
        raise NotImplementedError
