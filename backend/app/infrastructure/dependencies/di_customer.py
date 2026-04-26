from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.customer.create_customer import CreateCustomer
from application.use_cases.customer.delete_customer import DeleteCustomer
from application.use_cases.customer.get_all_customers import GetAllCustomers
from application.use_cases.customer.get_customer import GetCustomer
from application.use_cases.customer.update_customer import UpdateCustomer
from infrastructure.repositories.customer_repository_postgres import CustomerRepositoryPostgres

def get_customer_repository(session: AsyncSession) -> CustomerRepositoryPostgres:
    return CustomerRepositoryPostgres(session)

def get_create_customer(session: AsyncSession) -> CreateCustomer:
    return CreateCustomer(repo=get_customer_repository(session))

def get_get_customer(session: AsyncSession) -> GetCustomer:
    return GetCustomer(customer_repo=get_customer_repository(session))

def get_get_all_customers(session: AsyncSession) -> GetAllCustomers:
    return GetAllCustomers(customer_repo=get_customer_repository(session))

def get_update_customer(session: AsyncSession) -> UpdateCustomer:
    return UpdateCustomer(customer_repo=get_customer_repository(session))

def get_delete_customer(session: AsyncSession) -> DeleteCustomer:
    return DeleteCustomer(customer_repo=get_customer_repository(session))
