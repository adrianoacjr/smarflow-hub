from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import get_session
from infrastructure.dependencies.di_conversation import (
    get_conversation_repository,
    get_escalate_conversation,
    get_resolve_conversation,
)
from application.use_cases.conversation.escalate_conversation import EscalateConversation
from application.use_cases.conversation.resolve_conversation import ResolveConversation
from application.dtos.conversation.escalate_conversation_command import EscalateConversationCommand
from domain.enums.conversation_status import ConversationStatus
from adapters.dtos.conversation_dto import (
    ConversationResponseDTO,
    ConversationListResponseDTO,
    EscalateConversationRequestDTO,
)

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.get("", response_model=ConversationListResponseDTO)
async def list_conversations(
    client_id: int,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    repo = get_conversation_repository(session)
    conversations = await repo.list(client_id, limit=limit, offset=offset)
    return ConversationListResponseDTO(
        conversation=[ConversationResponseDTO.model_validate(c) for c in conversations],
        total=len(conversations),
    )

@router.get("/by-status", response_model=ConversationListResponseDTO)
async def list_by_status(
    client_id: int,
    conversation_status: ConversationStatus,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    repo = get_conversation_repository(session)
    conversations = await repo.list_by_status(client_id, conversation_status, limit=limit, offset=offset)
    return ConversationListResponseDTO(
        conversations=[ConversationResponseDTO.model_validate(c) for c in conversations],
        total=len(conversations),
    )

@router.get("/by-customer", response_model=ConversationListResponseDTO)
async def list_by_customer(
    client_id: int,
    customer_id: int,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    repo = get_conversation_repository(session)
    conversations = await repo.list_by_customer(client_id, customer_id, limit=limit, offset=offset)
    return ConversationListResponseDTO(
        conversations=[ConversationListResponseDTO.model_validate(c) for c in conversations],
        total=len(conversations),
    )

@router.get("/{conversation_id}", response_model=ConversationResponseDTO)
async def get_conversations(
    client_id: int,
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    repo = get_conversation_repository(session)
    conversation = await repo.get_by_id(client_id, conversation_id)
    if conversation is None:
        from application.exceptions.conversation_exceptions import ConversationNotFoundError
        raise ConversationNotFoundError(f"Conversation '{conversation_id}' not found")
    return ConversationResponseDTO.model_validate(conversation)

@router.post("/{conversation_id}/escalate", reponse_model=ConversationResponseDTO)
async def escalate_conversation(
    conversation_id: UUID,
    body: EscalateConversationRequestDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case: EscalateConversation = get_escalate_conversation(session)
    command = EscalateConversationCommand(
        conversation_id=conversation_id,
        reason=body.reason,
    )
    conversation = await use_case.execute(command)
    return ConversationResponseDTO.model_validate(conversation)

@router.post("/{conversation_id}/resolve", response_model=ConversationResponseDTO, status_code=status.HTTP_200_OK)
async def resolve_conversation(
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    use_case: ResolveConversation = get_resolve_conversation(session)
    conversation = await use_case.execute(conversation_id)
    return ConversationResponseDTO.model_validate(conversation)
