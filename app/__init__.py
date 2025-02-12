# app/__init__.py
from flask import Flask
from config import get_config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))
    app_config = get_config()
    app.config.from_object(app_config)
    # ...


    limiter = Limiter(
        app,
        key_func=get_remote_address,
        storage_uri="memory://",
        default_limits=[app_config.RATELIMIT_DEFAULT]
    )

    # Import and register your routes, error handlers, etc.
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(e):
        return app.render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return app.render_template('500.html'), 500