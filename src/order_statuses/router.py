from typing import Optional

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.order_statuses.models import order_status
from src.order_statuses.schemas import ResponseModel, OrderTypeCreate, OrderTypeUpdate

router = APIRouter(
    prefix='/order_statuses',
    tags=['OrderType']
)


@router.get("", response_model=ResponseModel)
async def get_order_status_with_filtration(start: Optional[int] = Query(default=0, ge=0),
                                           step: Optional[int] = Query(default=10, gt=0),
                                           order_status_id: Optional[int] = None,
                                           session: AsyncSession = Depends(get_async_session)):
    """
    Получение данных и статусах заказов
    :param start: переменная, отвечающая с какой записи отсчитывать вывод\n
    :param step: шаг вывода\n
    :param order_status_id: id статуса заказа\n
    :param session: \n
    :return:
    """
    try:
        query = select(order_status)

        if order_status_id:
            query = query.where(order_status.c.id == order_status_id)

        result = await session.execute(query.offset(start).limit(step))
        order_statuses = result.all()

        if not order_statuses:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа по заданному критерию не найдено."
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": order_statuses,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("")
async def add_order_status(new_order_status: OrderTypeCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление нового статуса заказа\n
    :param new_order_status: словарь (JSON) с данными о новом статусе\n
    :param session: \n
    :return:
    """
    try:
        stmt = insert(order_status).values(**new_order_status.dict())
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
                "details": f"Заказ с идентификатором {new_order_status.id} уже существует существует.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при создании статуса заказа: {str(e)}"
        })


@router.put("/{order_status_id}")
async def update_order_status(order_status_id: int, updated_order: OrderTypeUpdate,
                              session: AsyncSession = Depends(get_async_session)):
    """
    Обновление данных о существующем статусе\n
    :param order_status_id: id статуса заказа\n
    :param updated_order: словарь (JSON) с новыми данными о статусе заказа\n
    :param session: \n
    :return:
    """
    try:
        query = select(order_status).where(order_status.c.id == order_status_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {order_status_id} не существует.",
            })

        stmt = update(order_status).where(order_status.c.id == order_status_id).values(**updated_order.dict())
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
                "details": f"Статуса заказа с идентификатором {order_status_id} не существует.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при обновлении заказа с идентификатором {order_status_id}.",
        })


@router.delete("/{order_status_id}")
async def delete_order_status(order_status_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление данных о статусе заказа\n
    :param order_status_id: id статуса заказа\n
    :param session: \n
    :return:
    """
    try:
        query = select(order_status).where(order_status.c.id == order_status_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Статуса заказа с идентификатором {order_status_id} не существует.",
            })

        stmt = delete(order_status).where(order_status.c.id == order_status_id)
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
            "details": f"Произошла ошибка при удалении статуса заказа с идентификатором {order_status_id}. {str(e)}",
        })
