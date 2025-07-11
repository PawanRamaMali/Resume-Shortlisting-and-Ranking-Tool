# Resume Shortlisting and Ranking Tool - Refactoring Plan

## Current Issues Identified

### 1. **Architecture & Structure**
- No clear separation of concerns
- Business logic mixed with presentation layer
- No proper MVC/MVP pattern
- Monolithic functions doing multiple things
- No dependency injection

### 2. **Code Quality Issues**
- Hardcoded credentials in source code
- Global variables and poor state management
- Inconsistent error handling
- No input validation
- Poor naming conventions
- Duplicate code across modules

### 3. **Security Vulnerabilities**
- Hardcoded admin credentials (`admin`/`root`)
- No CSRF protection
- No input sanitization
- File upload without validation
- Session management issues

### 4. **Performance Problems**
- No caching mechanisms
- Inefficient file processing
- Loading entire files into memory
- No pagination for results
- Blocking operations in main thread

### 5. **Maintainability Issues**
- No configuration management
- No logging system
- No testing infrastructure
- Poor documentation
- Tight coupling between components

### 6. **Dependencies & Libraries**
- Outdated library versions in requirements.txt
- Missing error handling for library imports
- Inconsistent use of libraries (multiple PDF parsers)

## Refactoring Strategy

### Phase 1: Project Structure & Configuration
1. Implement proper project structure
2. Add configuration management
3. Set up logging system
4. Create proper requirements management

### Phase 2: Core Architecture Refactoring
1. Implement service layer pattern
2. Create data access layer
3. Add dependency injection
4. Implement proper error handling

### Phase 3: Security & Validation
1. Implement proper authentication
2. Add input validation
3. Secure file handling
4. Add CSRF protection

### Phase 4: Performance & Scalability
1. Add caching layer
2. Implement async processing
3. Add database support
4. Optimize algorithms

### Phase 5: Testing & Documentation
1. Add unit tests
2. Integration tests
3. API documentation
4. User documentation

---

## Detailed Refactoring Plan

### 1. Project Structure Reorganization

```
rsart/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.conf
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume.py
│   │   ├── job_description.py
│   │   └── candidate.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── matching_service.py
│   │   ├── file_service.py
│   │   └── auth_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── resume_controller.py
│   │   └── api_controller.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   └── templates/
│       └── [existing templates]
├── tests/
├── data/
├── logs/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── migrations/
├── docker-compose.yml
├── Dockerfile
└── run.py
```

### 2. Configuration Management

Replace hardcoded values with proper configuration:

```python
# app/config/settings.py
import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = Path('data/uploaded_resumes')
    JOB_DESCRIPTIONS_FOLDER = Path('data/job_descriptions')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///rsart.db'
    
    # Redis for caching
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = Path('logs/rsart.log')

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
```

### 3. Models Layer

Create proper data models:

```python
# app/models/candidate.py
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class Candidate:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = None
    education: List[str] = None
    experience: List[str] = None
    resume_path: Optional[Path] = None
    score: Optional[float] = None
    rank: Optional[int] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.education is None:
            self.education = []
        if self.experience is None:
            self.experience = []

# app/models/job_description.py
@dataclass
class JobDescription:
    id: Optional[str] = None
    title: Optional[str] = None
    description: str = ""
    requirements: List[str] = None
    skills: List[str] = None
    file_path: Optional[Path] = None
    
    def __post_init__(self):
        if self.requirements is None:
            self.requirements = []
        if self.skills is None:
            self.skills = []
```

### 4. Service Layer Implementation

Extract business logic into services:

```python
# app/services/resume_parser.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ResumeParserInterface(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> Dict[str, Any]:
        pass

class PDFResumeParser(ResumeParserInterface):
    def parse(self, file_path: Path) -> Dict[str, Any]:
        try:
            # Implement PDF parsing logic
            return self._extract_resume_data(file_path)
        except Exception as e:
            logger.error(f"Error parsing PDF resume {file_path}: {e}")
            raise

class ResumeParserFactory:
    @staticmethod
    def get_parser(file_extension: str) -> ResumeParserInterface:
        parsers = {
            '.pdf': PDFResumeParser(),
            '.doc': DocResumeParser(),
            '.docx': DocxResumeParser(),
        }
        return parsers.get(file_extension.lower())

# app/services/matching_service.py
class ResumeMatchingService:
    def __init__(self, vectorizer_service, similarity_calculator):
        self.vectorizer = vectorizer_service
        self.similarity_calculator = similarity_calculator
    
    def calculate_match_scores(self, job_description: JobDescription, 
                             candidates: List[Candidate]) -> List[Candidate]:
        job_vector = self.vectorizer.vectorize(job_description.description)
        
        for candidate in candidates:
            resume_text = self._prepare_resume_text(candidate)
            resume_vector = self.vectorizer.vectorize(resume_text)
            score = self.similarity_calculator.calculate(job_vector, resume_vector)
            candidate.score = score
        
        return sorted(candidates, key=lambda x: x.score, reverse=True)
```

