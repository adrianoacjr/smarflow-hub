from presentation.dtos.message_dto import MessageCreateDTO, MessageResponseDTO
from infrastructure.repositories.message_repository_fake import MessageRepositoryFake
from application.message.send_message import SendMessage
from domain.interfaces.message_repository import IMessageRepository
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()
repo = MessageRepositoryFake()

def get_message_repository() -> IMessageRepository:
    return repo

def get_send_message(repo: IMessageRepository = Depends(get_message_repository)):
    return SendMessage(repo)

@router.post("/messages/", response_model=MessageResponseDTO)
def send_message(message_input: MessageCreateDTO, send_message_use_case: SendMessage = Depends(get_send_message)):
    message = send_message_use_case.execute(message_input.user_id, message_input.content, message_input.source)
    return MessageResponseDTO.from_domain(message)
