from typing import List

from src.user.dependencies.repository import IUserRepository, IUserPropertyRepository
from src.user.dto import (
    UserDTO,
    UpdateUserDTO,
    FindUserDTO,
    UserProfileDTO,
    UpdateUserPropertyDTO,
    UserPropertyDTO
)
from src.user.entity import UserEntity, UserPropertyEntity


class UserService:
    def __init__(self, user_repository: IUserRepository, user_property_repository: IUserPropertyRepository):
        self.user_repository = user_repository
        self.user_property_repository = user_property_repository

    async def create_user(self, user_entity: UserEntity) -> UserDTO:
        return await self.user_repository.create(user_entity)

    async def update_user(self, dto: UpdateUserDTO) -> UserDTO:
        return await self.user_repository.update(dto)

    async def delete_user(self, pk: int) -> None:
        await self.user_repository.delete(pk)

    async def list_users(self, limit: int = None, offset: int = None) -> List[UserDTO]:
        return await self.user_repository.get_list(limit, offset)

    async def get_user_profile(self, dto: FindUserDTO) -> UserProfileDTO:
        user = await self.user_repository.get_user(dto)
        user.password = None

        user_properties = await self.user_property_repository.get_properties(user.id)

        user_profile = UserProfileDTO(**user.model_dump(exclude_none=True))
        user_profile.properties = user_properties

        return user_profile


