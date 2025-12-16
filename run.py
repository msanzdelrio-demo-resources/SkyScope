from app import app
import os

if __name__ == "__main__":
    # Only enable debug in development environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)