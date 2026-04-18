from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from application.dtos.user.change_user_password_command import ChangeUserPasswordCommand
from application.exceptions.user_exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidPasswordError,
    SamePasswordError,
    UserNotFoundError
)
from application.interfaces.password_hasher import IPasswordHasher

class ChangeUserPassword:
    def __init__(
        self,
        repo: IUserRepository,
        password_hasher: IPasswordHasher
    ) -> None:
        self.repo = repo
        self.password_hasher = password_hasher

    async def execute(self, command: ChangeUserPasswordCommand) -> User:
        user = await self.repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        if not user.active:
            raise InactiveUserError("Inactive user")
        
        if not self.password_hasher.verify(command.current_password, user.password_hash):
            raise InvalidCredentialsError("Current password is invalid")
        
        if not command.new_password.strip():
            raise InvalidPasswordError("New password cannot be empty")
        
        if len(command.new_password) < 8:
            raise InvalidPasswordError("New password must have at least 8 characters")
        
        if self.password_hasher.verify(command.new_password, user.password_hash):
            raise SamePasswordError("New password must be different from the current password")
        
        user.password_hash = self.password_hasher.hash(command.new_password)

        return await self.repo.update(user)
