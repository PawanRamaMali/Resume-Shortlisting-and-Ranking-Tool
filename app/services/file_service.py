import shutil
from pathlib import Path
from typing import List, Optional
import logging
from werkzeug.utils import secure_filename
from app.utils.exceptions import FileServiceError
from flask import current_app

logger = logging.getLogger(__name__)

class FileService:
    """Service for handling file operations"""
    
    def __init__(self):
        self.upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        self.job_descriptions_folder = Path(current_app.config['JOB_DESCRIPTIONS_FOLDER'])
        self.allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
        
        # Ensure directories exist
        self.upload_folder.mkdir(parents=True, exist_ok=True)
        self.job_descriptions_folder.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_file(self, file, filename: str = None) -> Path:
        """Save uploaded file and return path"""
        try:
            if not filename:
                filename = file.filename
            
            if not self.is_allowed_file(filename):
                raise FileServiceError(f"File type not allowed: {filename}")
            
            safe_filename = secure_filename(filename)
            file_path = self.upload_folder / safe_filename
            
            # Handle duplicate filenames
            counter = 1
            while file_path.exists():
                name, ext = safe_filename.rsplit('.', 1)
                safe_filename = f"{name}_{counter}.{ext}"
                file_path = self.upload_folder / safe_filename
                counter += 1
            
            file.save(file_path)
            logger.info(f"Saved uploaded file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
            raise FileServiceError(f"Failed to save file: {e}")
    
    def get_resume_files(self) -> List[Path]:
        """Get all resume files from upload folder"""
        try:
            resume_files = []
            for ext in self.allowed_extensions:
                pattern = f"*.{ext}"
                resume_files.extend(self.upload_folder.glob(pattern))
            
            logger.info(f"Found {len(resume_files)} resume files")
            return resume_files
            
        except Exception as e:
            logger.error(f"Error getting resume files: {e}")
            raise FileServiceError(f"Failed to get resume files: {e}")
    
    def get_job_description_files(self) -> List[Path]:
        """Get all job description files"""
        try:
            job_files = []
            for ext in self.allowed_extensions:
                pattern = f"*.{ext}"
                job_files.extend(self.job_descriptions_folder.glob(pattern))
            
            logger.info(f"Found {len(job_files)} job description files")
            return job_files
            
        except Exception as e:
            logger.error(f"Error getting job description files: {e}")
            raise FileServiceError(f"Failed to get job description files: {e}")
    
    def delete_file(self, file_path: Path) -> bool:
        """Delete a file"""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise FileServiceError(f"Failed to delete file: {e}")
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in self.allowed_extensions)
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        try:
            return file_path.stat().st_size
        except Exception as e:
            logger.error(f"Error getting file size for {file_path}: {e}")
            return 0
