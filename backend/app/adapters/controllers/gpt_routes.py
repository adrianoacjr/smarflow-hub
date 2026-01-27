from fastapi import APIRouter, HTTPException, status

from adapters.dtos.gpt_dto import GPTRequestDTO, GPTResponseDTO
from application.use_cases.integration.process_ai_reply import ProcessAIReply

def build_gpt_router(
    process_ai_reply: ProcessAIReply,
) -> APIRouter:
    router = APIRouter()

    @router.post("/gpt", response_model=GPTResponseDTO, status_code=status.HTTP_200_OK)
    async def generate_gpt_response(data: GPTRequestDTO):
        try:
            result = await process_ai_reply.execute(
                customer_id=data.customer_id,
                inbound_content=data.message,
            )
            return GPTResponseDTO(response=result.content)
        
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

    return router
