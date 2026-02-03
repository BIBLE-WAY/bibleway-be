from bible_way.storage import UserDB
from bible_way.presenters.update_profile_response import UpdateProfileResponse
from rest_framework.response import Response
import re


class UpdateProfileInteractor:
    def __init__(self, storage: UserDB, response: UpdateProfileResponse):
        self.storage = storage
        self.response = response

    def update_profile_interactor(self, user_id: str, username: str = None, preferred_language: str = None,
                                  age: int = None, country: str = None, profile_picture_url: str = None) -> Response:
        """
        Update user profile with provided fields
        At least one field must be provided
        """
        
        # Validate that at least one field is provided
        if all(field is None for field in [username, preferred_language, age, country, profile_picture_url]):
            return self.response.validation_error_response("At least one field must be provided to update")
        
        # Validate username if provided
        if username is not None:
            username = username.strip()
            if not username:
                return self.response.validation_error_response("Username cannot be empty")
            
            # Validate username length (Django AbstractUser constraint: max 150 chars)
            if len(username) < 3:
                return self.response.validation_error_response("Username must be at least 3 characters long")
            if len(username) > 150:
                return self.response.validation_error_response("Username must be less than 150 characters")
            
            # Validate username format (alphanumeric, underscore, hyphen only)
            if not re.match(r'^[a-zA-Z0-9_-]+$', username):
                return self.response.validation_error_response("Username can only contain letters, numbers, underscores, and hyphens")
        
        # Validate age if provided
        if age is not None:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 150:
                    return self.response.validation_error_response("Age must be between 1 and 150")
                age = age_int
            except (ValueError, TypeError):
                return self.response.validation_error_response("Age must be a valid integer")
        
        # Validate preferred_language if provided
        if preferred_language is not None and preferred_language:
            if len(preferred_language) < 2 or len(preferred_language) > 50:
                return self.response.validation_error_response("Preferred language must be between 2 and 50 characters")
        
        # Validate country if provided
        if country is not None and country:
            if len(country) < 2 or len(country) > 100:
                return self.response.validation_error_response("Country must be between 2 and 100 characters")
        
        # Validate profile_picture_url if provided (URL comes from S3 upload)
        if profile_picture_url is not None and profile_picture_url:
            if len(profile_picture_url) > 1000:
                return self.response.validation_error_response("Profile picture URL must be less than 1000 characters")
        
        try:
            # Update user profile
            updated_user = self.storage.update_user_profile(
                user_id=user_id,
                username=username,
                preferred_language=preferred_language,
                age=age,
                country=country,
                profile_picture_url=profile_picture_url
            )
            
            if not updated_user:
                return self.response.user_not_found_response()
            
            return self.response.profile_updated_successfully_response(updated_user.profile_picture_url)
            
        except Exception as e:
            error_message = str(e)
            # Handle username uniqueness error specifically
            if "username" in error_message.lower() and ("taken" in error_message.lower() or "already" in error_message.lower()):
                return self.response.validation_error_response("Username is already taken")
            return self.response.error_response(f"Failed to update profile: {error_message}")
