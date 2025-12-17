from fastapi import APIRouter, Depends, HTTPException, status

from application.integration.generate_ai_reply import GenerateAIReply

from presentation.dtos.gpt_dto import GPTRequestDTO, GPTResponseDTO
from presentation.dependencies.di_ai import di_ai

router = APIRouter()

@router.post("",response_model=GPTRequestDTO,status_code=status.HTTP_200_OK)
async def generate_gpt_response(data: GPTRequestDTO, service: GenerateAIReply = Depends(di_ai.get_generate_ai_reply_service)):
    try:
        result = await service.generate_reply(data.message)
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
