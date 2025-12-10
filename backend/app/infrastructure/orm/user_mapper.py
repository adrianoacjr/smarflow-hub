from domain.models.user import User
from infrastructure.orm.user_orm import UserORM

class UserMapper:
    @staticmethod
    def orm_to_domain(orm: UserORM) -> User:
        return User(
            id=orm.id,
            name=orm.name,
            email=orm.email,
            password_hash=orm.password_hash,
            access_level=orm.access_level,
            created_at=orm.created_at,
            active=orm.active
        )
    
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
