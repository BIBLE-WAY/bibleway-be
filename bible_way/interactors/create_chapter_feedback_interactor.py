from bible_way.storage import UserDB
from bible_way.presenters.create_chapter_feedback_response import CreateChapterFeedbackResponse
from rest_framework.response import Response


class CreateChapterFeedbackInteractor:
    def __init__(self, storage: UserDB, response: CreateChapterFeedbackResponse):
        self.storage = storage
        self.response = response

    def create_chapter_feedback_interactor(self, chapter_id: str, user_id: str, description: str, rating: int) -> Response:
        if not chapter_id:
            return self.response.validation_error_response("Chapter ID is required")
        
        if not description or not description.strip():
            return self.response.validation_error_response("Feedback description is required")
        
        if rating is None:
            return self.response.validation_error_response("Rating is required")
        
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                return self.response.invalid_rating_response()
        except (ValueError, TypeError):
            return self.response.invalid_rating_response()
        
        try:
            feedback = self.storage.create_chapter_feedback(
                chapter_id=chapter_id,
                user_id=user_id,
                description=description,
                rating=rating_int
            )
            
            return self.response.feedback_created_successfully_response(
                feedback_id=str(feedback.feedback_id),
                chapter_id=chapter_id,
                rating=rating_int
            )
            
        except Exception as e:
            error_message = str(e)
            if "not found" in error_message.lower():
                return self.response.chapter_not_found_response()
            if "rating" in error_message.lower() and ("between" in error_message.lower() or "1" in error_message or "5" in error_message):
                return self.response.invalid_rating_response()
            return self.response.error_response(f"Failed to create feedback: {error_message}")

