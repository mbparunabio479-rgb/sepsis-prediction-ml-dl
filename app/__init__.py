from flask import Flask, session, redirect, url_for, request

from .routes import bp
from .routes_human_loop import human_loop_bp
from .services.store import PatientStore
from .services.sepsis_engine import SepsisEngine
from .services.simulator import PatientSimulator


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sepsis-demo-secret-key-change-in-production"

    # Enable session management
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour timeout

    store = PatientStore()
    engine = SepsisEngine()
    simulator = PatientSimulator(store)

    app.config["STORE"] = store
    app.config["ENGINE"] = engine
    app.config["SIMULATOR"] = simulator

    # Start real-time simulation
    simulator.start()

    # Authentication middleware
    @app.before_request
    def check_authentication():
        """Check if user is authenticated before accessing protected routes"""
        # Public routes that don't require authentication
        public_routes = ['main.login', 'main.home']

        # If user not in session and accessing protected route
        if 'user_id' not in session:
            # Allow access to login, home, static files, and API routes
            if request.endpoint not in public_routes and not request.path.startswith('/static') and not request.path.startswith('/api/'):
                return redirect(url_for('main.login'))

    app.register_blueprint(bp)
    app.register_blueprint(human_loop_bp)
    return app
