from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.user.exceptions import UserPropertyCreationError, UserPropertyNotFound
from src.config.database.session import ISession
from src.user.models.user_property import UserPropertyModel
from src.user.dto import UserPropertyDTO, UpdateUserPropertyDTO


class UserPropertyRepository:
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, user_property: UserPropertyDTO) -> UserPropertyDTO:
        instance = UserPropertyModel(**user_property.model_dump())
        self.session.add(instance)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise UserPropertyCreationError(f"Something went wrong while creating the property: {user_property}")

        await self.session.refresh(instance)

        return self._get_dto(instance)


    async def update(self, dto: UpdateUserPropertyDTO, pk: int) -> UserPropertyDTO:
        stmt = (
            update(UserPropertyModel)
            .values(**dto.model_dump(exclude_none=True))
            .filter_by(id=pk)
            .returning(UserPropertyModel)
        )

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        await self.session.commit()

        if result is None:
            raise UserPropertyNotFound()

        return self._get_dto(result)

    async def get(self, user_id: int) -> List[UserPropertyDTO]:
        """
        Get user properties by user id

        Args:
            user_id (int): User id

        Returns:
            List[UserPropertyDTO]

        """
        stmt = select(UserPropertyModel).where(UserPropertyModel.user_id == user_id)

        raw = await self.session.execute(stmt)
        results = raw.scalars().all()

        return [self._get_dto(result) for result in results]

    async def delete(self, pk: int) -> None:
        stmt = delete(UserPropertyModel).where(UserPropertyModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    @staticmethod
    def _get_dto(instance: UserPropertyModel) -> UserPropertyDTO:
        return UserPropertyDTO(
            id=instance.id,
            key=instance.key,
            value=instance.value,
            user_id=instance.user_id
        )