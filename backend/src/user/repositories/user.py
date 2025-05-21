from typing import Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.user.exceptions import UserAlreadyExist, UserNotFound
from src.config.database.session import ISession
from src.user.models.user import UserModel
from src.user.dto import UpdateUserDTO, UserDTO, FindUserDTO


class UserRepository:
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, user: UserDTO) -> UserDTO:
        """
        Create a new user by UserDTO

        Args:
            user: UserDTO (without id)

        Returns:
            UserDTO

        Raises:
            UserAlreadyExist: if user with same login or email already exists in database
        """
        instance = UserModel(**user.model_dump())

        self.session.add(instance)

        try:
            await self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise UserAlreadyExist(f"User with same login or email already exists. User: {UserDTO}")

        await self.session.refresh(instance)

        return self._get_dto(instance)

    async def get(self, pk: int) -> Optional[UserDTO]:
        """
        Get user by primary key

        Args:
            pk: Primary key, id of the user

        Returns:
            UserDTO

        Raises:
            UserNotFound: if user with primary key does not exist
        """
        stmt = select(UserModel).where(UserModel.id == pk)

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        if result is None:
            raise UserNotFound(f"User not found by {pk} id")

        return self._get_dto(result)

    async def find(self, dto: FindUserDTO) -> Optional[UserDTO]:
        """
        Get user by FindUserDTO values,
        rows from database filters by match of dto not none fields

        Args:
            dto: FindUserDTO (multivariable data object)

        Returns:
            UserDTO

        Raises:
            UserNotFound: if user with fields that match to dto do not exist
        """
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        if result is None:
            raise UserNotFound()

        return self._get_dto(result)

    async def get_list(self, limit: int = None, offset: int = None) -> List[UserDTO]:
        """
        Get users list by limit and offset

        Args:
            limit: Number of users to return
            offset: Number of users to skip

        Returns:
            List[UserDTO]
        """
        stmt = select(UserModel).offset(offset).limit(limit)

        raw = await self.session.execute(stmt)
        results = raw.scalars().all()

        return [self._get_dto(row) for row in results]

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        """
        Update user by dto and primary key

        Args:
            dto: UpdateUserDTO, data to update
            pk: Primary key, id of the user to update

        Returns:
            UserDTO

        Raises:
            UserNotFound: if user with primary key does not exist
        """
        stmt = (
            update(UserModel)
            .values(**dto.model_dump(exclude_none=True))
            .filter_by(id=pk)
            .returning(UserModel)
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        await self.session.commit()

        if result is None:
            raise UserNotFound()

        return self._get_dto(result)

    async def delete(self, pk: int) -> None:
        """
        Delete user by primary key

        Args:
            pk: Primary key, id of the user to delete

        Returns:
            None
        """
        stmt = delete(UserModel).where(UserModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        """
        Update user password by primary key

        Args:
            new_password: New password of user
            pk: Primary key, id of the user to update
        """
        stmt = (
            update(UserModel)
            .values(password=new_password)
            .filter_by(id=pk)
            .returning(UserModel)
        )
        result: Optional[UserModel] = (await self.session.execute(stmt)).scalar_one_or_none()
        await self.session.commit()

        if result is None:
            raise UserNotFound()

        return self._get_dto(result)

    @staticmethod
    def _get_dto(row: UserModel) -> UserDTO:
        """
        Helper function to prevent repetitive code blocks

        Args:
            row: UserModel

        Returns:
            UserDTO
        """
        return UserDTO(
            id=row.id,
            name=row.name,
            login=row.login,
            email=row.email,
            password=row.password,
        )
