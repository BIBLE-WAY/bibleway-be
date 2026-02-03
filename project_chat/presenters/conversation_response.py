"""
Presenter for conversation-related responses.
"""

from typing import Dict, Any, List
from rest_framework.response import Response
from rest_framework import status
from project_chat.models import Conversation, ConversationMember
from bible_way.utils.s3_url_helper import get_presigned_url as get_bible_way_presigned_url


class ConversationResponse:
    """Response formatter for conversation operations."""
    
    @staticmethod
    def conversation_details_response(
        conversation: Conversation, 
        members: List[ConversationMember],
        messages: List[dict] = None
    ) -> Dict[str, Any]:
        """Format conversation details response."""
        # Format members
        members_data = []
        for member in members:
            members_data.append({
                'user_id': str(member.user.user_id),
                'user_name': member.user.username,
                'profile_picture_url': get_bible_way_presigned_url(member.user.profile_picture_url) if member.user.profile_picture_url else '',
                'is_admin': member.is_admin,
                'joined_at': member.joined_at.isoformat() if member.joined_at else None,
                'last_read_at': member.last_read_at.isoformat() if member.last_read_at else None
            })
        
        # Format conversation
        conversation_data = {
            'conversation_id': conversation.id,
            'type': conversation.type,
            'name': conversation.name or '',
            'description': conversation.description or '',
            'image': get_bible_way_presigned_url(conversation.image.url) if conversation.image and conversation.image.url else '',
            'created_by': {
                'user_id': str(conversation.created_by.user_id),
                'user_name': conversation.created_by.username,
                'profile_picture_url': get_bible_way_presigned_url(conversation.created_by.profile_picture_url) if conversation.created_by and conversation.created_by.profile_picture_url else ''
            } if conversation.created_by else None,
            'is_active': conversation.is_active,
            'created_at': conversation.created_at.isoformat() if conversation.created_at else None,
            'updated_at': conversation.updated_at.isoformat() if conversation.updated_at else None,
            'members': members_data,
            'members_count': len(members_data),
            'messages': messages or [],
            'messages_count': len(messages) if messages else 0
        }
        
        return {
            'success': True,
            'data': conversation_data
        }

