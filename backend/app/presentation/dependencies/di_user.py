from domain.interfaces.user_repository import IUserRepository
from application.user.create_user import CreateUser
from application.user.get_user import GetUser
from application.user.get_all_users import GetAllUsers
from application.user.delete_user import DeleteUser
from infrastructure.repositories.user_repository_fake import UserRepositoryFake

class DIUser:
    def __init__(self):
        self._repo: IUserRepository = UserRepositoryFake()

    def get_user_repository(self) -> IUserRepository:
        return self._repo

    def get_create_user_service(self) -> CreateUser:
        return CreateUser(self._repo)

    def get_get_user_service(self) -> GetUser:
        return GetUser(self._repo)

    def get_get_all_users_service(self) -> GetAllUsers:
        return GetAllUsers(self._repo)

    def get_delete_user_service(self) -> DeleteUser:
        return DeleteUser(self._repo)

di_user = DIUser()
