class EntityDoesNotExistError(Exception):
    """Student entity is not found in the memory map"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityAlreadyExistsError(Exception):
    """Student entity is already found in the memory map"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
