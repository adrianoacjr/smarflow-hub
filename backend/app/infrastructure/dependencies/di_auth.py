from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.user.authenticate_user import AuthenticateUser
from infrastructure.dependencies.di_user import (
    get_authenticate_user,
    get_token_service,
)

def get_authenticate_user_use_case(session: AsyncSession) -> AuthenticateUser:
    return get_authenticate_user(session)
