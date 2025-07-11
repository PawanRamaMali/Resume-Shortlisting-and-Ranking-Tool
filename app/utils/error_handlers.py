from flask import render_template, jsonify, request
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers with Flask app"""
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        logger.warning(f"404 error: {request.url}")
        return render_template('404.html'), 404
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 errors"""
        logger.error(f"500 error: {request.url} - {str(e)}")
        return render_template('500.html'), 500



