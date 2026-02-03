from rest_framework.response import Response
from rest_framework import status


class BulkDeleteChaptersResponse:

    @staticmethod
    def chapters_deleted_successfully_response(deleted_count: int, deleted_ids: list, failed_count: int = 0, failed_ids: list = None, errors: list = None) -> Response:
        """Response when chapters are deleted (all or partial success)"""
        if failed_ids is None:
            failed_ids = []
        if errors is None:
            errors = []
        
        message = "Chapters deleted successfully"
        if failed_count > 0:
            message = "Chapters deleted with some failures"
        
        return Response(
            {
                "success": True,
                "message": message,
                "deleted_count": deleted_count,
                "deleted_ids": deleted_ids,
                "failed_count": failed_count,
                "failed_ids": failed_ids,
                "errors": errors
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def all_chapters_failed_response(failed_count: int, failed_ids: list, errors: list) -> Response:
        """Response when all chapters failed to delete"""
        return Response(
            {
                "success": False,
                "error": "No chapters were deleted",
                "error_code": "BULK_DELETE_FAILED",
                "deleted_count": 0,
                "deleted_ids": [],
                "failed_count": failed_count,
                "failed_ids": failed_ids,
                "errors": errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def validation_error_response(error_message: str) -> Response:
        return Response(
            {
                "success": False,
                "error": error_message,
                "error_code": "VALIDATION_ERROR"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def error_response(error_message: str) -> Response:
        return Response(
            {
                "success": False,
                "error": error_message,
                "error_code": "INTERNAL_ERROR"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

