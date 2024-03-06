from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from src.demo_user.models import user

metadata = MetaData()

token = Table(
    "token",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("access_token", String, unique=True, index=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),

)

token_users = relationship("user", back_populates="token")

