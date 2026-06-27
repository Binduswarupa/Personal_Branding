"""
============================================
LinkedIn Branding Assistant - Main Application
============================================
Flask application entry point with route registration and CORS setup.
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from config import Config
from database import Database

def create_app():
    """Application factory pattern."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    
    # Configuration
    app.config.from_object(Config)
    
    # Enable CORS for frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize database
    try:
        Database.initialize()
    except Exception as e:
        print(f"[WARN] Database initialization warning: {e}")
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.profile import profile_bp
    from routes.content import content_bp
    from routes.branding import branding_bp
    from routes.history import history_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(content_bp, url_prefix='/api/content')
    app.register_blueprint(branding_bp, url_prefix='/api/branding')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    
    # ── Frontend Serving ─────────────────────────────
    
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    # ── Health Check ─────────────────────────────────
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'LinkedIn Branding Assistant API',
            'version': '1.0.0'
        }), 200
    
    # ── Error Handlers ───────────────────────────────
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


# ── Application Entry Point ─────────────────────────

app = create_app()

if __name__ == '__main__':
    print("""
    ==============================================
      LinkedIn Branding Assistant API Server
      Running on http://localhost:5000
    ==============================================
    """)
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
