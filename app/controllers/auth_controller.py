from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.services.auth_service import AuthService
from app.utils.exceptions import AuthenticationError
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        auth_service = AuthService()
        user_info = auth_service.authenticate_user(username, password)
        
        # Set session
        session['logged_in'] = True
        session['username'] = user_info['username']
        session['role'] = user_info['role']
        
        flash('Login successful', 'success')
        logger.info(f"User logged in: {username}")
        
        return redirect(url_for('main.index'))
        
    except AuthenticationError as e:
        flash(str(e), 'error')
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Login error: {e}")
        flash('Login failed. Please try again.', 'error')
        return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    username = session.get('username')
    session.clear()
    flash('You have been logged out', 'info')
    logger.info(f"User logged out: {username}")
    return redirect(url_for('main.index'))