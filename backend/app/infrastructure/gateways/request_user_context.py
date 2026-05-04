from typing import Optional

from application.interfaces.user_context import IUserContext
from application.interfaces.token_service import ITokenService

class RequestUserContext(IUserContext):
    def __init__(self, token: str, token_service: ITokenService) -> None:
        self._token = token
        self._token_service = token_service
        self._payload: Optional[dict] = None

    def _get_payload(self) -> dict:
        if self._payload is None:
            self._payload = self._token_service.verify_access_token(self._token)
        return self._payload
    
    @property
    def user_id(self) -> Optional[int]:
        try:
            raw = self._get_payload().get("sub")
            return int(raw) if raw is not None else None
        except (ValueError, TypeError):
            return None
        
    @property
    def access_level(self) -> Optional[str]:
        return self._get_payload().get("access_level")
    
    @property
    def user_type(self) -> Optional[str]:
        return self._get_payload().get("user_type")
