from domain.interfaces.message_repository import IMessageRepository
from domain.interfaces.user_repository import IUserRepository
from application.dtos.message.list_messages_query import ListMessagesByUserQuery
from application.dtos.message.message_list_result import MessageListResult
from application.exceptions.message_exceptions import UserNotFoundError

class ListMessageByUser:
    def __init__(
        self,
        message_repo: IMessageRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.message_repo = message_repo
        self.user_repo = user_repo

    async def execute(self, query: ListMessagesByUserQuery) -> MessageListResult:
        user = await self.user_repo.get_by_id(query.user_id)
        if user is None:
            raise UserNotFoundError(f"User '{query.user_id}' not found")
        
        items = await self.message_repo.list_by_user(
            user_id = query.user_id,
            limit = query.limit,
            offset = query.offset,
        )
        total = await self.message_repo.count_by_user(query.user_id)

        return MessageListResult(
            items = tuple(items),
            total = total,
            limit = query.limit,
            offset = query.offset,
        )
