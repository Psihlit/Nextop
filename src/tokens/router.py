import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from src.database import get_async_session
from src.demo_user.models import user
from src.demo_user.schemas import UserAuth
from src.secure import pwd_context
from src.tokens.models import token
from src.tokens.schemas import Token

router = APIRouter(
    prefix='/tokens',
    tags=['Token']
)


@router.post("")
async def create_token(user_data: UserAuth, session: AsyncSession = Depends(get_async_session)):
    """
    Создание токена для авторизации пользователя
    :param user_data: данные для проверки существования пользователя (почта и пароль)
    :param session:
    :return:
    """
    try:
        # получаем пользователя по email
        query = select(user).where(user.c.email == user_data.email)
        result = await session.execute(query)
        existing_user = result.first()

        # проверяем наличие данного пользователя
        if not existing_user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )

        # записываем пароль пользователя
        user_hashed_password = existing_user.hashed_password

        # проверяем пароль пользователя
        if not pwd_context.verify(user_data.hashed_password, user_hashed_password):
            raise HTTPException(status_code=400, detail="Неверная почта или пароль!")

        # генерируем новый токен
        new_token: Token = Token(user_id=existing_user.id, access_token=str(uuid.uuid4()))

        # делаем запрос по id пользователя
        query = select(token).where(token.c.user_id == new_token.user_id)
        result = await session.execute(query)
        existing_token = result.first()

        # если по id пользователя токен уже существует, обновляем токен
        if existing_token:
            stmt = update(token).where(token.c.user_id == new_token.user_id).values(access_token=new_token.access_token)
        else:  # иначе создаем новый токен для пользователя
            stmt = insert(token).values(**new_token.dict())

        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "status_code": "200",
            "data": {"access_token": new_token.access_token},
            "details": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Произошла ошибка: {str(e)}.",
        })
