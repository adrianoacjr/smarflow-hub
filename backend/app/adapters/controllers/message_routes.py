from fastapi import APIRouter, HTTPException, Depends
from typing import List

from application.dtos.message_dto import MessageCreateDTO, MessageResponseDTO

from infrastructure.dependencies.di_message import di_message

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
