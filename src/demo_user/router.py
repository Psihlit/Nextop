from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, insert, column
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.database import get_async_session
from src.demo_user.models import user
from src.tokens.models import token
from src.demo_user.schemas import ResponseModel, UserCreate
from src.secure import pwd_context, apikey_scheme
from src.tokens.schemas import Token

router = APIRouter(
    prefix='/users',
    tags=['Demo User']
)


@router.get("", response_model=ResponseModel)
async def get_users(start: Optional[int] = Query(default=0, ge=0),
                    step: Optional[int] = Query(default=10, gt=0),
                    user_id: Optional[int] = None,
                    session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user)

        if user_id:
            query = query.where(user.c.id == user_id)

        result = await session.execute(query.offset(start).limit(step))
        users = result.all()

        if not users:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Результатов по заданным критериям не найдено"
            })

        return {
            "status": "success",
            "status_code": "200",
            "data": users,
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"{str(e)}"
        })


@router.post("")
async def add_user(new_user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user).where(user.c.email == new_user.email)
        result = await session.execute(query)
        existing_user = result.first()

        if existing_user:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Пользователь с такой почтой уже существует!"
            )

        new_user_model = UserCreate(
            email=new_user.email,
            surname=new_user.surname,
            name=new_user.name,
            hashed_password=pwd_context.hash(new_user.hashed_password),
            phone_number=new_user.phone_number,
            is_active=new_user.is_active,
            is_superuser=new_user.is_superuser,
            is_verified=new_user.is_verified,
        )

        stmt = insert(user).values(**new_user_model.dict())
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
                "details": f"Водитель с идентификатором {user.id} уже существует.",
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


@router.get("/self")
async def get_info_about_authorize_user(access_token: Annotated[str, Depends(apikey_scheme)],
                                        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(token).where(token.c.access_token == access_token)
        result = await session.execute(query)
        existing_token = result.first() # находим id пользователя по access токену

        if not existing_token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED"
            )

        user_id = existing_token[2]  # Получаем user_id из данных токена

        user_query = select(user).where(user.c.id == user_id)
        user_result = await session.execute(user_query)
        user_data = user_result.first()  # получаем данные о пользователе

        return {
            "id": user_data.id,
            "email": user_data.email,
            "surname": user_data.surname,
            "name": user_data.name,
            "phone_number": user_data.phone_number
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка: {str(e)}.",
        })
