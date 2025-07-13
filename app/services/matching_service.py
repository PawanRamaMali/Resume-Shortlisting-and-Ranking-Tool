from typing import List, Tuple
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
from app.extensions import Candidate
from app.extensions import JobDescription
from app.utils.text_processor import TextProcessor
from app.utils.exceptions import MatchingServiceError

logger = logging.getLogger(__name__)

class ResumeMatchingService:
    """Service for matching resumes against job descriptions"""
    
    def __init__(self, top_candidates_count: int = 10, similarity_threshold: float = 0.1):
        self.top_candidates_count = top_candidates_count
        self.similarity_threshold = similarity_threshold
        self.text_processor = TextProcessor()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2),
            lowercase=True
        )
    
    def match_candidates(self, job_description: JobDescription, 
                        candidates: List[Candidate]) -> List[Candidate]:
        """
        Match candidates against job description and return ranked results
        """
        try:
            logger.info(f"Matching {len(candidates)} candidates against job: {job_description.display_name}")
            
            if not candidates:
                logger.warning("No candidates provided for matching")
                return []
            
            # Prepare texts for vectorization
            job_text = self._prepare_job_text(job_description)
            candidate_texts = [self._prepare_candidate_text(candidate) for candidate in candidates]
            
            # Create corpus including job description
            corpus = [job_text] + candidate_texts
            
            # Vectorize texts
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Calculate similarities
            job_vector = tfidf_matrix[0:1]  # First row is job description
            candidate_vectors = tfidf_matrix[1:]  # Rest are candidates
            
            similarities = cosine_similarity(job_vector, candidate_vectors)[0]
            
            # Assign scores and ranks
            for i, candidate in enumerate(candidates):
                candidate.score = float(similarities[i])
            
            # Sort by score descending
            ranked_candidates = sorted(candidates, key=lambda x: x.score, reverse=True)
            
            # Assign ranks
            for rank, candidate in enumerate(ranked_candidates, 1):
                candidate.rank = rank
            
            # Filter by threshold and limit
            filtered_candidates = [
                c for c in ranked_candidates 
                if c.score >= self.similarity_threshold
            ][:self.top_candidates_count]
            
            logger.info(f"Matched {len(filtered_candidates)} candidates above threshold")
            return filtered_candidates
            
        except Exception as e:
            logger.error(f"Error in candidate matching: {e}")
            raise MatchingServiceError(f"Failed to match candidates: {e}")
    
    def _prepare_job_text(self, job_description: JobDescription) -> str:
        """Prepare job description text for vectorization"""
        text_parts = []
        
        if job_description.description:
            text_parts.append(job_description.description)
        
        if job_description.requirements:
            text_parts.extend(job_description.requirements)
        
        if job_description.skills:
            text_parts.extend(job_description.skills)
        
        combined_text = " ".join(text_parts)
        return self.text_processor.preprocess(combined_text)
    
    def _prepare_candidate_text(self, candidate: Candidate) -> str:
        """Prepare candidate text for vectorization"""
        text_parts = []
        
        if candidate.resume_text:
            text_parts.append(candidate.resume_text)
        
        if candidate.skills:
            text_parts.extend(candidate.skills)
        
        if candidate.experience:
            text_parts.extend(candidate.experience)
        
        if candidate.education:
            text_parts.extend(candidate.education)
        
        combined_text = " ".join(text_parts)
        return self.text_processor.preprocess(combined_text)