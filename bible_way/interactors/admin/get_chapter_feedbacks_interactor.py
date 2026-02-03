from bible_way.storage import UserDB
from bible_way.presenters.admin.get_chapter_feedbacks_response import AdminGetChapterFeedbacksResponse
from rest_framework.response import Response


class AdminGetChapterFeedbacksInteractor:
    def __init__(self, storage: UserDB, response: AdminGetChapterFeedbacksResponse):
        self.storage = storage
        self.response = response

    def get_chapter_feedbacks_interactor(self) -> Response:
        try:
            result = self.storage.get_all_chapter_feedbacks_admin()
            
            return self.response.feedbacks_retrieved_successfully_response(
                total_feedbacks=result['total_feedbacks'],
                total_books=result['total_books'],
                books_data=result['books']
            )
        except Exception as e:
            return self.response.error_response(f"Failed to retrieve chapter feedbacks: {str(e)}")

