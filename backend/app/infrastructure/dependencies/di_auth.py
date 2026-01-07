from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.user_repository import IUserRepository

from application.interfaces.token_service import ITokenService
from application.use_cases.user.authenticate_user import AuthenticateUser

from infrastructure.repositories.user_repository_postgres import UserRepositoryPostgres
from adapters.security.token_service_jwt import TokenServiceJWT

class DIAuth:
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepositoryPostgres(session)
    
    def get_token_service(self) -> ITokenService:
        return TokenServiceJWT()
    
    def get_get_current_user_service(self, session: AsyncSession) -> AuthenticateUser:
        return AuthenticateUser(
            self.get_user_repository(session),
            self.get_token_service()
        )
    
di_auth = DIAuth()
