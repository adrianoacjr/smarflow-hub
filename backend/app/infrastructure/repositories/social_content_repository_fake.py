from typing import Optional, List

from models.social_content import SocialContent
from data.social_content_db import fake_social_content_db, get_next_message_id

class SocialContentRepositoryFake:
    def get_by_id(self, content_id: int) -> Optional[SocialContent]:
        return next((c for c in fake_social_content_db if c.id == content_id), None)
    
    def create(self, content: SocialContent) -> SocialContent:
        content.id = get_next_message_id()
        fake_social_content_db.append(content)
        return content
    
    def list_all(self) -> List[SocialContent]:
        return fake_social_content_db
