from rest_framework.response import Response
from rest_framework import status


class DeletePromotionResponse:

    @staticmethod
    def promotion_deleted_successfully_response(promotion_id: str) -> Response:
        return Response(
            {
                "success": True,
                "message": "Promotion deleted successfully",
                "promotion_id": promotion_id
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def promotion_not_found_response() -> Response:
        return Response(
            {
                "success": False,
                "error": "Promotion not found",
                "error_code": "PROMOTION_NOT_FOUND"
            },
            status=status.HTTP_404_NOT_FOUND
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

