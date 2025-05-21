from typing import List

from src.user.dependencies.repository import IUserPropertyRepository, UserPropertyRepository

from src.user.dto import UserPropertyDTO, UpdateUserPropertyDTO

class UserPropertyService:
    def __init__(self, repository: IUserPropertyRepository):
        self.repository: UserPropertyRepository = repository

    async def create(self, dto: UserPropertyDTO) -> UserPropertyDTO:
        return await self.repository.create(dto)

    async def update(self, dto: UpdateUserPropertyDTO, pk: int) -> UserPropertyDTO:
        return await self.repository.update(dto, pk)

    async def delete(self, pk: int) -> None:
        return await self.repository.delete(pk)

    async def get(self, user_id) -> List[UserPropertyDTO]:
        return await self.repository.get(user_id)