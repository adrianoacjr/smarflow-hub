from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import get_session
from infrastructure.dependencies.di_client import (
    get_create_client,
    get_get_client,
    get_get_all_clients,
    get_update_client,
    get_change_client_plan,
    get_deactivate_client,
    get_delete_client,
)
from application.use_cases.client.create_client import CreateClient
from application.use_cases.client.get_client import GetClient
from application.use_cases.client.get_all_clients import GetAllClients
from application.use_cases.client.update_client import UpdateClient
from application.use_cases.client.change_client_plan import ChangeClientPlan
from application.use_cases.client.deactivate_client import DeactivateClient
from application.use_cases.client.delete_client import DeleteClient
from application.dtos.client.create_client_command import CreateClientCommand
from application.exceptions.client_exceptions import ClientAlreadyExistsError
from adapters.dtos.client_dto import (
    ClientCreateRequestDTO,
    ClientResponseDTO,
    ClientListResponseDTO,
    ClientUpdateRequestDTO,
    ClientChangePlanRequestDTO,
    ClientCreateResponseDTO,
)

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientCreateRequestDTO)
async def create_client(
    body: ClientCreateRequestDTO,
    session: AsyncSession = Depends(get_session)
):
    use_case: CreateClient = get_create_client(session)
    try:
        command = CreateClientCommand(
            name=body.name,
            email=body.email,
            plan=body.plan,
        )
        client, raw_api_key = await use_case.execute(command)
        return ClientCreateResponseDTO(
            id=client.id,
            name=client.name,
            email=str(client.email),
            plan=client.plan,
            is_active=client.active,
            created_at=client.created_at,
            api_key=raw_api_key,
        )
    except ClientAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
@router.get("", response_model=ClientListResponseDTO)
async def list_clients(
    session: AsyncSession = Depends(get_session),
):
    use_case: GetAllClients = get_get_all_clients(session)
    clients = await use_case.execute()
    return ClientListResponseDTO(
        clients=[
            ClientListResponseDTO(
                id=c.id,
                name=c.name,
                emai=str(c.email),
                plan=c.plan,
                is_active=c.is_active,
                created_at=c.created_at,
            )
            for c in clients
        ]
    )

@router.get("/{client_id}", response_model=ClientResponseDTO)
async def get_client(
    client_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    use_case: GetClient = get_get_client(session)
    client = await use_case.execute(client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return ClientResponseDTO(
        id=client.id,
        name=client.name,
        email=str(client.email),
        plan=client.plan,
        is_active=client.active,
        created_at=client.created_at,
    )

@router.patch("/{client_id}", response_model=ClientResponseDTO)
async def update_client(
    client_id: UUID,
    body: ClientUpdateRequestDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case: UpdateClient = get_update_client(session)
    client = await use_case.execute(client_id, body.name, body.email)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return ClientResponseDTO(
        id=client.id,
        name=client.name,email=str(client.email),
        plan=client.plan,
        is_active=client.active,
        created_at=client.created_at,
    )

@router.patch("/{client_id}/plan", response_model=ClientResponseDTO)
async def change_plan(
    client_id: UUID,
    body: ClientChangePlanRequestDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case: ChangeClientPlan = get_change_client_plan(session)
    client = await use_case.execute(client_id, body.plan)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return ClientResponseDTO(
        id=client.id,
        name=client.name,
        email=str(client.email),
        plan=client.plan,
        is_active=client.active,
        created_at=client.created_at,
    )

@router.patch("/{client_id}/deactivate", response_model=ClientResponseDTO)
async def deactivate_client(
    client_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    use_case: DeactivateClient = get_deactivate_client(session)
    client = await use_case.execute(client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return ClientResponseDTO(
        id=client.id,
        name=client.name,
        email=str(client.email),
        plan=client.plan,
        is_active=client.active,
        created_at=client.created_at,
    )

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    use_case: delete_client = get_delete_client(session)
    await use_case.execute(client_id)
