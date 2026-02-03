from rest_framework.response import Response
from rest_framework import status


class AdminGetChapterFeedbacksResponse:

    @staticmethod
    def feedbacks_retrieved_successfully_response(total_feedbacks: int, total_books: int, books_data: list) -> Response:
        return Response(
            {
                "success": True,
                "message": "Chapter feedbacks retrieved successfully",
                "data": {
                    "total_feedbacks": total_feedbacks,
                    "total_books": total_books,
                    "books": books_data
                }
            },
            status=status.HTTP_200_OK
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

