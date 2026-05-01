from domain.interfaces.message_repository import IMessageRepository
from application.dtos.message.list_messages_query import (
    ListMessagesByCustomerQuery,
    ListMessagesByUserQuery,
)
from application.dtos.message.message_list_result import MessageListResult

class GetMessagesByCustomer:
    def __init__(self, message_repo: IMessageRepository) -> None:
        self._message_repo = message_repo

    async def execute(self, query: ListMessagesByCustomerQuery) -> MessageListResult:
        items = await self._message_repo.list_by_customer(
            customer_id=query.customer_id,
            limit=query.limit,
            offset=query.offset,
            order_by_created_asc=True,
        )
        total = await self._message_repo.count_by_customer(query.customer_id)
        return MessageListResult(
            items=tuple(items),
            total=total,
            limit=query.limit,
            offset=query.offset,
        )
    
class GetMessageByUser:
    def __init__(self, message_repo: IMessageRepository) -> None:
        self._message_repo = message_repo

    async def execute(self, query: ListMessagesByCustomerQuery) -> MessageListResult:
        items = await self._message_repo.list_by_user(
            user_id=query.user_id,
            limit=query.limit,
            offset=query.offset,
        )
        total = await self._message_repo.count_by_user(query.user_id)
        return MessageListResult(
            items=tuple(items),
            total=total,
            limit=query.limit,
            offset=query.offset,
        )
