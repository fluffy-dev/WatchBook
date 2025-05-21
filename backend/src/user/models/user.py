from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.libs.base_model import Base


class UserModel(Base):
    """

    Model for users

    :param name: name of the user
    :type name: str

    :param email: email of the user
    :type email: str

    :param login: login of the user
    :type login: str

    :param password: hashed password of the user
    :type password: str

    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    password: Mapped[str]