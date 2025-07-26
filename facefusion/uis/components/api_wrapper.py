"""
API Wrapper for FaceFusion
Provides a clean API interface for programmatic access
"""

import gradio
import tempfile
import base64
import os
from typing import Optional, Dict, Any

from facefusion import state_manager
from facefusion.filesystem import is_image, is_video
from facefusion.jobs import job_manager, job_store, job_helper
from facefusion.uis.typing import File
from facefusion.uis.core import get_ui_component


def process_face_swap(
    source_image: str,
    target_image: str,
    face_detector_model: str = "yoloface",
    face_detector_size: str = "640x640",
    face_selector_mode: str = "reference",
    face_selector_age: Optional[str] = None,
    face_selector_gender: Optional[str] = None,
    reference_face_distance: float = 0.6,
    face_mask_types: Optional[list] = None,
    face_mask_blur: float = 0.3,
    face_mask_padding: list = [0, 0, 0, 0],
    face_mask_regions: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Process face swap with base64 encoded images
    
    Args:
        source_image: Base64 encoded source image
        target_image: Base64 encoded target image
        face_detector_model: Model for face detection
        face_detector_size: Size for face detection
        face_selector_mode: Mode for face selection
        face_selector_age: Age filter (optional)
        face_selector_gender: Gender filter (optional)
        reference_face_distance: Distance threshold for face matching
        face_mask_types: Types of face masks to apply
        face_mask_blur: Blur amount for face mask
        face_mask_padding: Padding for face mask [top, right, bottom, left]
        face_mask_regions: Specific regions to mask
        
    Returns:
        Dictionary with result image as base64 and status
    """
    try:
        # Create temporary files for processing
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as source_file:
            source_data = base64.b64decode(source_image)
            source_file.write(source_data)
            source_path = source_file.name
            
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as target_file:
            target_data = base64.b64decode(target_image)
            target_file.write(target_data)
            target_path = target_file.name
            
        # Set up state manager with processing parameters
        state_manager.set_item('source_paths', [source_path])
        state_manager.set_item('target_path', target_path)
        state_manager.set_item('face_detector_model', face_detector_model)
        state_manager.set_item('face_detector_size', face_detector_size)
        state_manager.set_item('face_selector_mode', face_selector_mode)
        
        if face_selector_age:
            state_manager.set_item('face_selector_age', face_selector_age)
        if face_selector_gender:
            state_manager.set_item('face_selector_gender', face_selector_gender)
            
        state_manager.set_item('reference_face_distance', reference_face_distance)
        
        if face_mask_types:
            state_manager.set_item('face_mask_types', face_mask_types)
        state_manager.set_item('face_mask_blur', face_mask_blur)
        state_manager.set_item('face_mask_padding', face_mask_padding)
        
        if face_mask_regions:
            state_manager.set_item('face_mask_regions', face_mask_regions)
            
        # Process the swap
        from facefusion.core import conditional_process
        output_path = conditional_process()
        
        # Read result and convert to base64
        if output_path and os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                result_data = f.read()
                result_base64 = base64.b64encode(result_data).decode('utf-8')
                
            # Cleanup temporary files
            os.unlink(source_path)
            os.unlink(target_path)
            os.unlink(output_path)
            
            return {
                'status': 'success',
                'result': result_base64,
                'output_type': 'image' if is_image(output_path) else 'video'
            }
        else:
            # Cleanup temporary files
            os.unlink(source_path)
            os.unlink(target_path)
            
            return {
                'status': 'error',
                'message': 'Processing failed'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }


def create_api_interface():
    """Create a Gradio interface specifically for API access"""
    
    api_interface = gradio.Interface(
        fn=process_face_swap,
        inputs=[
            gradio.Textbox(label="Source Image (Base64)", lines=2),
            gradio.Textbox(label="Target Image (Base64)", lines=2),
            gradio.Dropdown(
                label="Face Detector Model",
                choices=["yoloface", "retinaface", "scrfd", "yunet"],
                value="yoloface"
            ),
            gradio.Dropdown(
                label="Face Detector Size", 
                choices=["160x160", "320x320", "480x480", "512x512", "640x640", "768x768", "960x960", "1024x1024"],
                value="640x640"
            ),
            gradio.Dropdown(
                label="Face Selector Mode",
                choices=["reference", "one", "many"],
                value="reference"
            ),
            gradio.Dropdown(
                label="Face Selector Age",
                choices=[None, "child", "teenager", "adult", "senior"],
                value=None
            ),
            gradio.Dropdown(
                label="Face Selector Gender",
                choices=[None, "male", "female"],
                value=None
            ),
            gradio.Slider(
                label="Reference Face Distance",
                minimum=0.0,
                maximum=2.0,
                value=0.6,
                step=0.05
            ),
            gradio.CheckboxGroup(
                label="Face Mask Types",
                choices=["box", "occlusion", "region"],
                value=None
            ),
            gradio.Slider(
                label="Face Mask Blur",
                minimum=0.0,
                maximum=1.0,
                value=0.3,
                step=0.05
            ),
            gradio.Dataframe(
                label="Face Mask Padding [top, right, bottom, left]",
                value=[[0, 0, 0, 0]],
                headers=["top", "right", "bottom", "left"],
                datatype=["number", "number", "number", "number"],
                max_rows=1
            ),
            gradio.CheckboxGroup(
                label="Face Mask Regions",
                choices=["skin", "left-eyebrow", "right-eyebrow", "left-eye", "right-eye", "glasses", "nose", "mouth", "upper-lip", "lower-lip"],
                value=None
            )
        ],
        outputs=gradio.JSON(label="Result"),
        title="FaceFusion API",
        description="API endpoint for face swapping. Send base64 encoded images and receive base64 encoded results.",
        allow_flagging="never"
    )
    
    return api_interface
