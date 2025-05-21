from typing import Optional, List, Type

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from src.user.exceptions import UserAlreadyExist, UserNotFound, UserPropertyCreationError, UserPropertyNotFound
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

    async def get(self, pk: int) -> Optional[UserPropertyDTO]:
        stmt = select(UserPropertyModel).filter(UserPropertyModel.id == pk)

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        if result is None:
            raise UserPropertyNotFound()

        return self._get_dto(result)

    async def get_list(self, limit: int = None, offset: int = None) -> List[UserPropertyDTO]:
        stmt = select(UserPropertyModel).limit(limit).offset(offset)
        raw = await self.session.execute(stmt)

        results = raw.scalars().all()

        return [self._get_dto(result) for result in results]

    @staticmethod
    def _get_dto(instance: UserPropertyModel) -> UserPropertyDTO:
        return UserPropertyDTO(
            id=instance.id,
            key=instance.key,
            value=instance.value,
            user_id=instance.user_id
        )