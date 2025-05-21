from src.libs.exceptions import AlreadyExists, NotFound


class UserAlreadyExist(AlreadyExists):
    pass

class UserNotFound(NotFound):
    pass

class UserPropertyNotFound(NotFound):
    pass

class UserPropertyCreationError(Exception):
    pass

