from bible_way.storage import UserDB
from bible_way.presenters.get_post_by_id_response import GetPostByIdResponse
from rest_framework.response import Response


class GetPostByIdInteractor:
    def __init__(self, storage: UserDB, response: GetPostByIdResponse):
        self.storage = storage
        self.response = response

    def get_post_by_id_interactor(self, post_id: str, current_user_id: str | None = None) -> Response:
        if not post_id or not post_id.strip():
            return self.response.validation_error_response("post_id is required")
        
        post_id = post_id.strip()
        
        try:
            post_data = self.storage.get_post_by_id_with_counts(post_id=post_id, current_user_id=current_user_id)
            
            if not post_data:
                return self.response.post_not_found_response()
            
            return self.response.post_retrieved_successfully_response(post_data=post_data)
        except Exception as e:
            return self.response.error_response(f"Failed to retrieve post: {str(e)}")

