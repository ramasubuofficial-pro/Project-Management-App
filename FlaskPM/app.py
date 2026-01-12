from flask import Flask
from config import Config
from routes.auth_routes import auth_bp
from routes.view_routes import view_bp
from routes.api_routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    # Inject config into all templates
    # Inject config into all templates
    @app.context_processor
    def inject_config():
        return dict(config=app.config)

    # Global Session Verification
    from flask import session, request, redirect, url_for
    from utils import supabase

    @app.route('/favicon.ico')
    def favicon():
        return "", 204

    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # Check session on every request
    @app.before_request
    def check_user_active():
        # Skip static assets and auth routes (to allow login/logout)
        if not request.endpoint or 'static' in request.endpoint or 'auth.' in request.endpoint:
            return
        
        # If accessing the login page itself, don't loop
        if request.endpoint == 'view_bp.login':
            return

        # Check if session exists but user is deleted from DB
        if 'user' in session:
            user_id = session.get('user', {}).get('id')
            if user_id:
                try:
                    # Check if user exists in public.users table
                    res = supabase.table('users').select('id').eq('id', user_id).execute()
                    if not res.data:
                        print(f"User {user_id} not found in DB. Forcing logout.")
                        session.clear()
                        return redirect(url_for('view_bp.login'))
                except Exception as e:
                    print(f"Session check error: {e}")
                    # Optional: Force logout on error to be safe? 
                    # For now, let's allow ensuring it's not a temp glitch.

    return app

app = create_app()

if __name__ == "__main__":
    import os
    from scheduler import start_scheduler
    
    # Ensure scheduler only runs once (in the reloader process)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()
        
    app.run(debug=True, port=5000)
