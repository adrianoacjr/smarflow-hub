from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from application.exceptions.user_exceptions import UserNotFoundError

class DeleteUser:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def execute(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError("User not found")
        
        user.deactivate()

        return await self.repo.update(user)

