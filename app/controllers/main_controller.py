from flask import Blueprint, render_template, current_app
from app.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main landing page"""
    try:
        # Check if file service is working
        try:
            file_service = FileService()
            job_files = file_service.get_job_description_files()
            
            # Convert to simple objects for template
            job_options = [{'name': file.name, 'display_name': file.stem} 
                          for file in job_files]
        except Exception as e:
            logger.warning(f"Error getting job files: {e}")
            job_options = []
        
        return render_template('index.html', job_options=job_options)
        
    except Exception as e:
        logger.error(f"Error loading main page: {e}")
        # Return a simple HTML response if templates fail
        return f"""
        <html>
        <head><title>RSART - Resume Shortlisting Tool</title></head>
        <body>
            <h1>Resume Shortlisting and Ranking Tool</h1>
            <p>Welcome to RSART. The application is running but encountered an error loading the full interface.</p>
            <p>Error: {str(e)}</p>
            <p><a href="/auth/login">Login</a></p>
        </body>
        </html>
        """, 500

@main_bp.route('/health')
def health_check():
    """Simple health check endpoint"""
    return {'status': 'ok', 'message': 'RSART is running'}