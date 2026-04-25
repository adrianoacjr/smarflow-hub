from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from application.exceptions.user_exceptions import (
    InactiveUserError,
    UnauthenticatedUserError,
    UserNotFoundError
)
from application.interfaces.user_context import IUserContext

class GetCurrentUser:
    def __init__(
        self,
        repo: IUserRepository,
        user_context: IUserContext,
    ) -> None:
        self.repo = repo
        self.user_context = user_context

    async def execute(self) -> User:
        current_user_id = self.user_context.user_id
        if current_user_id is None:
            raise UnauthenticatedUserError("User is not authenticated")
        
        user = await self.repo.get_by_id(current_user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        if not user.active:
            raise InactiveUserError("Inactive user")
        
        return user
