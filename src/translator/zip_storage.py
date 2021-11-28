class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OperatorsStorage(dict, metaclass=Singleton):
    pass


class DependenceStorage(dict, metaclass=Singleton):
    """
    id of DMN node to related tables
    """
    pass


class InputDataStorage(dict, metaclass=Singleton):
    pass
