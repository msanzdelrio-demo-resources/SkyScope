from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
import secrets

app = Flask(__name__)

# Security configurations
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    secret_key = secrets.token_hex(32)
    print(f"WARNING: Using generated secret key. Set SECRET_KEY environment variable for production.")
app.secret_key = secret_key

# Secure session configuration
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True only with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token lifetime

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Security headers - configured for development
talisman = Talisman(
    app,
    force_https=False,  # Don't force HTTPS in development
    strict_transport_security=False,  # Disable HSTS for development
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https://openweathermap.org",
    }
)

# Import utils module to make functions available
from . import utils

# Import views (must be after app creation)
from . import views