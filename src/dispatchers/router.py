from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.dispatchers.models import dispatcher
from src.dispatchers.schemas import ResponseModel, DispatcherCreate, DispatcherUpdate

router = APIRouter(
    prefix='/dispatchers',
    tags=['Dispatchers']
)


@router.get('', response_model=ResponseModel)
async def get_dispatchers(start: Optional[int] = Query(default=0, ge=0),
                          step: Optional[int] = Query(default=10, gt=0),
                          dispatcher_id: Optional[int] = None,
                          session: AsyncSession = Depends(get_async_session)):
    """
    Получение данных из таблицы диспетчеров по заданным критериям\n
    :param start: переменная, отвечающая с какой записи отсчитывать вывод\n
    :param step: шаг вывода\n
    :param dispatcher_id: id диспетчера\n
    :param session:\n
    :return:
    """
    try:
        query = select(dispatcher)

        if dispatcher_id:
            query = query.where(dispatcher.c.id == dispatcher_id)

        result = await session.execute(query.offset(start).limit(step))
        dispatchers = result.all()

        if not dispatchers:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Не найдено записей по данным критериям."
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": dispatchers,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("")
async def add_dispatcher(new_dispatcher: DispatcherCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление данных о диспетчере в таблицу\n
    :param new_dispatcher: словарь (JSON) с данными о новом диспетчере\n
    :param session:\n
    :return:
    """
    try:
        stmt = insert(dispatcher).values(**new_dispatcher.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'повторяющееся значение ключа нарушает ограничение уникальности "dispatcher_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчер с идентификатором {dispatcher.id} уже существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании диспетчера: {str(e)}.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при создании диспетчера: {str(e)}.",
        })


@router.put("/{dispatchers_id}")
async def update_dispatcher(dispatcher_id: int, updated_dispatcher: DispatcherUpdate,
                            session: AsyncSession = Depends(get_async_session)):
    """
    Обновление данных о существующем диспетчере\n
    :param dispatcher_id: id диспетчера, данные о котором следует обновить\n
    :param updated_dispatcher: словарь (JSON) с новыми данными о диспетчере\n
    :param session:\n
    :return:
    """
    try:
        query = select(dispatcher).where(dispatcher.c.id == dispatcher_id)
        result = await session.execute(query)
        existing_dispatcher = result.first()

        if existing_dispatcher is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {dispatcher_id} не существует.",
            })

        stmt = update(dispatcher).where(dispatcher.c.id == dispatcher_id).values(**updated_dispatcher.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": None,
            "details": None
        }

    except IntegrityError as e:
        if 'повторяющееся значение ключа нарушает ограничение уникальности "dispatcher_pkey"' in str(e):
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчер с идентификатором {dispatcher.id} уже существует.",
            })

        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": f"Произошла ошибка при создании диспетчера: {str(e)}.",
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка при создании диспетчера: {str(e)}.",
        })


@router.delete("/{dispatcher_id}")
async def delete_dispatcher(dispatcher_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление данных о диспетчере\n
    :param dispatcher_id: id диспетчера, данные о котором следует удалить\n
    :param session:\n
    :return:
    """
    try:
        query = select(dispatcher).where(dispatcher.c.id == dispatcher_id)
        result = await session.execute(query)
        existing_dispatcher = result.first()

        if existing_dispatcher is None:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Диспетчера с идентификатором {dispatcher_id} не существует.",
            })

        stmt = delete(dispatcher).where(dispatcher.c.id == dispatcher_id)
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
            "details": f"Произошла ошибка при удалении диспетчера с идентификатором {dispatcher_id}: {str(e)}",
        })
