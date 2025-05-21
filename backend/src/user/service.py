from typing import List

from src.libs.exceptions import PaginationError
from src.user.dependencies.repository import IUserRepository, UserRepository
from src.user.dto import (
    UserDTO,
    UpdateUserDTO,
    FindUserDTO,
    PublicUserDTO,
    PrivateUserDTO,
)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.repository: UserRepository = user_repository

    async def create(self, dto: UserDTO) -> UserDTO:
        """
        Create a new user by UserDTO,

        this function shouldn't be used in API, only via other higher layer services, cause of insecurity

        Args:
            dto: UserDTO (without id)

        Returns:
            UserDTO
        """
        return await self.repository.create(dto)

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        """
        Update a user by UpdateUserDTO and primary key

        this function shouldn't be used in API, only via other higher layer services, cause of insecurity

        Args:
            dto: UpdateUserDTO
            pk: Primary key integer

        Returns:
             UserDTO
        """
        return await self.repository.update(dto, pk)

    async def find(self, dto: FindUserDTO) -> UserDTO:
        """
        Find user by FindUserDTO fields match

        this function shouldn't be used in API, only via other higher layer services, cause of insecurity

        Args:
            dto: FindUserDTO

        Returns:
            UserDTO
        """
        return await self.repository.find(dto)

    async def get_private(self, pk: int) -> PrivateUserDTO:
        """
        Get the user private data by primary key

        uses to get user personal profile or data, not the public one

        Args:
            pk: Primary key integer

        Returns:
            PrivateUserDTO
        """
        raw_data = await self.repository.get(pk)

        return PrivateUserDTO(
            name=raw_data.name,
            login=raw_data.login,
            email=raw_data.email
        )

    async def get(self, pk: int) -> PublicUserDTO:
        """
        Get the user public data by primary key

        uses to get user public profiles or data

        Args:
            pk: Primary key integer

        Returns:
            PublicUserDTO
        """
        raw_data = await self.repository.get(pk)
        return PublicUserDTO(
            name=raw_data.name
        )

    async def get_list(self, limit: int = None, offset: int = None) -> List[PublicUserDTO]:
        """
        Get the list of users public data

        uses to show list of other user public profiles

        Args:
            limit: the number of users to show
            offset: the number of users to skip

        Returns:
            List[PublicUserDTO]
        """
        if limit < 0 or offset < 0:
            raise PaginationError("Limit and offset must be positive")

        raw_data_list = await self.repository.get_list(limit, offset)
        return [PublicUserDTO(name=raw_data.name) for raw_data in raw_data_list]

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        """
        Change the password for the user by primary key

        this function shouldn't be used in API, only via other higher layer services, cause of insecurity

        Args:
            new_password: new user password
            pk: id of the user

        Returns:
            UserDTO
        """
        return await self.repository.update_password(new_password, pk)




