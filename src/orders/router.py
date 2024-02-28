from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.orders.models import order
from src.orders.schemas import OrderCreate, ResponseModel, OrderUpdate

router = APIRouter(
    prefix='/orders',
    tags=['Order']
)


@router.get('/get_all_orders', response_model=ResponseModel)
async def get_all_orders(start: Optional[int] = Query(default=1, gt=0), end: Optional[int] = Query(default=10, gt=0),
                         session: AsyncSession = Depends(get_async_session)):
    if start > end:
        start, end = end, start

    start -= 1  # Преобразуем ввод пользователя, чтобы начало считалось с 0
    end -= start  # Вычисляем разницу между конечным и начальным индексами

    try:
        query = select(order).offset(start).limit(end)
        print(query)
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


@router.get('/get_order_by_id/{order_id}', response_model=ResponseModel)
async def get_orders_by_id(order_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.id == order_id)
        result = await session.execute(query)
        result = result.first()

        if result is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказа с идентификатором {order_id} не существует"
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


@router.get('/get_order_by_user_id/{user_id}', response_model=ResponseModel)
async def get_orders_by_user_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.user_id == user_id)
        result = await session.execute(query)
        result = result.fetchall()

        if not result:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказов пользователя с идентификатором {user_id} не существует."
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": result,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.get('/get_order_by_status_id/{status_id}', response_model=ResponseModel)
async def get_orders_by_status_id(status_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.status_id == status_id)
        result = await session.execute(query)
        result = result.fetchall()

        if not result:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказов с идентификатором статуса {status_id} не существует."
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": result,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("/add_order")
async def add_order(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(order).values(**new_order.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        print(e)
        if 'повторяющееся значение ключа нарушает ограничение уникальности "order_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {new_order.id} уже существует существует.",
            })

        elif 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_status_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {new_order.status_id} не существует.",
            })

        elif 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_user_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Пользователь с идентификатором {new_order.user_id} не существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании заказа: {str(e)}",
            })


@router.put("/update_order/{order_id}")
async def update_order(order_id: int, updated_order: OrderUpdate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.id == order_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {order_id} не существует.",
            })

        stmt = update(order).where(order.c.id == order_id).values(**updated_order.dict())
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
                "details": f"Статуса заказа с идентификатором {updated_order.status_id} не существует.",
            })

        elif 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_user_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Пользователь с идентификатором {updated_order.user_id} не существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при обновлении заказа с идентификатором {order_id}.",
            })


@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(order).where(order.c.id == order_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказ с идентификатором {order_id} не существует.",
            })

        stmt = delete(order).where(order.c.id == order_id)
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
            "details": f"Произошла ошибка при удалении заказа с идентификатором {order_id}. {str(e)}",
        })
