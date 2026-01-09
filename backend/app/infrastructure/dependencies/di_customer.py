from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.customer_repository import ICustomerRepository
from application.use_cases.customer.create_customer import CreateCustomer
from application.use_cases.customer.delete_customer import DeleteCustomer
from application.use_cases.customer.get_all_customers import GetAllCustomers
from application.use_cases.customer.get_customer import GetCustomer
from application.use_cases.customer.update_customer import UpdateCustomer
from infrastructure.repositories.customer_repository_postgres import CustomerRepositoryPostgres

class DICustomer:
    def build(
        self,
        session: AsyncSession
    ) -> tuple[
        CreateCustomer,
        GetCustomer,
        GetAllCustomers,
        DeleteCustomer,
        UpdateCustomer,
    ]:
        repo = CustomerRepositoryPostgres(session)

        return (
            CreateCustomer(repo),
            GetCustomer(),
            GetAllCustomers(),
            DeleteCustomer(),
            UpdateCustomer(),
        )

        # def get_user_repository(self, session: AsyncSession) -> ICustomerRepository:
        #     return CustomerRepositoryPostgres(session)
        
        # def get_create_customer_service(self, session: AsyncSession) -> CreateCustomer:
        #     return CreateCustomer(self.get_user_repository(session))

di_customer = DICustomer()
