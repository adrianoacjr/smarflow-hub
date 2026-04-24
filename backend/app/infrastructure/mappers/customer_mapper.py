from domain.entities.customer import Customer
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from domain.enums.customer_origin import CustomerOrigin
from infrastructure.orm.customer_orm import CustomerORM

class CustomerMapper:
    @staticmethod
    def orm_to_domain(orm: CustomerORM) -> Customer:
        domain = Customer(
            id=orm.id,
            name=orm.name, 
            email=EmailAddress(orm.email) if orm.email else None,
            phone=PhoneNumber(orm.phone) if orm.phone else None,
            origin=CustomerOrigin(orm.origin),
            tags=orm.tags,
            created_at=orm.created_at
        )
        return domain
    
    @staticmethod
    def domain_to_orm(domain: Customer) -> CustomerORM:
        orm = CustomerORM(
            id=domain.id,
            name=domain.name,
            email=domain.email,
            phone=domain.phone,
            origin=domain.origin,
            tags=domain.tags,
            created_at=domain.created_at
        )
        return orm