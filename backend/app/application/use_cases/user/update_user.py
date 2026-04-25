from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.email_address import EmailAddress
from application.dtos.user.update_user_command import UpdateUserCommand
from application.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundError

class UpdateUser:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def execute(self, command: UpdateUserCommand) -> User:
        user = await self.repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        if command.name is not None:
            normalized_name = command.name.strip()
            if not normalized_name:
                raise ValueError("name cannot be empty")
            user.name = normalized_name

        if command.email is not None:
            new_email = EmailAddress(command.email)

            if user.email != new_email:
                existing_user = await self.repo.get_by_email(new_email)
                if existing_user is not None and existing_user.id != user.id:
                    raise UserAlreadyExistsError("A user with this email already exists")
                
                user.email = new_email

        if command.access_level is not None:
            user.change_access_level(command.access_level)

        return await self.repo.update(user)

                
