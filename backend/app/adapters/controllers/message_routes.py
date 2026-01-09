from fastapi import APIRouter, HTTPException
from typing import List

from application.dtos.message_dto import MessageCreateDTO, MessageResponseDTO
from application.use_cases.message.create_message import CreateMessage
from application.use_cases.message.get_message_by_id import GetMessageById
from application.use_cases.message.list_message_by_user import ListMessageByUser
from application.use_cases.message.list_message_by_customer import ListMessageByCustomer
from application.use_cases.message.delete_message import DeleteMessage

def build_message_router(
    create_message: CreateMessage,
    get_message_by_id: GetMessageById,
    list_message_by_user: ListMessageByUser,
    list_message_by_customer: ListMessageByCustomer,
    delete_message: DeleteMessage,
) -> APIRouter:
    router = APIRouter()

    @router.post("/messages/", response_model=MessageResponseDTO)
    def create(message_input: MessageCreateDTO):
        pass

    @router.get("/messages/{message_id}", response_model=MessageResponseDTO)
    def get_by_id(message_id: int):
        pass

    @router.get("/users/{user_id}", response_model=List[MessageResponseDTO])
    def list_by_user(user_id: int):
        pass

    @router.get("/users/{customer_id}", response_model=List[MessageResponseDTO])
    def list_by_customer(customer_id: int):
        pass

    @router.get("/users/{user_id}", status_code=204)
    def delete(user_id: int):
        pass

    return router
