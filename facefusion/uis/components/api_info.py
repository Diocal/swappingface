"""
API Information Component
Muestra información sobre el acceso API en la interfaz
"""

import gradio

from facefusion import metadata, wording
from facefusion.uis.core import get_ui_component

API_INFO_HTML = """
<div style="padding: 1.5rem; background: linear-gradient(135deg, #ff4444 0%, #ff6666 100%); border-radius: 0.5rem; margin-bottom: 1rem; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h2 style="margin-top: 0; color: white; text-align: center;">🚀 GRADIO API ENABLED - Full API Access Available!</h2>
    <p style="margin: 0.5rem 0;"><strong>Gradio Version:</strong> 5.25.2</p>
    <p style="margin: 0.5rem 0;"><strong>API Documentation:</strong> <a href="/docs" target="_blank" style="color: #ff4444;">/docs</a></p>
    <p style="margin: 0.5rem 0;"><strong>API Endpoint:</strong> <code>/api/predict</code></p>
    
    <details style="margin-top: 1rem;">
        <summary style="cursor: pointer; font-weight: bold; color: #ff4444;">Quick Start Guide</summary>
        <div style="margin-top: 0.5rem; padding: 0.5rem; background-color: #fff; border-radius: 0.25rem;">
            <h4 style="margin-top: 0;">Python Client:</h4>
            <pre style="background-color: #f5f5f5; padding: 0.5rem; border-radius: 0.25rem; overflow-x: auto;">
from gradio_client import Client

client = Client("https://your-space.hf.space")
result = client.predict(
    "source.jpg",
    "target.jpg",
    api_name="/predict"
)</pre>
            
            <h4>REST API:</h4>
            <pre style="background-color: #f5f5f5; padding: 0.5rem; border-radius: 0.25rem; overflow-x: auto;">
curl -X POST https://your-space.hf.space/api/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "fn_index": 0,
    "data": ["source_base64", "target_base64"]
  }'</pre>
            
            <p style="margin: 0.5rem 0;">
                <a href="https://github.com/gradio-app/gradio/blob/main/client/python/README.md" 
                   target="_blank" style="color: #ff4444;">
                   Full API Documentation →
                </a>
            </p>
        </div>
    </details>
</div>
"""

HUGGINGFACE_INFO_HTML = """
<div style="padding: 1rem; background-color: #ffe6e6; border-radius: 0.5rem; margin-bottom: 1rem;">
    <h3 style="margin-top: 0; color: #333;">🤗 Hugging Face Deployment</h3>
    <p style="margin: 0.5rem 0;">This app is optimized for Hugging Face Spaces deployment.</p>
    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>GPU Support: ✅ Enabled</li>
        <li>API Access: ✅ Enabled</li>
        <li>Queue System: ✅ Enabled</li>
        <li>Max File Size: 100MB</li>
        <li>Timeout: 600 seconds</li>
    </ul>
    <p style="margin: 0.5rem 0;">
        <a href="/API_GUIDE.md" target="_blank" style="color: #ff4444;">View Full API Guide</a> | 
        <a href="/HUGGINGFACE_DEPLOYMENT.md" target="_blank" style="color: #ff4444;">Deployment Instructions</a>
    </p>
</div>
"""


def render() -> None:
    """Render API information component"""
    
    # API Info
    api_info = gradio.HTML(
        value=API_INFO_HTML,
        visible=True
    )
    
    # Hugging Face Info  
    hf_info = gradio.HTML(
        value=HUGGINGFACE_INFO_HTML,
        visible=True
    )
    
    # Status indicator
    status = gradio.Textbox(
        label="API Status",
        value="✅ API is running and accessible",
        interactive=False,
        max_lines=1
    )


def listen() -> None:
    """Set up event listeners"""
    pass


def run() -> None:
    """Run component logic"""
    pass
