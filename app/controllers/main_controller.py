from flask import Blueprint, render_template, current_app
from app.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main landing page"""
    try:
        file_service = FileService()
        job_files = file_service.get_job_description_files()
        
        # Convert to simple objects for template
        job_options = [{'name': file.name, 'display_name': file.stem} 
                      for file in job_files]
        
        return render_template('index.html', job_options=job_options)
        
    except Exception as e:
        logger.error(f"Error loading main page: {e}")
        return render_template('error.html', error="Failed to load page"), 500