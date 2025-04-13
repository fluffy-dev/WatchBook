from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserDTO(BaseModel):
    id: Optional[int]
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr
    password: Optional[str]

class FindUserDTO(BaseModel):
    id: Optional[int] = None
    login: constr(max_length=50) = None
    email: EmailStr = None


class UpdateUserDTO(BaseModel):
    name: constr(max_length=30)
    login: constr(max_length=50)

