from domain.entities.message import Message
from application.use_cases.integration.generate_ai_reply import GenerateAIReply
from backend.app.application.use_cases.message.queue_outbound_message import SaveOutboundMessage

class ProcessAIReply:
    def __init__(self, ai_service: GenerateAIReply, save_outbound_message: SaveOutboundMessage):
        self.ai_service = ai_service
        self.save_outbound_message = save_outbound_message

    async def execute(
            self, *, customer_id: int, inbound_content: str,) -> Message:
        if not inbound_content.strip():
            raise ValueError("Inbound message cannot be empty")
        
        ai_reply = await self.ai_service.generate_reply(inbound_content)

        return await self.save_outbound_message.execute(
            customer_id=customer_id,
            content=ai_reply,
            source="ai",
            automated=True,
            status="sent"
        )
