from bible_way.storage import UserDB
from bible_way.presenters.get_book_chapters_response import GetBookChaptersResponse
from bible_way.models import Reaction
from rest_framework.response import Response
import uuid


class GetBookChaptersInteractor:
    def __init__(self, storage: UserDB, response: GetBookChaptersResponse):
        self.storage = storage
        self.response = response

    def get_book_chapters_interactor(self, book_id: str, user_id: str = None) -> Response:
        if not book_id or (isinstance(book_id, str) and not book_id.strip()):
            return self.response.validation_error_response("Book ID is required")
        
        try:
            book = self.storage.get_book_by_id(book_id)
        except Exception:
            return self.response.validation_error_response(f"Book with id '{book_id}' does not exist")
        
        # Extract category information from book
        category_id = str(book.category.category_id) if book.category else None
        category_name = book.category.get_category_name_display() if book.category else None
        
        try:
            chapters = self.storage.get_book_chapters(book_id)
            
            # Get all chapter IDs for bulk query
            chapter_ids = [chapter.chapter_id for chapter in chapters]
            
            # Bulk query for like counts
            like_counts = {}
            if chapter_ids:
                from django.db.models import Count
                like_counts_dict = Reaction.objects.filter(
                    chapter__chapter_id__in=chapter_ids,
                    reaction_type=Reaction.LIKE
                ).values('chapter__chapter_id').annotate(count=Count('reaction_id'))
                like_counts = {item['chapter__chapter_id']: item['count'] for item in like_counts_dict}
            
            # Bulk query for user likes if user_id provided
            user_liked_chapters = set()
            if user_id and chapter_ids:
                try:
                    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
                    user_liked_chapters = set(
                        Reaction.objects.filter(
                            chapter__chapter_id__in=chapter_ids,
                            user__user_id=user_uuid,
                            reaction_type=Reaction.LIKE
                        ).values_list('chapter__chapter_id', flat=True)
                    )
                except (ValueError, TypeError):
                    pass
            
            chapters_data = []
            for chapter in chapters:
                chapter_id = chapter.chapter_id
                like_count = like_counts.get(chapter_id, 0)
                is_liked = chapter_id in user_liked_chapters
                
                chapters_data.append({
                    "chapter_id": str(chapter.chapter_id),
                    "book_id": str(chapter.book.book_id),
                    "title": chapter.title,
                    "description": chapter.description,
                    "chapter_number": chapter.chapter_number,
                    "chapter_name": chapter.chapter_name,
                    "chapter_url": chapter.chapter_url,
                    "video_url": chapter.video_url,
                    "like_count": like_count,
                    "is_liked": is_liked,
                    "created_at": chapter.created_at.isoformat() if chapter.created_at else None,
                    "updated_at": chapter.updated_at.isoformat() if chapter.updated_at else None
                })
            
            return self.response.chapters_retrieved_successfully_response(
                chapters_data=chapters_data,
                category_id=category_id,
                category_name=category_name
            )
        except Exception as e:
            return self.response.error_response(f"Failed to retrieve chapters: {str(e)}")
