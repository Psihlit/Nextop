from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.drivers.models import driver
from src.drivers.schemas import ResponseModel, DriverCreate, DriverUpdate

router = APIRouter(
    prefix='/drivers',
    tags=['Driver']
)


@router.get('', response_model=ResponseModel)
async def get_drivers(start: Optional[int] = Query(default=0, ge=0),
                      step: Optional[int] = Query(default=10, gt=0),
                      driver_id: Optional[int] = None,
                      dispatcher_id: Optional[int] = None,
                      session: AsyncSession = Depends(get_async_session)):
    """
    Получение данных о водителях по заданным критериям\n
    :param start: переменная, отвечающая с какой записи отсчитывать вывод\n
    :param step: шаг вывода\n
    :param driver_id: id водителя\n
    :param dispatcher_id: id диспетчера\n
    :param session:\n
    :return:
    """
    try:
        query = select(driver)

        if driver_id:
            query = query.where(driver.c.id == driver_id)
        if dispatcher_id:
            query = query.where(driver.c.dispatcher_id == dispatcher_id)

        result = await session.execute(query.offset(start).limit(step))
        drivers = result.all()

        if not drivers:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Результатов по заданным критериям не найдено"
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": drivers,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("")
async def add_driver(new_driver: DriverCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление данных о новом водителе\n
    :param new_driver: словарь (JSON) с данными о новом водителе\n
    :param session: \n
    :return:
    """
    try:
        stmt = insert(driver).values(**new_driver.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'повторяющееся значение ключа нарушает ограничение уникальности "driver_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Водитель с идентификатором {driver.id} уже существует.",
            })

        if ('INSERT или UPDATE в таблице "driver" нарушает ограничение внешнего ключа "driver_dispatcher_id_fkey"'
                in str(e)):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {new_driver.dispatcher_id} не существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании водителя: {str(e)}.",
            })

    except ValueError as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при создании водителя: {str(e)}.",
        })


@router.put("/{driver_id}")
async def update_driver(driver_id: int, updated_driver: DriverUpdate,
                        session: AsyncSession = Depends(get_async_session)):
    """
    Обновление данных о существующем водителе\n
    :param driver_id: id водителя\n
    :param updated_driver: словарь (JSON) с новыми данными о водителе\n
    :param session: \n
    :return:
    """
    try:
        query = select(driver).where(driver.c.id == driver_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Водителя с идентификатором {driver_id} не существует.",
            })

        stmt = update(driver).where(driver.c.id == driver_id).values(**updated_driver.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'повторяющееся значение ключа нарушает ограничение уникальности "driver_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Водитель с идентификатором {driver.id} уже существует.",
            })

        if ('INSERT или UPDATE в таблице "driver" нарушает ограничение внешнего ключа "driver_dispatcher_id_fkey"'
                in str(e)):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {updated_driver.dispatcher_id} не существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании водителя: {str(e)}.",
            })

    except ValueError as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при создании водителя: {str(e)}.",
        })


@router.delete("/{driver_id}")
async def delete_driver(driver_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление данных о существующем водителе\n
    :param driver_id: id водителя\n
    :param session: \n
    :return:
    """
    try:
        query = select(driver).where(driver.c.id == driver_id)
        result = await session.execute(query)
        existing_order = result.first()

        if existing_order is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Водителя с идентификатором {driver_id} не существует.",
            })

        stmt = delete(driver).where(driver.c.id == driver_id)
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
            "details": f"Произошла ошибка при удалении водителя с идентификатором {driver_id}: {str(e)}",
        })
