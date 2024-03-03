from fastapi import FastAPI
import sys

sys.path.append("D:\\PycharmProjects\\Nextop")

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from orders.router import router as router_order
from order_statuses.router import router as router_order_type
from dispatchers.router import router as router_dispatcher
from drivers.router import router as router_driver

app = FastAPI(
    title="Nextop"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_order)

app.include_router(router_order_type)

app.include_router(router_dispatcher)

app.include_router(router_driver)
