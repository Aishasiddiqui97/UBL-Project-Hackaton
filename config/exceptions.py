"""Custom exception handler for DRF."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, Optional


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """
    Custom exception handler for consistent error responses.
    
    Args:
        exc: The exception instance
        context: Context information about the error
        
    Returns:
        Response with standardized error format
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'An error occurred',
            'errors': {}
        }
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = str(response.data['detail'])
            else:
                custom_response_data['errors'] = response.data
                custom_response_data['message'] = 'Validation error'
        else:
            custom_response_data['message'] = str(response.data)
        
        response.data = custom_response_data
    
    return response
