# app/__init__.py
from flask import Flask
from config import get_config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    # Create and configure Flask app
    app = Flask(__name__)
    app_config = get_config()
    app.config.from_object(app_config)

    # Initialize rate limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[app_config.RATELIMIT_DEFAULT]
    )

    # Import the routes blueprint (defined in routes.py)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Register custom error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    # Handle 404
    @app.errorhandler(404)
    def not_found_error(e):
        return app.render_template('404.html'), 404

    # Handle 500
    @app.errorhandler(500)
    def internal_error(e):
        return app.render_template('500.html'), 500