from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.customer_repository import ICustomerRepository

from application.use_cases.customer.create_customer import CreateCustomer

from infrastructure.repositories.customer_repository_postgres import CustomerRepositoryPostgres

class DICustomer:
    def get_user_repository(self, session: AsyncSession) -> ICustomerRepository:
        return CustomerRepositoryPostgres(session)
    
    def get_create_customer_service(self, session: AsyncSession) -> CreateCustomer:
        return CreateCustomer(self.get_user_repository(session))

di_customer = DICustomer()
