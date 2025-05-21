from fastapi import Depends
from typing import Annotated


from src.user.repositories.user_property import UserPropertyRepository
from src.user.repositories.user import UserRepository


IUserRepository = Annotated[UserRepository, Depends()]
IUserPropertyRepository = Annotated[UserPropertyRepository, Depends()]

