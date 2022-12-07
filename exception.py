class ValueNotInDB(ValueError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Value <{self.value}> not in DB"


class ValueAlreadyInDB(ValueError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Value <{self.value}> already in DB"
