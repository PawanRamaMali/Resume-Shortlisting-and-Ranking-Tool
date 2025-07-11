from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import uuid

@dataclass
class JobDescription:
    """Data model for job description information"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    file_path: Optional[Path] = None
    processed_text: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Return display name or filename"""
        if self.title:
            return self.title
        if self.file_path:
            return self.file_path.stem
        return f"Job_{self.id[:8]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job description to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'skills': self.skills,
            'file_path': str(self.file_path) if self.file_path else None
        }