### 5. Controller Layer

Separate route handlers from business logic:

```python
# app/controllers/resume_controller.py
from flask import Blueprint, request, render_template, jsonify
from app.services.matching_service import ResumeMatchingService
from app.utils.validators import validate_file_upload
from app.utils.decorators import login_required

resume_bp = Blueprint('resume', __name__)

class ResumeController:
    def __init__(self, matching_service: ResumeMatchingService):
        self.matching_service = matching_service
    
    @resume_bp.route('/process', methods=['POST'])
    @login_required
    def process_resumes(self):
        try:
            job_description_file = request.form.get('job_description')
            
            if not validate_file_upload(job_description_file):
                return jsonify({'error': 'Invalid file'}), 400
            
            results = self.matching_service.process_job_application(
                job_description_file
            )
            
            return render_template('results.html', results=results)
            
        except Exception as e:
            logger.error(f"Error processing resumes: {e}")
            return jsonify({'error': 'Processing failed'}), 500
```

### 6. Utilities and Helpers

Create reusable utility functions:

```python
# app/utils/validators.py
from pathlib import Path
from werkzeug.utils import secure_filename
from app.config.settings import Config

def validate_file_extension(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_file_size(file) -> bool:
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset
    return size <= Config.MAX_CONTENT_LENGTH

def sanitize_filename(filename: str) -> str:
    return secure_filename(filename)

# app/utils/decorators.py
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

### 7. Error Handling and Logging

Implement comprehensive error handling:

```python
# app/utils/error_handlers.py
from flask import jsonify, render_template
import logging

logger = logging.getLogger(__name__)

class RSARTException(Exception):
    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

def handle_rsart_exception(error):
    logger.error(f"RSART Exception: {error.message}")
    response = jsonify(error.payload or {'error': error.message})
    response.status_code = error.status_code
    return response

def handle_generic_exception(error):
    logger.error(f"Unhandled exception: {error}")
    return render_template('error.html', error="An unexpected error occurred"), 500
```

### 8. Testing Infrastructure

Add comprehensive testing:

```python
# tests/test_resume_parser.py
import pytest
from pathlib import Path
from app.services.resume_parser import PDFResumeParser

class TestPDFResumeParser:
    def setup_method(self):
        self.parser = PDFResumeParser()
    
    def test_parse_valid_pdf(self):
        test_file = Path('tests/fixtures/sample_resume.pdf')
        result = self.parser.parse(test_file)
        
        assert 'name' in result
        assert 'email' in result
        assert 'skills' in result
    
    def test_parse_invalid_file(self):
        with pytest.raises(Exception):
            self.parser.parse(Path('nonexistent.pdf'))

# tests/conftest.py
import pytest
from app import create_app
from app.config.settings import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

### 9. Performance Optimizations

Add caching and async processing:

```python
# app/services/cache_service.py
import redis
import json
from typing import Any, Optional

class CacheService:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
    
    def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, expire: int = 3600):
        self.redis_client.setex(key, expire, json.dumps(value))
    
    def delete(self, key: str):
        self.redis_client.delete(key)

# app/services/async_processing.py
from celery import Celery

def create_celery_app(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config)
    return celery

@celery.task
def process_resume_batch(job_description_id: str, resume_files: List[str]):
    # Implement async resume processing
    pass
```

### 10. Database Integration

Add proper data persistence:

```python
# app/models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CandidateModel(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    skills = Column(Text)
    resume_path = Column(String(255))
    score = Column(Float)
    
# app/repositories/candidate_repository.py
class CandidateRepository:
    def __init__(self, session):
        self.session = session
    
    def save(self, candidate: Candidate) -> Candidate:
        candidate_model = CandidateModel(**candidate.__dict__)
        self.session.add(candidate_model)
        self.session.commit()
        return candidate
    
    def find_by_job_description(self, job_id: str) -> List[Candidate]:
        # Implement query logic
        pass
```

## Implementation Priority

1. **High Priority**: Configuration, Security, Error Handling
2. **Medium Priority**: Service Layer, Testing, Database
3. **Low Priority**: Caching, Async Processing, Advanced Features

## Benefits of Refactoring

- **Maintainability**: Clear separation of concerns
- **Testability**: Proper dependency injection and mocking
- **Security**: Proper authentication and validation
- **Performance**: Caching and async processing
- **Scalability**: Database support and service architecture
- **Reliability**: Comprehensive error handling and logging
