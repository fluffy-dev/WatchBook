from typing import List

from src.apps.user.dependencies.repository import IUserRepository, IUserPropertyRepository
from src.apps.user.dto import (
    UserDTO,
    UpdateUserDTO,
    FindUserDTO,
    UserProfileDTO,
    UpdateUserPropertyDTO,
    UserPropertyDTO
)
from src.apps.user.entity import UserEntity, UserPropertyEntity


class UserService:
    def __init__(self, user_repository: IUserRepository, user_property_repository: IUserPropertyRepository):
        self.user_repository = user_repository
        self.user_property_repository = user_property_repository

    async def create_user(self, user_entity: UserEntity) -> UserDTO:
        """

        Function to create a new user.

        UserEntity:
            #. name: str.
            #. email: str.
            #. login: str.
            #. password: str.

        :param user_entity: UserEntity

        UserDTO:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: UserDTO

        :raises AnyException: from repository
        """
        return await self.user_repository.create(user_entity)

    async def update_user(self, dto: UpdateUserDTO) -> UserDTO:
        """
        Function to  update a user via UpdateUserDTO.

        UpdateUserDTO fields:
            #. name: str.
            #. login: str.


        :param dto: UpdateUserDTO

        UserDTO fields:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: UserDTO

        :raises AnyException: from repository
        """
        return await self.user_repository.update(dto)

    async def delete_user(self, pk: int) -> None:
        """
        Function to  delete a user via FindUserDTO.

        :param pk:
        :return:

        :raises AnyException: from repository
        """
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


    async def create_property(self, property_entity: UserPropertyEntity) -> UserPropertyDTO:
        return await self.user_property_repository.create(property_entity)

    async def update_property(self, dto: UpdateUserPropertyDTO):
        return await self.user_property_repository.update(dto)

    async def delete_property(self, pk: int) -> None:
        await self.user_property_repository.delete(pk)