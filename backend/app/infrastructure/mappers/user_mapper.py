from domain.entities.user import User
from domain.enums.access_level import AccessLevel
from domain.enums.user_type import UserType
from domain.value_objects.email_address import EmailAddress
from infrastructure.orm.user_orm import UserORM

class UserMapper:
    @staticmethod
    def orm_to_domain(orm: UserORM) -> User:
        return User(
            id=orm.id,
            name=orm.name,
            email=EmailAddress(orm.email),
            password_hash=orm.password_hash,
            access_level=AccessLevel(orm.access_level),
            user_type=UserType(orm.user_type),
            created_at=orm.created_at,
            active=orm.active,
        )
    
    @staticmethod
    def domain_to_orm(domain: User) -> UserORM:
        return UserORM(
            id=domain.id,
            name=domain.name,
            email=domain.email.value,
            password_hash=domain.password_hash,
            access_level=domain.access_level.value,
            user_type=domain.user_type.value,
            created_at=domain.created_at,
            active=domain.active,
        )

