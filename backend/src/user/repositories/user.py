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
        instance = UserModel(**user.model_dump())

        self.session.add(instance)

        try:
            await self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise UserAlreadyExist(f"User with same login or login already exists. User: {UserDTO}")

        await self.session.refresh(instance)

        return self._get_dto(instance)

    async def get(self, pk: int) -> Optional[UserDTO]:
        stmt = select(UserModel).where(UserModel.id == pk)

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        if result is None:
            raise UserNotFound(f"User not found by {pk} id")

        return self._get_dto(result)

    async def find(self, dto: FindUserDTO) -> Optional[UserDTO]:
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))

        raw = await self.session.execute(stmt)
        result = raw.scalar_one_or_none()

        if result is None:
            raise UserNotFound()

        return self._get_dto(result)

    async def get_list(self, limit: int = None, offset: int = None) -> List[UserDTO]:
        stmt = select(UserModel).offset(offset).limit(limit)

        raw = await self.session.execute(stmt)
        results = raw.scalars().all()

        return [self._get_dto(row) for row in results]

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
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
        stmt = delete(UserModel).where(UserModel.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
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
            email=row.email,
            password=row.password,
        )
