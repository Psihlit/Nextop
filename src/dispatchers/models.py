from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import relationship

metadata = MetaData()

dispatcher = Table(
    "dispatcher",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("phone_number", String, nullable=False)
)

dispatcher_orders = relationship("order", back_populates="dispatcher")

dispatcher_drivers = relationship("driver", back_populates="dispatcher")