from bible_way.storage import UserDB
from bible_way.presenters.create_post_response import CreatePostResponse
from rest_framework.response import Response


class CreatePostInteractor:
    def __init__(self, storage: UserDB, response: CreatePostResponse):
        self.storage = storage
        self.response = response

    def create_post_interactor(self, user_id: str, title: str, description: str, media_files: list) -> Response:
        title = title.strip() if title else ''
        description = description.strip() if description else ''
        
        try:
            post = self.storage.create_post(
                user_id=user_id,
                title=title,
                description=description
            )
            
            if media_files:
                for media_file in media_files:
                    try:
                        if not media_file or not hasattr(media_file, 'name'):
                            continue
                        
                        # Validate file type before processing
                        is_valid, error_message = self.storage.validate_media_file_type(media_file)
                        if not is_valid:
                            return self.response.invalid_media_type_response(media_file.name)
                        
                        media_type = self.storage.get_media_type_from_file(media_file)
                        
                        s3_url = self.storage.upload_file_to_s3(
                            post=post,
                            media_file=media_file,
                            user_id=user_id
                        )
                        
                        self.storage.create_media(
                            post=post,
                            s3_url=s3_url,
                            media_type=media_type
                        )
                    except ValueError as e:
                        # Handle unsupported file type error from _determine_media_type_from_filename
                        return self.response.invalid_media_type_response(media_file.name if hasattr(media_file, 'name') else None)
                    except Exception as e:
                        return self.response.s3_upload_error_response(str(e))
            
            return self.response.post_created_successfully_response(str(post.post_id))
            
        except Exception as e:
            return self.response.validation_error_response(f"Failed to create post: {str(e)}")

