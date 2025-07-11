from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

# app/models/candidate.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
import uuid

@dataclass
class Candidate:
    """Data model for candidate information extracted from resume"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    experience: List[str] = field(default_factory=list)
    competencies: Dict[str, List[str]] = field(default_factory=dict)
    resume_path: Optional[Path] = None
    resume_text: Optional[str] = None
    score: Optional[float] = None
    rank: Optional[int] = None
    
    @property
    def display_name(self) -> str:
        """Return display name or filename if name not extracted"""
        if self.name:
            return self.name
        if self.resume_path:
            return self.resume_path.stem
        return f"Candidate_{self.id[:8]}"
    
    @property
    def skills_text(self) -> str:
        """Return skills as comma-separated string"""
        return ", ".join(self.skills) if self.skills else ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert candidate to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills,
            'education': self.education,
            'experience': self.experience,
            'competencies': self.competencies,
            'resume_path': str(self.resume_path) if self.resume_path else None,
            'score': self.score,
            'rank': self.rank
        }