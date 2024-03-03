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


@router.get("", response_model=ResponseModel)
async def get_orders_with_filtration(start: Optional[int] = Query(default=0, ge=0),
                                     step: Optional[int] = Query(default=10, gt=0),
                                     order_id: Optional[int] = None,
                                     user_id: Optional[int] = None,
                                     status_id: Optional[int] = None,
                                     session: AsyncSession = Depends(get_async_session)):
    """
    :param start: переменная, отвечающая с какой записи отсчитывать вывод\n
    :param step: шаг вывода\n
    :param order_id: id заказа\n
    :param user_id: id пользователя\n
    :param status_id: id статуса заказа\n
    :param session:\n
    :return:
    """

    try:
        query = select(order)

        if order_id:
            query = query.where(order.c.id == order_id)
        if user_id:
            query = query.where(order.c.user_id == user_id)
        if status_id:
            query = query.where(order.c.status_id == status_id)

        result = await session.execute(query.offset(start).limit(step))
        orders = result.all()

        if not orders:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Заказов по заданным критериям не найдено."
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": orders,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("")
async def add_order(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление данных о новом заказе\n
    :param new_order: словарь (JSON) с данными о новом заказе\n
    :param session: \n
    :return:
    """
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

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_dispatcher_id_fkey"' in str(
                e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {new_order.dispatcher_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_driver_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Водителя с идентификатором {new_order.driver_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_status_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {new_order.status_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_user_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Пользователя с идентификатором {new_order.user_id} не существует.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.put("/{order_id}")
async def update_order(order_id: int, updated_order: OrderUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Обновление данных существующего заказа\n
    :param order_id: id заказа\n
    :param updated_order: словарь (JSON) с новыми данными о заказе\n
    :param session: \n
    :return:
    """
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

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_dispatcher_id_fkey"' in str(
                e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {updated_order.dispatcher_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_driver_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Водителя с идентификатором {updated_order.driver_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_status_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {updated_order.status_id} не существует.",
            })

        if 'INSERT или UPDATE в таблице "order" нарушает ограничение внешнего ключа "order_user_id_fkey"' in str(e):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Пользователя с идентификатором {updated_order.user_id} не существует.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.delete("/{order_id}")
async def delete_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление данных о заказе\n
    :param order_id: id заказа\n
    :param session: \n
    :return:
    """
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
