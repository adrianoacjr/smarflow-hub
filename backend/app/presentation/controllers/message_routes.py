from fastapi import APIRouter, HTTPException, Depends
from typing import List

from domain.models.message import Message

from presentation.dependencies.di_message import di_message
from presentation.dtos.message_dto import MessageCreateDTO, MessageResponseDTO

router = APIRouter()

@router.post("/messages/", response_model=MessageResponseDTO)
def save(message_input: MessageCreateDTO):
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
