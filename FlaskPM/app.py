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

    # Reverse Geocode API (OSM Fallback)
    import requests
    from flask import request, jsonify

    # Reverse Geocode API (OSM Fallback) - Zoom 18
    @app.route("/api/reverse-geocode")
    def reverse_geocode():
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        headers = {
            "User-Agent": "DIGIANCHORZ-Attendance/1.0 (contact@digianchorz.com)"
        }

        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "json",
            "lat": lat,
            "lon": lon,
            "zoom": 18,
            "addressdetails": 1
        }

        try:
            r = requests.get(url, params=params, headers=headers, timeout=6)
            data = r.json()
            addr = data.get("address", {})

            # Extract highly granular parts (PagarBook style)
            # Priority: House/Building -> Specific Place (Shop, College) -> Road -> Area -> City
            
            house_number = addr.get("house_number")
            
            # Specific place names
            place_name = (
                addr.get("amenity") 
                or addr.get("building") 
                or addr.get("shop") 
                or addr.get("office") 
                or addr.get("leisure")
                or addr.get("tourism")
                or addr.get("name") # Generic name fallback
            )
            
            road = addr.get("road")
            
            suburb = (
                addr.get("neighbourhood")
                or addr.get("suburb")
                or addr.get("residential")
                or addr.get("quarter")
                or addr.get("hamlet")
                or addr.get("locality")
                or addr.get("city_district")
            )
            
            city_town = (
                addr.get("city")
                or addr.get("town")
                or addr.get("village")
                or addr.get("municipality")
            )
            
            district = (
                addr.get("state_district")
                or addr.get("city_district")
                or addr.get("county")
            )
            
            state = addr.get("state")
            postcode = addr.get("postcode")

            # Build list with specific header parts first
            parts = []
            if house_number: parts.append(str(house_number))
            if place_name: parts.append(place_name)
            if road: parts.append(road)
            if suburb: parts.append(suburb)
            if city_town: parts.append(city_town)
            if district: parts.append(district)
            if state: parts.append(state)
            if postcode: parts.append(postcode)

            # Deduplicate preserving order (e.g. if Place Name == Road, don't show it twice)
            seen = set()
            clean_parts = []
            for p in parts:
                if p and p not in seen:
                    clean_parts.append(p)
                    seen.add(p)

            location = ", ".join(clean_parts)

            if location:
                return jsonify({"location": location})

        except Exception as e:
            print("Reverse geo error:", e)

        return jsonify({"location": f"{lat}, {lon}"})

    return app

app = create_app()

if __name__ == "__main__":
    import os
    from scheduler import start_scheduler
    
    # Ensure scheduler only runs once (in the reloader process)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler()
        
    app.run(debug=True, port=5000)

