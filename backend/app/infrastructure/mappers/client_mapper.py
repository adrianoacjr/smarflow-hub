from domain.entities.client import Client
from domain.enums.client_plan import ClientPlan
from domain.value_objects.email_address import EmailAddress
from infrastructure.orm.client_orm import ClientORM

class ClientMapper:
    @staticmethod
    def orm_to_domain(orm: ClientORM) -> Client:
        return Client(
            id=orm.id,
            name=orm.name,
            email=EmailAddress(orm.email),
            plan=ClientPlan(orm.plan),
            api_key_hash=orm.api_key_hash,
            active=orm.active,
            created_at=orm.created_at,
        )
    
    @staticmethod
    def domain_to_orm(domain: Client) -> ClientORM:
        return ClientORM(
            id=domain.id,
            name=domain.name,
            email=domain.email.value,
            plan=domain.plan.value,
            api_key_hash=domain.api_key_hash,
            active=domain.active,
            created_at=domain.created_at,
        )
