from typing import Optional, List, Type

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.user.exceptions import AlreadyExistError, UserNotFound
from src.user.entity import UserEntity
from src.config.database.session import ISession
from src.user.models.user import UserModel
from src.user.dto import UpdateUserDTO, UserDTO, FindUserDTO


class UserRepository:
    """

    Class to work with User Model,

    Class methods:
        #. get_user
        #. get_list
        #. create
        #. delete
        #. update
        #. update_password

    Repository Uses FastAPI Injection System in session providing,
    ISession is injected sqlalchemy async session generator function.

    """
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, user: UserEntity) -> UserDTO:
        """

        Function to create a new user from user_entity

        UserEntity:
            #. name: str.
            #. email: str.
            #. login: str.
            #. password: str.

        :param user: UserEntity

        UserDTO:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: UserDTO

        :raises AlreadyExistError: if user with same credentials (email or login) already exists

        """
        instance = UserModel(**user.__dict__)

        self.session.add(instance)

        try:
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistError()

        await self.session.refresh(instance)

        return self._get_dto(instance)

    async def get_user(self, dto: FindUserDTO) -> Optional[UserDTO]:
        """

        Function to get a user by FindUserDTO fields

        FindUserDTO:
            #. id : int.
            #. email: str.
            #. login: str.


        :param dto: FindUserDTO

        UserDTO:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: UserDTO

        :raises UserNotFound: if user with credentials (email or login) doesn't exist
        """

        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))

        result = (await self.session.execute(stmt)).scalar_one_or_none()

        if result is None:
            raise UserNotFound()

        return self._get_dto(result)

    async def get_list(self, limit: int = None, offset: int = None) -> List[UserDTO]:
        """
        Function to get a list of users, from ``offset`` num items get ``limit`` items

        :param limit: number of items to get, by default None
        :param offset: number of items to skip, by default None

        if you don't provide limit, you will get all users, started from offset.

        if you don't provide offset, you will get users from first.

        UserDTO:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: List[UserDTO]
        """

        stmt = select(UserModel).offset(offset).limit(limit)

        results: List[UserModel] = (await self.session.execute(stmt)).scalars().all()

        return [self._get_dto(row) for row in results]

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        """

        Function to update a user model with UpdateUserDTO fields and PrimaryKey


        UpdateUserDTO fields:
            #. name: str.
            #. login: str.

        :param dto: UpdateUserDTO
        :param pk: int

        UserDTO fields:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :return: UserDTO

        :raises UserNotFound: if user with this PK/ID doesn't exist
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

        Function to delete a user model by PrimaryKey

        :param pk: int
        :return: None
        """
        stmt = delete(UserModel).where(UserModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        """

        function to update a user password by PrimaryKey.

        UserDTO fields:
            #. id :int.
            #. email: str.
            #. login: str.
            #. email: str.
            #. password: str.

        :param new_password: str
        :param pk: int
        :return: UserDTO

        :raises UserNotFound: if user with this PK/ID doesn't exist

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
        return UserDTO(
            id=row.id,
            name=row.name,
            login=row.login,
            email=row.email, # DTO: pydantic EmailStr, UserModel: str
            password=row.password,
        )
