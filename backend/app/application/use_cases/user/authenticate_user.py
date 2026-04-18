from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.email_address import EmailAddress
from application.dtos.user.authenticate_user_command import AuthenticateUserCommand
from application.dtos.user.authentication_result import AuthenticationResult
from application.exceptions.auth_exceptions import InvalidCredentialsError, InactiveUserError
from application.interfaces.password_hasher import IPasswordHasher
from application.interfaces.token_service import ITokenService

class AuthenticateUser:
    def __init__(
        self,
        repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self.repo = repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, command: AuthenticateUserCommand) -> AuthenticationResult:
        email = EmailAddress(command.email)

        user = await self.repo.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Invalid credentials")
        
        if not user.active:
            raise InactiveUserError("Inactive user")
        
        if not self.password_hasher.verify(command.password, user.password_hash):
            raise InvalidCredentialsError("Invalid credentials")
        
        access_token = self.token_service.create_access_token(
            subject = str(user.id),
            email = str(user.email),
            access_level = user.access_level.value,
        )

        return AuthenticationResult(access_token=access_token)
