from fastapi import HTTPException


class AlreadyExistError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail=f"User with this data already exists")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")