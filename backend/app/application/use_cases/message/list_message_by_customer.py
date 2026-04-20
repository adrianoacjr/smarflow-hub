from domain.interfaces.customer_repository import ICustomerRepository
from domain.interfaces.message_repository import IMessageRepository
from application.dtos.message.list_messages_query import ListMessagesByCustomerQuery
from application.dtos.message.message_list_result import MessageListResult
from application.exceptions.message_exceptions import CustomerNotFoundError

class ListMessageByCustomer:
    def __init__(
        self,
        message_repo: IMessageRepository,
        customer_repo: ICustomerRepository
    ) -> None:
        self.message_repo = message_repo
        self.customer_repo = customer_repo

    async def execute(self, query: ListMessagesByCustomerQuery) -> MessageListResult:
        customer = await self.customer_repo.get_by_id(query.customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{query.customer_id}' not found")
        
        items = await self.message_repo.list_by_customer(
            customer_id = query.customer_id,
            limit = query.limit,
            offset = query.offset,
        )
        total = await self.message_repo.count_by_customer(query.customer_id)

        return MessageListResult(
            items = tuple(items),
            total = total,
            limit = query.limit,
            offset = query.offset,
        )
