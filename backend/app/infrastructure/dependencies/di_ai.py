from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.message.analyze_message import AnalyzeMessage
from infrastructure.dependencies.di_conversation import (
    get_create_conversation,
    get_escalate_conversation,
)
from infrastructure.dependencies.di_message import (
    get_message_repository,
    get_queue_outbound_message,
)
from infrastructure.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai
from infrastructure.gateways.openai_client import OpenAIClientFactory


def get_ai_gateway() -> AIResponderGatewayOpenai:
    return AIResponderGatewayOpenai(client=OpenAIClientFactory.create())


def get_analyze_message(session: AsyncSession) -> AnalyzeMessage:
    return AnalyzeMessage(
        message_repo=get_message_repository(session),
        ai_gateway=get_ai_gateway(),
        queue_outbound=get_queue_outbound_message(session),
        create_conversation=get_create_conversation(session),
        escalate_conversation=get_escalate_conversation(session),
    )
