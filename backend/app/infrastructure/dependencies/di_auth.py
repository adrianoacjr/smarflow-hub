from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.user.authenticate_user import AuthenticateUser
from backend.app.infrastructure.gateways.token_service_jwt import TokenServiceJWT
from infrastructure.repositories.user_repository_postgres import UserRepositoryPostgres

class DIAuth:
    def build(
        self,
        session: AsyncSession,
    ) -> tuple[
        AuthenticateUser,
    ]:
        repo = UserRepositoryPostgres(session)
        token_service = TokenServiceJWT()

        return (
            AuthenticateUser(repo, token_service),
        )

    # def get_user_repository(self, session: AsyncSession) -> IUserRepository:
    #     return UserRepositoryPostgres(session)
    
    # def get_token_service(self) -> ITokenService:
    #     return TokenServiceJWT()
    
    # def get_get_current_user_service(self, session: AsyncSession) -> AuthenticateUser:
    #     return AuthenticateUser(
    #         self.get_user_repository(session),
    #         self.get_token_service()
    #     )
    
di_auth = DIAuth()
