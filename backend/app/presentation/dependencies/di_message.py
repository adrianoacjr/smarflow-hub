from domain.interfaces.message_repository import IMessageRepository

from infrastructure.repositories.message_repository_postgres import MessageRepositoryPostgres

class DIMessage:
    def __init__(self):
        self._repo: IMessageRepository = MessageRepositoryPostgres

    def get_user_repository(self) -> IMessageRepository:
        return self._repo
    
di_message = DIMessage()
