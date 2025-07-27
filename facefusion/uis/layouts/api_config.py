"""
API Configuration for Gradio deployment on Hugging Face
This module provides enhanced API access for FaceFusion
"""

import os

def get_api_launch_config():
    """Get launch configuration for API access and Hugging Face deployment"""
    return {
        # Server configuration
        'server_name': os.getenv('GRADIO_SERVER_NAME', '0.0.0.0'),
        'server_port': int(os.getenv('GRADIO_SERVER_PORT', 7860)),
        
        # Sharing configuration
        'share': os.getenv('GRADIO_SHARE', 'False').lower() == 'true',
        
        # Authentication (optional)
        'auth': None,  # Can be set to ('username', 'password') for basic auth
        
        # Additional settings
        'max_threads': 40,
        
        # For Hugging Face Spaces
        'root_path': os.getenv('GRADIO_ROOT_PATH', ''),
    }
