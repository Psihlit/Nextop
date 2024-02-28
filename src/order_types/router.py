from typing import Optional

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.order_types.models import order_status
from src.order_types.schemas import OrderTypeSchema, ResponseModel, OrderTypeCreate, OrderTypeUpdate

router = APIRouter(
    prefix='/order_types',
    tags=['OrderType']
)


@router.get('/get_all_order_types', response_model=ResponseModel)
async def get_all_order_types(start: Optional[int] = Query(default=1, gt=0),
                              end: Optional[int] = Query(default=10, gt=0),
                              session: AsyncSession = Depends(get_async_session)):
    if start > end:
        start, end = end, start

    start -= 1  # Преобразуем ввод пользователя, чтобы начало считалось с 0
    end -= start  # Вычисляем разницу между конечным и начальным индексами

    try:
        query = select(order_status).offset(start).limit(end)
        result = await session.execute(query)
        return {
            "status": "success",
            "status_code": "200",
            "data": result.all(),
            "details": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.get('/get_order_type_by_id/{order_type_id}', response_model=ResponseModel)
async def get_order_type_by_id(order_type_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order_status).where(order_status.c.id == order_type_id)
        result = await session.execute(query)
        result = result.first()

        if result is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказа с идентификатором {order_type_id} не существует"
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": [result],
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("/add_order_typer")
async def add_order_type(new_order_type: OrderTypeCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(order_status).values(**new_order_type.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'повторяющееся значение ключа нарушает ограничение уникальности "order_status_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {new_order_type.id} уже существует существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании заказа: {str(e)}.",
            })


@router.put("/update_order_type/{order_type_id}")
async def update_order_type(order_type_id: int, updated_order: OrderTypeUpdate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order_status).where(order_status.c.id == order_type_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {order_type_id} не существует.",
            })

        stmt = update(order_status).where(order_status.c.id == order_type_id).values(**updated_order.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_status_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {order_type_id} не существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при обновлении заказа с идентификатором {order_type_id}.",
            })


@router.delete("/delete_order/{order_id}")
async def delete_order(order_type_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order_status).where(order_status.c.id == order_type_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {order_type_id} не существует.",
            })

        stmt = delete(order_status).where(order_status.c.id == order_type_id)
        await session.execute(stmt)
        await session.commit()

        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при удалении заказа с идентификатором {order_type_id}. {str(e)}",
        })
