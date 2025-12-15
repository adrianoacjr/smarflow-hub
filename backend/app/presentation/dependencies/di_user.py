from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.user_repository import IUserRepository
from application.user.create_user import CreateUser
from application.user.get_user import GetUser
from application.user.get_all_users import GetAllUsers
from application.user.delete_user import DeleteUser
from infrastructure.repositories.user_repository_postgres import UserRepositoryPostgres

class DIUser:
    def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return UserRepositoryPostgres(session)

    def get_create_user_service(self, session: AsyncSession) -> CreateUser:
        return CreateUser(self.get_user_repository(session))

    def get_get_user_service(self, session: AsyncSession) -> GetUser:
        return GetUser(self.get_user_repository(session))

    def get_get_all_users_service(self, session: AsyncSession) -> GetAllUsers:
        return GetAllUsers(self.get_user_repository(session))

    def get_delete_user_service(self, session: AsyncSession) -> DeleteUser:
        return DeleteUser(self.get_user_repository(session))

di_user = DIUser()
