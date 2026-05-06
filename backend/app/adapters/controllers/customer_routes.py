from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dtos.customer_dto import CustomerCreateDTO, CustomerResponseDTO
from infrastructure.database import get_session
from infrastructure.dependencies.di_customer import (
    get_create_customer,
    get_get_customer,
    get_get_all_customers,
    get_update_customer,
    get_delete_customer,
)

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponseDTO, status_code=201)
async def create(
    body: CustomerCreateDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_create_customer(session)
    customer = await use_case.execute(
        body.name, body.email, body.phone, body.origin
    )
    return CustomerResponseDTO.from_domain(customer)

@router.get("/{customer_id}", response_model=CustomerResponseDTO)
async def get_one(
    customer_id: int,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_get_customer(session)
    customer = await use_case.execute(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponseDTO.from_domain(customer)

@router.delete("/{customer_id}", status_code=204)
async def delete(
    customer_id: int,
    session: AsyncSession = Depends(get_session)
):
    use_case = get_delete_customer(session)
    await use_case.execute(customer_id)
