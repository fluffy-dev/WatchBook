from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    name: str
    email: str
    login: str
    password: Optional[str]


@dataclass
class UserPropertyEntity:
    key: str
    value: str

    user_id: Optional[int]