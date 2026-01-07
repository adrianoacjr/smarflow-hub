from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.get_all_users import GetAllUsers
from application.use_cases.user.delete_user import DeleteUser

from adapters.repositories.user_repository_postgres import UserRepositoryPostgres

class DIUser:
    def get_user_repository(self, session: AsyncSession) -> UserRepositoryPostgres:
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
