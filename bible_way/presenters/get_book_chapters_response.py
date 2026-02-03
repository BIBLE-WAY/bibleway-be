from rest_framework.response import Response
from rest_framework import status


class GetBookChaptersResponse:

    @staticmethod
    def chapters_retrieved_successfully_response(chapters_data: list, category_id: str = None, category_name: str = None) -> Response:
        return Response(
            {
                "success": True,
                "message": "Chapters retrieved successfully",
                "category_id": category_id,
                "category_name": category_name,
                "data": chapters_data
            },
            status=status.HTTP_200_OK
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
