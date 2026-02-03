from bible_way.storage import UserDB
from bible_way.presenters.unlike_chapter_response import UnlikeChapterResponse
from rest_framework.response import Response


class UnlikeChapterInteractor:
    def __init__(self, storage: UserDB, response: UnlikeChapterResponse):
        self.storage = storage
        self.response = response

    def unlike_chapter_interactor(self, chapter_id: str, user_id: str) -> Response:
        if not chapter_id:
            return self.response.validation_error_response("Chapter ID is required")
        
        try:
            self.storage.unlike_chapter(chapter_id=chapter_id, user_id=user_id)
            
            return self.response.chapter_unliked_successfully_response(chapter_id=chapter_id)
        except Exception as e:
            error_message = str(e)
            if "not found" in error_message.lower():
                return self.response.chapter_not_found_response()
            if "haven't liked" in error_message.lower():
                return self.response.not_liked_response()
            return self.response.error_response(f"Failed to unlike chapter: {error_message}")

