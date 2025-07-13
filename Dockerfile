FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \
    libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig \
    libpulse-dev \
    # PostgreSQL dependencies
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/ ./requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/production.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/uploaded_resumes data/job_descriptions logs

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=run.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]