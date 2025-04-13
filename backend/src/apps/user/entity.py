from dataclasses import dataclass


@dataclass
class UserEntity:
    name: str
    email: str
    login: str
    password: str


class UserPropertyEntity:
    key: str
    value: str

    user_id: int