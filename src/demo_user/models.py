from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import relationship

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

user_orders = relationship("order", back_populates="user")
user_tokens = relationship("token", back_populates="user")

