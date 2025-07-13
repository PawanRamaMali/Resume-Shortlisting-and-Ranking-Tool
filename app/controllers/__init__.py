from flask import Flask
from app.controllers.auth_controller import auth_bp
from app.controllers.resume_controller import resume_bp
from app.controllers.main_controller import main_bp

def register_blueprints(app: Flask):
    """Register all blueprint controllers"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resume_bp, url_prefix='/resume')