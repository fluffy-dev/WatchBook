from typing import List
from sqlalchemy import select, update, delete

from src.apps.user.exceptions import PropertyNotFound
from src.apps.user.models.user_properties import UserPropertyModel

from src.apps.user.entity import UserPropertyEntity
from src.config.database.session import ISession
from src.apps.user.dto import UserPropertyDTO, UpdateUserPropertyDTO


class UserPropertyRepository:

    def __init__(self, session: ISession):
        self.session: ISession = session

    async def create(self, user_property: UserPropertyEntity) -> UserPropertyDTO:
        """

        Function to create a new user property

        UserPropertyEntity fields:
            #. key: str
            #. value: str
            #. user_id: int

        :param user_property: UserPropertyEntity

        UserPropertyDTO fields:
            #. id: int
            #. key: str
            #. value: str
            #. user_id: int

        :return: UserPropertyDTO
        """
        instance = UserPropertyModel(**user_property.__dict__)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_properties(self, user_id: int) -> List[UserPropertyDTO]:
        """

        Function to get properties from the user via user_id

        :param user_id: int

        UserPropertyDTO fields:
            #. id: int
            #. key: str
            #. value: str
            #. user_id: int

        :return: List[UserPropertyDTO]
        """
        instance = select(UserPropertyModel).filter_by(user_id=user_id)
        user_properties = (await self.session.execute(instance)).scalars()
        return [self._get_dto(item) for item in user_properties]

    async def update(self, dto: UpdateUserPropertyDTO, pk: int) -> UserPropertyDTO:
        """

        Function to update a user property

        UpdateUserPropertyDTO fields:
            #. key: str
            #. value: str

        :param dto: UpdateUserPropertyDTO
        :param pk: int

        UserPropertyDTO fields:
            #. id: int
            #. key: str
            #. value: str
            #. user_id: int

        :return: UserPropertyDTO
        """
        stmt = (
            update(UserPropertyModel)
            .values(**dto.model_dump(exclude_none=True))
            .filter_by(id=pk)
            .returning(UserPropertyModel)
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        await self.session.commit()

        if result is None:
            raise PropertyNotFound()

        return self._get_dto(result)

    async def delete(self, pk: int) -> None:
        """

        Function to delete a user property by PrimaryKey

        :param pk: int
        :return: Nothing
        """

        stmt = delete(UserPropertyModel).where(UserPropertyModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()


    @staticmethod
    def _get_dto(row: UserPropertyModel) -> UserPropertyDTO:
        return UserPropertyDTO(
            id=row.id,
            key=row.key,
            value=row.value,
            user_id=row.user_id,
        )