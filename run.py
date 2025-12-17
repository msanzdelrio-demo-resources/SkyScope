from app import app
import os

if __name__ == "__main__":
    # Only enable debug in development environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    app.run(host=host, port=5001, debug=debug_mode)