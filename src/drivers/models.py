from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from src.dispatchers.models import dispatcher
from sqlalchemy.orm import relationship

metadata = MetaData()

driver = Table(
    "driver",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("dispatcher_id", Integer, ForeignKey(dispatcher.c.id))
)

driver_order = relationship("order", uselist=False, back_populates="driver")
