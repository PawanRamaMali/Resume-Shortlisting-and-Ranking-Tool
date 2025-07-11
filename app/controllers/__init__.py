from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.resume_controller import resume_bp
from app.controllers.main_controller import main_bp

def register_blueprints(app: Flask):
    """Register all blueprint controllers"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resume_bp, url_prefix='/resume')

# app/controllers/main_controller.py
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