class GenericBookshelfError(Exception):
    """Base Error class for Bookshelf API"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityDoesNotExistError(GenericBookshelfError):
    """Entity is not found in the Database"""

    pass
