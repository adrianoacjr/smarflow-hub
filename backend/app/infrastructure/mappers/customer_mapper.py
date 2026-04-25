from domain.entities.customer import Customer
from domain.enums.customer_origin import CustomerOrigin
from domain.enums.message_source import MessageSource
from domain.value_objects.customer_tag import CustomerTag
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from infrastructure.orm.customer_orm import CustomerORM

class CustomerMapper:
    @staticmethod
    def orm_to_domain(orm: CustomerORM) -> Customer:
        return Customer(
            id=orm.id,
            name=orm.name, 
            email=EmailAddress(orm.email) if orm.email else None,
            phone=PhoneNumber(orm.phone) if orm.phone else None,
            origin=CustomerOrigin(orm.origin),
            source=MessageSource(orm.source) if orm.source else None,
            source_ref=orm.source_ref,
            tags=[CustomerTag(t) for t in (orm.tags or [])],
            created_at=orm.created_at,
        )

    @staticmethod
    def domain_to_orm(domain: Customer) -> CustomerORM:
        return CustomerORM(
            id=domain.id,
            name=domain.name,
            email=domain.email.value if domain.email else None,
            phone=domain.phone.value if domain.phone else None,
            origin=domain.origin.value,
            source=domain.source.value if domain.source else None,
            source_ref=domain.source_ref,
            tags=[t.value for t in domain.tags] if domain.tags else [],
            created_at=domain.created_at,
        )
