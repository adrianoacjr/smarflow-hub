from domain.entities.user import User
from domain.enums.access_level import AccessLevel
from domain.value_objects.email_address import EmailAddress
from infrastructure.orm.user_orm import UserORM

class UserMapper:
    @staticmethod
    def orm_to_domain(orm: UserORM) -> User:
        domain = User(
            id=orm.id,
            name=orm.name,
            email=EmailAddress(orm.email),
            password_hash=orm.password_hash,
            access_level=AccessLevel(orm.access_level),
            created_at=orm.created_at,
            active=orm.active
        )
        return domain
    
    @staticmethod
    def domain_to_orm(domain: User) -> UserORM:
        orm = UserORM(
            id=domain.id,
            name=domain.name,
            email=domain.email,
            password_hash=domain.password_hash,
            access_level=domain.access_level,
            created_at=domain.created_at,
            active=domain.active
        )
        return orm
