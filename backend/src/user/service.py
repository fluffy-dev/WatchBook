from typing import List

from src.libs.exceptions import PaginationError
from src.user.dependencies.repository import IUserRepository, UserRepository
from src.user.dto import (
    UserDTO,
    UpdateUserDTO,
    FindUserDTO,
    UserProfileDTO,
    UpdateUserPropertyDTO,
    UserPropertyDTO
)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.repository: UserRepository = user_repository

    async def create(self, dto: UserDTO) -> UserDTO:
        return await self.repository.create(dto)

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        return await self.repository.update(dto, pk)

    async def find(self, dto: FindUserDTO) -> UserDTO:
        return await self.repository.find(dto)

    async def get(self, pk: int) -> UserDTO:
        return await self.repository.get(pk)

    async def get_list(self, limit: int = None, offset: int = None) -> List[UserDTO]:
        if limit < 0 or offset < 0:
            raise PaginationError("Limit and offset must be positive")

        return await self.repository.get_list(limit, offset)

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        return await self.repository.update_password(new_password, pk)




