from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.client.create_client import CreateClient
from application.use_cases.client.get_client import GetClient
from application.use_cases.client.get_all_clients import GetAllClients
from application.use_cases.client.update_client import UpdateClient
from application.use_cases.client.change_client_plan import ChangeClientPlan
from application.use_cases.client.deactivate_client import DeactivateClient
from application.use_cases.client.delete_client import DeleteClient
from infrastructure.repositories.client_repository_postgres import (
    ClientRepositoryPostgres,
)

def get_client_repository(session: AsyncSession) -> ClientRepositoryPostgres:
    return ClientRepositoryPostgres(session)

def get_create_client(session: AsyncSession) -> CreateClient:
    return CreateClient(repo=get_client_repository(session))

def get_get_client(session: AsyncSession) -> GetClient:
    return GetClient(repo=get_client_repository(session))

def get_get_all_clients(session: AsyncSession) -> GetAllClients:
    return GetAllClients(repo=get_client_repository(session))

def get_update_client(session: AsyncSession) -> UpdateClient:
    return UpdateClient(repo=get_client_repository(session))

def get_change_client_plan(session: AsyncSession) -> ChangeClientPlan:
    return ChangeClientPlan(repo=get_client_repository(session))

def get_deactivate_client(session: AsyncSession) -> DeactivateClient:
    return DeactivateClient(repo=get_client_repository(session))

def get_delete_client(session: AsyncSession) -> DeleteClient:
    return DeleteClient(repo=get_client_repository(session))
