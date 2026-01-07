from domain.entities.customer import Customer

from infrastructure.orm.customer_orm import CustomerORM

class CustomerMapper:
    @staticmethod
    def orm_to_domain(orm: CustomerORM) -> Customer:
        domain = Customer(
            id=orm.id,
            name=orm.name, 
            email=orm.email,
            phone=orm.phone,
            origin=orm.origin,
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