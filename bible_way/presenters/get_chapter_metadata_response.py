from rest_framework.response import Response
from rest_framework import status


class GetChapterMetadataResponse:

    @staticmethod
    def metadata_retrieved_successfully_response(data: dict) -> Response:
        return Response(
            {
                "success": True,
                "message": "Chapter metadata retrieved successfully",
                "data": data
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
    def chapter_not_found_response() -> Response:
        return Response(
            {
                "success": False,
                "error": "Chapter not found",
                "error_code": "CHAPTER_NOT_FOUND"
            },
            status=status.HTTP_404_NOT_FOUND
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

