from functools import lru_cache

from openai import AsyncOpenAI

from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.ai_responder_gateway import IAIResponderGateway
from application.use_cases.message.analyze_message import AnalyzeMessage
from infrastructure.config import settings
from infrastructure.dependencies.di_conversation import (
    get_conversation_repository,
    get_create_conversation,
    get_escalate_conversation,
)
from infrastructure.dependencies.di_message import (
    get_message_repository,
    get_queue_outbound_message,
    get_dispatch_outbound_message,
)
from infrastructure.dependencies.di_user import get_user_repository
from infrastructure.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai
from infrastructure.gateways.openai_client import OpenAIClientFactory

@lru_cache(maxsize=1)
def get_openai_client() -> AsyncOpenAI:
    return OpenAIClientFactory.create()

def get_ai_gateway() -> IAIResponderGateway:
    return AIResponderGatewayOpenai(
        client=get_openai_client(),
        model=settings.OPENAI_MODEL,
        system_prompt=settings.OPENAI_SYSTEM_PROMPT,
    )

def get_analyze_message(session: AsyncSession) -> AnalyzeMessage:
    return AnalyzeMessage(
        message_repo=get_message_repository(session),
        ai_gateway=get_ai_gateway(),
        conversation_repo=get_conversation_repository(session),
        queue_outbound=get_queue_outbound_message(session),
        create_conversation=get_create_conversation(session),
        escalate_conversation=get_escalate_conversation(session),
        dispatch_outboud=get_dispatch_outbound_message(session),
        user_repo=get_user_repository(session),
        default_system_prompt=settings.OPENAI_SYSTEM_PROMPT,
    )
