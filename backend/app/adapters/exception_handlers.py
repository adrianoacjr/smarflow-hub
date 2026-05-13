from fastapi import Request
from fastapi.responses import JSONResponse

from application.exceptions.message_exceptions import (
    MessageValidationError,
    CustomerNotFoundError,
    MessageNotFoundError,
    InvalidMessageFlowError,
    MessageDeliveryError,
    InvalidMessageStatusTransitionError,
)
from application.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UnauthenticatedUserError,
    InactiveUserError,
    SamePasswordError,
    InvalidCredentialsError,
    InvalidPasswordError,
)
from application.exceptions.client_exceptions import (
    ClientNotFoundError,
    ClientAlreadyExistsError,
    ClientInactiveError,
    InvalidClientPlanError,
)
from application.exceptions.conversation_exceptions import (
    ConversationNotFoundError,
    ConversationAlreadyResolvedError,
    ConversationInvalidTransitionError,
    AgentNotAvailableError,
)

def register_exception_handlers(app) -> None:
    @app.exception_handler(MessageNotFoundError)
    @app.exception_handler(CustomerNotFoundError)
    @app.exception_handler(UserNotFoundError)
    @app.exception_handler(ClientNotFoundError)
    @app.exception_handler(ConversationNotFoundError)
    async def not_found_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    
    @app.exception_handler(MessageValidationError)
    @app.exception_handler(InvalidMessageFlowError)
    @app.exception_handler(InvalidMessageStatusTransitionError)
    @app.exception_handler(ConversationAlreadyResolvedError)
    @app.exception_handler(ConversationInvalidTransitionError)
    @app.exception_handler(AgentNotAvailableError)
    async def validation_error_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
    
    @app.exception_handler(UserAlreadyExistsError)
    @app.exception_handler(ClientAlreadyExistsError)
    @app.exception_handler(ClientInactiveError)
    @app.exception_handler(InvalidClientPlanError)
    async def conflict_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidCredentialsError)
    @app.exception_handler(InactiveUserError)
    @app.exception_handler(UnauthenticatedUserError)
    @app.exception_handler(SamePasswordError)
    @app.exception_handler(InvalidPasswordError)
    async def unauthorized_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    
    @app.exception_handler(MessageDeliveryError)
    async def delivery_error_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=502, content={"detail": str(exc)})
