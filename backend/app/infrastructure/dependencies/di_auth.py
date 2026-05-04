from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.user.authenticate_user import AuthenticateUser
from application.use_cases.user.get_current_user import GetCurrentUser
from application.interfaces.user_context import IUserContext
from infrastructure.dependencies.di_user import (
    get_authenticate_user,
    get_user_repository,
)

def get_authenticate_user_use_case(session: AsyncSession) -> AuthenticateUser:
    return get_authenticate_user(session)

def get_get_current_user_use_case(
    session: AsyncSession,
    user_context: IUserContext,
) -> GetCurrentUser:
    return GetCurrentUser(
        repo=get_user_repository(session),
        user_context=user_context,
    )
