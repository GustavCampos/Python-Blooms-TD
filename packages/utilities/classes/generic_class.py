class GenericClass:
    def __init__(self, dictionary: dict) -> None:
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])