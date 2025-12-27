from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
import secrets

app = Flask(__name__)

# Determine if running in production
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production'

# Security configurations
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    if IS_PRODUCTION:
        raise ValueError(
            "SECRET_KEY environment variable is required in production. "
            "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
        )
    secret_key = secrets.token_hex(32)
    print(f"⚠️  WARNING: Using generated secret key for DEVELOPMENT ONLY.")
    print(f"   Set SECRET_KEY environment variable for production.")
app.secret_key = secret_key

# Secure session configuration with environment-based settings
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION  # Only send over HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS cookie access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token lifetime

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Security headers with environment-based configuration
talisman = Talisman(
    app,
    force_https=IS_PRODUCTION,  # Force HTTPS in production
    strict_transport_security=IS_PRODUCTION,  # Enable HSTS in production
    strict_transport_security_max_age=31536000 if IS_PRODUCTION else 0,  # 1 year
    strict_transport_security_include_subdomains=IS_PRODUCTION,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https://openweathermap.org",
        'connect-src': "'self'",
        'font-src': "'self'",
        'object-src': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'",
    },
    content_security_policy_nonce_in=['script-src', 'style-src'] if not IS_PRODUCTION else None,
)

# Log security configuration on startup
if IS_PRODUCTION:
    print("🔒 Security: Running in PRODUCTION mode")
    print("   ✓ HTTPS enforcement enabled")
    print("   ✓ Secure cookies enabled")
    print("   ✓ HSTS enabled")
else:
    print("🔓 Security: Running in DEVELOPMENT mode")
    print("   ⚠️  HTTPS enforcement disabled")
    print("   ⚠️  Secure cookies disabled")
    print("   ⚠️  Set FLASK_ENV=production for production deployment")

# Import utils module to make functions available
from . import utils

# Import views (must be after app creation)
from . import views