from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, Float

from src.auth.models import user
from src.order_statuses.models import order_status
from src.drivers.models import driver
from src.dispatchers.models import dispatcher

metadata = MetaData()

order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status_id", Integer, ForeignKey(order_status.c.id)),
    Column("start_address", String, nullable=False),
    Column("end_address", String, nullable=False),
    Column("cost", Float, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("dispatcher_id", Integer, ForeignKey(dispatcher.c.id)),
    Column("driver_id", Integer, ForeignKey(driver.c.id))
)


