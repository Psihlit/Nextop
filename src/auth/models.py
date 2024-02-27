from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

metadata = MetaData()

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

# dispatcher = Table(
#     "dispatcher",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("surname", String, nullable=False),
#     Column("email", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("phone_number", String, nullable=False)
# )
#
# driver = Table(
#     "driver",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("surname", String, nullable=False),
#     Column("email", String, nullable=False),
#     Column("password", String, nullable=False),
#     Column("phone_number", String, nullable=False),
#     Column("dispatcher_id", Integer, ForeignKey(dispatcher.c.id))
# )


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[int] = mapped_column(String, nullable=False)
    surname: Mapped[int] = mapped_column(String, nullable=False)
    phone_number: Mapped[int] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)