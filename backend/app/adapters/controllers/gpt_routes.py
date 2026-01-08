from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.gpt_dto import GPTRequestDTO, GPTResponseDTO
from application.use_cases.integration.process_ai_reply import ProcessAIReply

# from infrastructure.dependencies.di_ai import di_ai

# from core.database import get_session

def build_gpt_router(
    process_ai_reply: ProcessAIReply,
) -> APIRouter:
    router = APIRouter()

    @router.post("/gpt", response_model=GPTRequestDTO, status_code=status.HTTP_200_OK)
    async def generate_gpt_response(data: GPTRequestDTO):
    # async def generate_gpt_response(data: GPTRequestDTO, service: GenerateAIReply = Depends(di_ai.get_generate_ai_reply_service)):
        try:
            # service: ProcessAIReply = di_ai.get_process_ai_reply_service(session)
            # result = await service.generate_reply(data.message)
            result = await process_ai_reply.execute(data.message)
            return GPTResponseDTO(response=result)
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        except RuntimeError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service temporarily enavailable"
            )
