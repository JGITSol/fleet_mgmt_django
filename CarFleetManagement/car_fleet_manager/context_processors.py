"""Context processors for Car Fleet Manager.

This module contains context processors that add additional
variables to the template context.
"""

from car_fleet_manager.version import VERSION_INFO

def version_info(request):
    """Add version information to the template context.
    
    This makes version information available in all templates.
    
    Args:
        request: The HTTP request object
        
    Returns:
        dict: A dictionary containing version information
    """
    return {
        'version_info': VERSION_INFO
    }

def theme_processor(request):
    """Add theme information to the template context.
    
    This makes the current theme preference available in all templates.
    
    Args:
        request: The HTTP request object
        
    Returns:
        dict: A dictionary containing theme information
    """
    # Get theme from session or default to light
    theme = request.session.get('theme', 'light')
    return {
        'current_theme': theme
    }