from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from application.dtos.user.list_users_query import ListUsersQuery

class ListUsers:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def execute(self, query: ListUsersQuery) -> list[User]:
        limit = max(1, min(query.limit, 100))
        offset = max(0, query.offset)

        return await self.repo.list(limit=limit, offset=offset)
