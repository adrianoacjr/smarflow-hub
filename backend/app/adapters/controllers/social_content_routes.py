from repositories.social_content_repository_fake import SocialContentRepositoryFake
from application.social_content_service import SocialContentService
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
repo = SocialContentRepositoryFake()
service = SocialContentService(repo)

class SocialContentCreate(BaseModel):
    platform: str
    content: str
    timestamp: datetime
    metrics: dict

@router.post("/social_contents/")
def create_social_content(content: SocialContentCreate):
    return service.create_social_content(
        platform=content.platform,
        content=content.content,
        timestamp=content.timestamp,
        metrics=content.metrics
    )

@router.get("/social_contents/{content_id}")
def get_social_content(content_id: int):
    social_content = service.get_message(content_id)
    if not social_content:
        raise HTTPException(status_code=404, detail="Social content not found")
    return {
        "id": social_content.id,
        "platform": social_content.platform,
        "content": social_content.content,
        "timestamp": social_content.timestamp,
        "metrics": social_content.metrics
    }
