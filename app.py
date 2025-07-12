from app import create_app
from app.extensions import db
import os

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    # Add sample job descriptions and test data
    pass

if __name__ == '__main__':
    app.run()