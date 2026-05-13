from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dtos.message_dto import MessageCreateDTO, MessageResponseDTO
from infrastructure.database import get_session
from infrastructure.dependencies.di_message import (
    get_create_message,
    get_get_message_by_id,
    get_list_messages_by_user,
    get_list_messages_by_customer,
    get_delete_message,
)

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=MessageResponseDTO, status_code=201)
async def create(
    body: MessageCreateDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_create_message(session)
    msg = await use_case.execute(
        user_id=body.user_id,
        customer_id=body.customer_id,
        content=body.content,
        direction=body.direction,
        source=body.direction,
        automated=body.automated,
        status=body.status,
    )
    return MessageResponseDTO.from_domain(msg)

@router.get("/{message_id}", response_model=MessageResponseDTO)
async def get_by_id(
    message_id: int,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_get_message_by_id(session)
    msg = await use_case.execute(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageResponseDTO.from_domain(msg)

@router.get("/by-user/{user_id}", response_model=list[MessageResponseDTO])
async def list_by_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_list_messages_by_user(session)
    msgs = await use_case.execute(user_id)
    return [MessageResponseDTO.from_domain(m) for m in msgs]

@router.get("/by-customer/{customer_id}", response_model=list[MessageResponseDTO])
async def list_by_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_list_messages_by_customer(session)
    msgs = await use_case.execute(customer_id)
    return [MessageResponseDTO.from_domain(m) for m in msgs]

@router.delete("/{message_id}", status_code=204)
async def delete(
    message_id: int,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_delete_message(session)
    await use_case.execute(message_id)
