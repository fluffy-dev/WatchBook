from fastapi import APIRouter

from src.user.dto import UserDTO, UserProfileDTO
from src.user.entity import UserEntity
from src.user.dependencies.service import IUserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDTO)
async def create_user(user: UserEntity, service: IUserService) -> UserDTO:
    return await service.create_user(user)