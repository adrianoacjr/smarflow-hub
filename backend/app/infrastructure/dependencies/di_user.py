from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.get_all_users import GetAllUsers
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.update_user import UpdateUser
from infrastructure.repositories.user_repository_postgres import UserRepositoryPostgres
from infrastructure.database import get_session

class DIUser:
    def get_user_repository(self) -> UserRepositoryPostgres:
        return UserRepositoryPostgres(get_session())

    def get_create_user_use_case(self) -> CreateUser:
        return CreateUser(self.get_user_repository())

    def get_get_user_use_case(self) -> GetUser:
        return GetUser(self.get_user_repository())

    def get_get_all_users_use_case(self) -> GetAllUsers:
        return GetAllUsers(self.get_user_repository())

    def get_delete_user_use_case(self) -> DeleteUser:
        return DeleteUser(self.get_user_repository())
    
    def get_update_user_use_case(self) -> DeleteUser:
        return DeleteUser(self.get_user_repository())

di_user = DIUser()
