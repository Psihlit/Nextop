from sqlalchemy import MetaData, Table, Column, Integer, String

metadata = MetaData()

order_status = Table(
    "order_status",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status", String, nullable=False),
)