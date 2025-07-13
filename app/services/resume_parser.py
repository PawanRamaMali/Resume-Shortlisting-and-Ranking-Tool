from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import re
import docx2txt
import PyPDF2
import textract
from app.models.candidate import Candidate
from app.utils.text_processor import TextProcessor
from app.utils.exceptions import ResumeParsingError

logger = logging.getLogger(__name__)

class ResumeParserInterface(ABC):
    """Abstract interface for resume parsers"""
    
    @abstractmethod
    def parse(self, file_path: Path) -> Candidate:
        """Parse resume file and return Candidate object"""
        pass

class BaseResumeParser(ResumeParserInterface):
    """Base class with common parsing logic"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
    
    def _extract_basic_info(self, text: str) -> Dict[str, Any]:
        """Extract basic information from resume text"""
        try:
            return {
                'name': self._extract_name(text),
                'email': self._extract_email(text),
                'phone': self._extract_phone(text),
                'skills': self._extract_skills(text),
                'education': self._extract_education(text),
                'experience': self._extract_experience(text)
            }
        except Exception as e:
            logger.error(f"Error extracting basic info: {e}")
            return {}
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return ''.join(phones[0]) if phones else None
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from text (simplified implementation)"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if len(line.split()) == 2 and line.replace(' ', '').isalpha():
                return line
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        # This is a simplified implementation
        # In production, you'd use NLP models or predefined skill databases
        common_skills = [
            'python', 'java', 'javascript', 'sql', 'react', 'angular', 'vue',
            'machine learning', 'data analysis', 'project management',
            'communication', 'leadership', 'teamwork'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = ['degree', 'university', 'college', 'bachelor', 'master', 'phd']
        education = []
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education.append(line.strip())
        
        return education
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience"""
        experience_keywords = ['experience', 'work', 'employed', 'position', 'role']
        experience = []
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in experience_keywords):
                experience.append(line.strip())
        
        return experience

class PDFResumeParser(BaseResumeParser):
    """Parser for PDF resume files"""
    
    def parse(self, file_path: Path) -> Candidate:
        try:
            logger.info(f"Parsing PDF resume: {file_path}")
            
            text = self._extract_text_from_pdf(file_path)
            if not text.strip():
                raise ResumeParsingError(f"No text extracted from PDF: {file_path}")
            
            basic_info = self._extract_basic_info(text)
            
            candidate = Candidate(
                name=basic_info.get('name'),
                email=basic_info.get('email'),
                phone=basic_info.get('phone'),
                skills=basic_info.get('skills', []),
                education=basic_info.get('education', []),
                experience=basic_info.get('experience', []),
                resume_path=file_path,
                resume_text=text
            )
            
            logger.info(f"Successfully parsed PDF resume: {candidate.display_name}")
            return candidate
            
        except Exception as e:
            logger.error(f"Error parsing PDF resume {file_path}: {e}")
            raise ResumeParsingError(f"Failed to parse PDF resume: {e}")
    
    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.warning(f"PyPDF2 failed for {file_path}, trying textract: {e}")
            try:
                text = textract.process(str(file_path)).decode('utf-8')
            except Exception as e2:
                logger.error(f"Both PyPDF2 and textract failed for {file_path}: {e2}")
                raise
        
        return text

class DocxResumeParser(BaseResumeParser):
    """Parser for DOCX resume files"""
    
    def parse(self, file_path: Path) -> Candidate:
        try:
            logger.info(f"Parsing DOCX resume: {file_path}")
            
            text = docx2txt.process(str(file_path))
            if not text.strip():
                raise ResumeParsingError(f"No text extracted from DOCX: {file_path}")
            
            basic_info = self._extract_basic_info(text)
            
            candidate = Candidate(
                name=basic_info.get('name'),
                email=basic_info.get('email'),
                phone=basic_info.get('phone'),
                skills=basic_info.get('skills', []),
                education=basic_info.get('education', []),
                experience=basic_info.get('experience', []),
                resume_path=file_path,
                resume_text=text
            )
            
            logger.info(f"Successfully parsed DOCX resume: {candidate.display_name}")
            return candidate
            
        except Exception as e:
            logger.error(f"Error parsing DOCX resume {file_path}: {e}")
            raise ResumeParsingError(f"Failed to parse DOCX resume: {e}")

class DocResumeParser(BaseResumeParser):
    """Parser for DOC resume files"""
    
    def parse(self, file_path: Path) -> Candidate:
        try:
            logger.info(f"Parsing DOC resume: {file_path}")
            
            # Use textract for DOC files
            text = textract.process(str(file_path)).decode('utf-8')
            if not text.strip():
                raise ResumeParsingError(f"No text extracted from DOC: {file_path}")
            
            basic_info = self._extract_basic_info(text)
            
            candidate = Candidate(
                name=basic_info.get('name'),
                email=basic_info.get('email'),
                phone=basic_info.get('phone'),
                skills=basic_info.get('skills', []),
                education=basic_info.get('education', []),
                experience=basic_info.get('experience', []),
                resume_path=file_path,
                resume_text=text
            )
            
            logger.info(f"Successfully parsed DOC resume: {candidate.display_name}")
            return candidate
            
        except Exception as e:
            logger.error(f"Error parsing DOC resume {file_path}: {e}")
            raise ResumeParsingError(f"Failed to parse DOC resume: {e}")

class ResumeParserFactory:
    """Factory class to get appropriate parser based on file extension"""
    
    _parsers = {
        '.pdf': PDFResumeParser,
        '.docx': DocxResumeParser,
        '.doc': DocResumeParser,
    }
    
    @classmethod
    def get_parser(cls, file_extension: str) -> ResumeParserInterface:
        """Get parser instance for given file extension"""
        parser_class = cls._parsers.get(file_extension.lower())
        if not parser_class:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        return parser_class()
    
    @classmethod
    def supported_extensions(cls) -> List[str]:
        """Get list of supported file extensions"""
        return list(cls._parsers.keys())