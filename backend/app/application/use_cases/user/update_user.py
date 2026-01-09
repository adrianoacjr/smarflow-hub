from domain.interfaces.user_repository import IUserRepository

class UpdateUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
