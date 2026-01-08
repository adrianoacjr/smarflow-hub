from fastapi import APIRouter, HTTPException

from application.dtos.customer_dto import CustomerCreateDTO, CustomerResponseDTO
from application.use_cases.customer.create_customer import CreateCustomer
from application.use_cases.customer.delete_customer import DeleteCustomer
from application.use_cases.customer.get_all_customers import GetAllCustomers
from application.use_cases.customer.get_customer import GetCustomer
from application.use_cases.customer.update_customer import UpdateCustomer

def build_customer_router(
    create_customer: CreateCustomer,
    delete_customer: DeleteCustomer,
    get_all_customers: GetAllCustomers,
    get_customer: GetCustomer,
    update_customer: UpdateCustomer,
) -> APIRouter:
    router = APIRouter()

    @router.post("/customers/", response_model=CustomerResponseDTO)
    async def create_customer(customer_input: CustomerCreateDTO):
        customer = await create_customer.execute(
            customer_input.name,
            customer_input.email,
            customer_input.phone,
            customer_input.origin,
            customer_input.created_at
        )
        return CustomerResponseDTO.from_domain(customer)
