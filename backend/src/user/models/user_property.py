
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.libs.base_model import Base


class UserPropertyModel(Base):
    """

    Model for external user properties

    :param key: Key/Title value of the property
    :type key: str

    :param value: Value of the property
    :type value: str

    :param user_id: ID of the user which have this property
    :type user_id: int

    """

    __tablename__ = 'user_properties'

    key: Mapped[str] = mapped_column(String(25))
    value: Mapped[str] = mapped_column(String(30))

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
