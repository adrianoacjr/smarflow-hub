from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from presentation.dependencies.di_customer import di_customer
from presentation.dtos.customer_dto import CustomerCreateDTO, CustomerResponseDTO

from application.customer.create_customer import CreateCustomer

from core.database import get_session

router = APIRouter()

@router.post("/customers/", response_model=CustomerResponseDTO)
async def create_customer(customer_input: CustomerCreateDTO, session: AsyncSession = Depends(get_session)):
    service: CreateCustomer = di_customer.get_create_customer_service(session)
    customer = await service.execute(
        customer_input.name,
        customer_input.email,
        customer_input.phone,
        customer_input.origin,
        customer_input.created_at
    )
    return CustomerResponseDTO.from_domain(customer)
