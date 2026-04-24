from datetime import datetime, timezone

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.email_address import EmailAddress
from application.dtos.user.create_user_command import CreateUserCommand
from application.exceptions.user_exceptions import InvalidPasswordError, UserAlreadyExistsError
from application.interfaces.password_hasher import IPasswordHasher

class CreateUser:
    def __init__(
        self,
        repo: IUserRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.repo = repo
        self.password_hasher = password_hasher

    async def execute(self, command: CreateUserCommand) -> User:
        email = EmailAddress(command.email)

        existing_user = await self.repo.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError("A user with this email already exists")
        
        if len(command.password) < 8:
            raise InvalidPasswordError("Password must have at leat 8 characters")
        
        password_hash = self.password_hasher.hash(command.password)

        new_user = User(
            name = command.name.strip(),
            email = email,
            password_hash = password_hash,
            access_level = command.access_level,
            user_type = command.user_type,
            created_at = datetime.now(timezone.utc),
        )
        
        return await self.repo.create(new_user)
