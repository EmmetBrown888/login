from fastapi import HTTPException, status

from .models import User
from .schemas import UserLogin
from utils.crypt import check_pass


async def check_user(data: UserLogin):
    """
    Check user in database

    :param data: class 'user.schemas.UserLogin', parameters: phone: str, password: str
    :return: object or None
    """
    phone_exist: bool = await User.objects.filter(phone=data.phone).exists()
    if phone_exist:
        user: User = await User.objects.get(phone=data.phone)
        check_password: bool = await check_pass(data.password, user.password_hash)
        if check_password:
            return {
                'id': user.id,
                'email': user.email,
                'phone': user.phone,
                'birthday': user.birthday,
                'is_confirm': user.is_confirm
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect phone or password"
            )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect phone or password"
    )
