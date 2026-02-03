from bible_way.storage import UserDB
from bible_way.presenters.get_chapter_metadata_response import GetChapterMetadataResponse
from bible_way.models import Reaction
from rest_framework.response import Response
import uuid


class GetChapterMetadataInteractor:
    def __init__(self, storage: UserDB, response: GetChapterMetadataResponse):
        self.storage = storage
        self.response = response

    def get_chapter_metadata_interactor(self, chapter_id: str, user_id: str = None) -> Response:
        if not chapter_id or (isinstance(chapter_id, str) and not chapter_id.strip()):
            return self.response.validation_error_response("Chapter ID is required")
        
        chapter_id = chapter_id.strip()
        
        try:
            chapter = self.storage.get_chapter_by_id(chapter_id)
            
            if not chapter:
                return self.response.chapter_not_found_response()
            
            metadata = chapter.metadata if chapter.metadata else {}
            
            # Get like count
            like_count = Reaction.objects.filter(
                chapter=chapter,
                reaction_type=Reaction.LIKE
            ).count()
            
            # Check if user liked the chapter
            is_liked = False
            if user_id:
                try:
                    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
                    is_liked = Reaction.objects.filter(
                        chapter=chapter,
                        user__user_id=user_uuid,
                        reaction_type=Reaction.LIKE
                    ).exists()
                except (ValueError, TypeError):
                    pass
            
            data = {
                "chapter_id": str(chapter.chapter_id),
                "metadata": metadata,
                "like_count": like_count,
                "is_liked": is_liked
            }
            
            return self.response.metadata_retrieved_successfully_response(data)
        except Exception as e:
            return self.response.error_response(f"Failed to retrieve chapter metadata: {str(e)}")

