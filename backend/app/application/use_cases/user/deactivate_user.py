from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from application.dtos.user.deactivate_user_command import DeactivateUserCommand
from application.exceptions.user_exceptions import UserNotFoundError

class DeactivateUser:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def execute(self, command:DeactivateUserCommand) -> User:
        user = await self.repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        if not user.active:
            return user
        
        user.deativate()

        return await self.repo.update(user)
    