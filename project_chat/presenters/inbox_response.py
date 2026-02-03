"""
Presenter for inbox-related responses.
"""

from typing import Dict, Any, List
from rest_framework.response import Response
from rest_framework import status


class InboxResponse:
    """Response formatter for inbox operations."""
    
    @staticmethod
    def inbox_success_response(conversations: List[dict]) -> Dict[str, Any]:
        """Format successful inbox response."""
        return {
            'success': True,
            'data': conversations
        }
    
    @staticmethod
    def error_response(error_message: str) -> Dict[str, Any]:
        """Format error response."""
        return {
            'success': False,
            'error': error_message,
            'error_code': 'INTERNAL_ERROR'
        }
    
    @staticmethod
    def inbox_update_broadcast(conversation_entry: dict) -> Dict[str, Any]:
        """
        Format inbox update broadcast.
        
        Args:
            conversation_entry: Dictionary containing conversation inbox entry data
            
        Returns:
            Formatted inbox update broadcast message
        """
        return {
            "type": "inbox.updated",
            "data": conversation_entry
        }

