from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.user.authenticate_user import AuthenticateUser
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.update_user import UpdateUser
from infrastructure.gateways.bcrypt_password_hasher import BcryptPasswordHasher
from infrastructure.gateways.token_service_jwt import TokenServiceJWT
from infrastructure.repositories.user_repository_postgres import UserRepositoryPostgres
from infrastructure.config import settings

def get_user_repository(session: AsyncSession) -> UserRepositoryPostgres:
    return UserRepositoryPostgres(session)

def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()

def get_token_service() -> TokenServiceJWT:
    return TokenServiceJWT(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ACCESS_TOKEN_ALGORITHM,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

def get_create_user(session: AsyncSession) -> CreateUser:
    return CreateUser(
        repo=get_user_repository(session),
        password_hasher=get_password_hasher(),
    )

def get_authenticate_user(session: AsyncSession) -> AuthenticateUser:
    return AuthenticateUser(
        repo=get_user_repository(session),
        password_hasher=get_password_hasher(),
        token_service=get_token_service(),
    )

def get_get_user(session: AsyncSession) -> GetUser:
    return GetUser(repo=get_user_repository(session))

def get_update_user(session: AsyncSession) -> UpdateUser:
    return UpdateUser(repo=get_user_repository(session))

def get_delete_user(session: AsyncSession) -> DeleteUser:
    return DeleteUser(repo=get_user_repository(session))