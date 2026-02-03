from bible_way.storage import UserDB
from bible_way.presenters.like_chapter_response import LikeChapterResponse
from rest_framework.response import Response


class LikeChapterInteractor:
    def __init__(self, storage: UserDB, response: LikeChapterResponse):
        self.storage = storage
        self.response = response

    def like_chapter_interactor(self, chapter_id: str, user_id: str) -> Response:
        if not chapter_id:
            return self.response.validation_error_response("Chapter ID is required")
        
        try:
            reaction = self.storage.like_chapter(chapter_id=chapter_id, user_id=user_id)
            
            return self.response.chapter_liked_successfully_response(
                reaction_id=str(reaction.reaction_id),
                chapter_id=chapter_id
            )
        except Exception as e:
            error_message = str(e)
            if "not found" in error_message.lower():
                return self.response.chapter_not_found_response()
            if "already liked" in error_message.lower():
                return self.response.already_liked_response()
            return self.response.error_response(f"Failed to like chapter: {error_message}")

