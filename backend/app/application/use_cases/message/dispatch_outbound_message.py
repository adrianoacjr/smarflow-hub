from domain.entities.message import Message
from domain.enums.message_status import MessageStatus
from domain.interfaces.customer_repository import ICustomerRepository
from domain.interfaces.message_repository import IMessageRepository
from application.exceptions.message_exceptions import CustomerNotFoundError, MessageNotFoundError
from application.interfaces.message_gateway import IMessageGateway

class DispatchOutboundMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        customer_repo: ICustomerRepository,
        message_gateway: IMessageGateway,
    ) -> None:
        self._message_repo = message_repo
        self._customer_repo = customer_repo
        self._message_gateway = message_gateway

async def execute(self, message: Message) -> Message:
    customer = await self._customer_repo.get_by_id(message.customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"Customer '{message.customer_id}' not found")

    recipient = customer.source_ref
    if not recipient:
        raise ValueError(f"Customer '{customer.id}' has no source_red to dispatch to")
    
    content = message.content.value if message.content else ""

    try:
        await self._message_gateway.send_message(to=recipient, content=content)
        message.status = MessageStatus.SENT
    except Exception:
        message.status = MessageStatus.FAILED
        await self._message_repo.update(message)
        raise

    return await self._message_repo.update(message)
