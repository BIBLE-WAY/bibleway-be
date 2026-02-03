from rest_framework.response import Response
from rest_framework import status


class CreateChapterFeedbackResponse:

    @staticmethod
    def feedback_created_successfully_response(feedback_id: str, chapter_id: str, rating: int) -> Response:
        return Response(
            {
                "success": True,
                "message": "Feedback created successfully",
                "feedback_id": feedback_id,
                "chapter_id": chapter_id,
                "rating": rating
            },
            status=status.HTTP_201_CREATED
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
    def invalid_rating_response() -> Response:
        return Response(
            {
                "success": False,
                "error": "Rating must be between 1 and 5",
                "error_code": "INVALID_RATING"
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

