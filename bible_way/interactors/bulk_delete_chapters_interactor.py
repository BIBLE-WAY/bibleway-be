from bible_way.storage import UserDB
from bible_way.presenters.bulk_delete_chapters_response import BulkDeleteChaptersResponse
from rest_framework.response import Response


class BulkDeleteChaptersInteractor:
    def __init__(self, storage: UserDB, response: BulkDeleteChaptersResponse):
        self.storage = storage
        self.response = response

    def bulk_delete_chapters_interactor(self, chapter_ids: list[str]) -> Response:
        # Validate chapter_ids is provided
        if not chapter_ids:
            return self.response.validation_error_response("chapter_ids is required and must be a non-empty list")
        
        # Validate it's a list
        if not isinstance(chapter_ids, list):
            return self.response.validation_error_response("chapter_ids must be a list")
        
        # Validate list is not empty
        if len(chapter_ids) == 0:
            return self.response.validation_error_response("chapter_ids list cannot be empty")
        
        # Validate all items are strings
        for chapter_id in chapter_ids:
            if not isinstance(chapter_id, str):
                return self.response.validation_error_response("All chapter_ids must be strings")
        
        try:
            # Perform bulk delete
            result = self.storage.bulk_delete_chapters(chapter_ids=chapter_ids)
            
            deleted_count = result['deleted_count']
            failed_count = result['failed_count']
            deleted_ids = result['deleted_ids']
            failed_ids = result['failed_ids']
            errors = result['errors']
            
            # If all failed, return error response
            if deleted_count == 0:
                return self.response.all_chapters_failed_response(
                    failed_count=failed_count,
                    failed_ids=failed_ids,
                    errors=errors
                )
            
            # If some or all succeeded, return success response
            return self.response.chapters_deleted_successfully_response(
                deleted_count=deleted_count,
                deleted_ids=deleted_ids,
                failed_count=failed_count,
                failed_ids=failed_ids,
                errors=errors
            )
            
        except Exception as e:
            return self.response.error_response(f"Failed to bulk delete chapters: {str(e)}")

