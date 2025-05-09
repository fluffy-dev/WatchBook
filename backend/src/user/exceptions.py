from src.libs.exceptions import AlreadyExists, NotFound


class UserAlreadyExist(AlreadyExists):
    pass

class UserNotFound(NotFound):
    pass

class PropertyNotFound(NotFound):
    pass