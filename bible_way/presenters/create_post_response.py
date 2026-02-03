from rest_framework.response import Response
from rest_framework import status


class CreatePostResponse:

    @staticmethod
    def post_created_successfully_response(post_id: str) -> Response:
        return Response(
            {
                "success": True,
                "message": "Post created successfully",
                "post_id": post_id
            },
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def invalid_media_type_response(filename: str = None) -> Response:
        base_message = "Invalid file format. Only images, videos, and audio files are allowed."
        supported_formats = "Supported formats: Images (jpg, jpeg, png, gif, webp, bmp, svg), Videos (mp4, mov, avi, mkv, webm, flv, wmv, m4v), Audio (mp3, wav, aac, ogg, m4a, flac)"
        
        if filename:
            error_message = f"{base_message} File '{filename}' is not a supported format. {supported_formats}"
        else:
            error_message = f"{base_message} {supported_formats}"
        
        return Response(
            {
                "success": False,
                "error": error_message,
                "error_code": "INVALID_MEDIA_TYPE"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def s3_upload_error_response(error_message: str) -> Response:
        return Response(
            {
                "success": False,
                "error": f"Failed to upload media to S3: {error_message}",
                "error_code": "S3_UPLOAD_ERROR"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
    def no_media_provided_response() -> Response:
        return Response(
            {
                "success": False,
                "error": "At least one media file is required",
                "error_code": "NO_MEDIA_PROVIDED"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

