from bible_way.storage import UserDB
from bible_way.presenters.admin.delete_promotion_response import DeletePromotionResponse
from rest_framework.response import Response


class DeletePromotionInteractor:
    def __init__(self, storage: UserDB, response: DeletePromotionResponse):
        self.storage = storage
        self.response = response

    def delete_promotion_interactor(self, promotion_id: str) -> Response:
        if not promotion_id or not promotion_id.strip():
            return self.response.validation_error_response("promotion_id is required")
        
        promotion_id = promotion_id.strip()
        
        try:
            promotion = self.storage.get_promotion_by_id(promotion_id)
            if not promotion:
                return self.response.promotion_not_found_response()
            
            self.storage.delete_promotion(promotion_id)
            
            return self.response.promotion_deleted_successfully_response(promotion_id)
            
        except Exception as e:
            error_message = str(e)
            if "not found" in error_message.lower():
                return self.response.promotion_not_found_response()
            return self.response.error_response(f"Failed to delete promotion: {error_message}")

