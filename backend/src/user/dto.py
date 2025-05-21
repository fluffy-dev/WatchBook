from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List

class UserDTO(BaseModel):
    id: Optional[int]
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr | str
    password: Optional[str]

class PublicUserDTO(BaseModel):
    name: constr(max_length=30)

class PrivateUserDTO(BaseModel):
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr | str

class FindUserDTO(BaseModel):
    id: Optional[int] = None
    login: constr(max_length=50) = None
    email: EmailStr | str = None

class UpdateUserDTO(BaseModel):
    name: constr(max_length=30)
    login: constr(max_length=50)

class UserPropertyDTO(BaseModel):
    id: Optional[int] = None
    key: constr(max_length=25)
    value: constr(max_length=30)
    user_id: int

class UpdateUserPropertyDTO(BaseModel):
    key: constr(max_length=25) = None
    value: constr(max_length=30) = None

class UserProfileDTO(BaseModel):
    id: Optional[int]
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr = None
    properties: List[UserPropertyDTO] = []