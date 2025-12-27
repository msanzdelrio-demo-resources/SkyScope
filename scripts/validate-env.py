#!/usr/bin/env python3
"""
Environment validation script for SkyScope
Checks that all required environment variables are properly configured
Run before deployment: python scripts/validate-env.py
"""

import os
import sys
import re

class Colors:
    """Terminal colors for output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def check_required_env_vars():
    """Check for required environment variables"""
    print(f"\n{Colors.BOLD}🔍 Checking Required Environment Variables{Colors.RESET}")
    print("=" * 60)
    
    required_vars = {
        'SECRET_KEY': {
            'required': True,
            'min_length': 32,
            'description': 'Flask secret key for session encryption'
        },
        'OPENWEATHER_APPID': {
            'required': True,
            'min_length': 20,
            'description': 'OpenWeatherMap API key'
        },
        'FLASK_ENV': {
            'required': False,
            'valid_values': ['development', 'production'],
            'description': 'Flask environment mode'
        }
    }
    
    issues = []
    warnings = []
    
    for var_name, config in required_vars.items():
        value = os.environ.get(var_name)
        
        if not value:
            if config['required']:
                print(f"{Colors.RED}❌ {var_name}: NOT SET{Colors.RESET}")
                print(f"   {config['description']}")
                issues.append(var_name)
            else:
                print(f"{Colors.YELLOW}⚠️  {var_name}: Not set (optional){Colors.RESET}")
                warnings.append(var_name)
            continue
        
        # Check minimum length
        if 'min_length' in config and len(value) < config['min_length']:
            print(f"{Colors.RED}❌ {var_name}: TOO SHORT{Colors.RESET}")
            print(f"   Current: {len(value)} chars, Required: {config['min_length']}+ chars")
            issues.append(var_name)
            continue
        
        # Check valid values
        if 'valid_values' in config and value not in config['valid_values']:
            print(f"{Colors.RED}❌ {var_name}: INVALID VALUE{Colors.RESET}")
            print(f"   Current: '{value}', Valid: {config['valid_values']}")
            issues.append(var_name)
            continue
        
        # Check for example/placeholder values
        placeholder_patterns = [
            'your-',
            'change-this',
            'example',
            'placeholder',
            'test-api-key'
        ]
        if any(pattern in value.lower() for pattern in placeholder_patterns):
            print(f"{Colors.YELLOW}⚠️  {var_name}: Using placeholder value{Colors.RESET}")
            print(f"   Please set a real value for production")
            warnings.append(var_name)
            continue
        
        print(f"{Colors.GREEN}✅ {var_name}: Valid ({len(value)} chars){Colors.RESET}")
    
    return issues, warnings

def check_security_configuration():
    """Check security-related configuration"""
    print(f"\n{Colors.BOLD}🔒 Checking Security Configuration{Colors.RESET}")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    flask_env = os.environ.get('FLASK_ENV', 'development')
    is_production = flask_env == 'production'
    
    if is_production:
        print(f"{Colors.GREEN}✅ Running in PRODUCTION mode{Colors.RESET}")
        
        # Check SECRET_KEY strength in production
        secret_key = os.environ.get('SECRET_KEY', '')
        if len(secret_key) < 64:
            print(f"{Colors.YELLOW}⚠️  SECRET_KEY should be 64+ characters in production{Colors.RESET}")
            warnings.append('weak_secret_key')
        
        # Check for debug mode
        if os.environ.get('FLASK_DEBUG', 'False').lower() == 'true':
            print(f"{Colors.RED}❌ FLASK_DEBUG is enabled in production!{Colors.RESET}")
            issues.append('debug_enabled')
        else:
            print(f"{Colors.GREEN}✅ Debug mode disabled{Colors.RESET}")
        
        print(f"{Colors.GREEN}✅ HTTPS enforcement will be enabled{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Secure cookies will be enabled{Colors.RESET}")
        print(f"{Colors.GREEN}✅ HSTS will be enabled{Colors.RESET}")
        
    else:
        print(f"{Colors.BLUE}ℹ️  Running in DEVELOPMENT mode{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  HTTPS enforcement disabled{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠️  Secure cookies disabled{Colors.RESET}")
        print(f"   Set FLASK_ENV=production for production deployment")
    
    return issues, warnings

def check_file_security():
    """Check for common security misconfigurations in files"""
    print(f"\n{Colors.BOLD}📁 Checking File Security{Colors.RESET}")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # Check if .env exists and is not in git
    if os.path.exists('.env'):
        print(f"{Colors.GREEN}✅ .env file exists{Colors.RESET}")
        
        # Check if .env is in .gitignore
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
                if '.env' in gitignore_content:
                    print(f"{Colors.GREEN}✅ .env is in .gitignore{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ .env is NOT in .gitignore!{Colors.RESET}")
                    issues.append('.env_not_ignored')
    else:
        print(f"{Colors.YELLOW}⚠️  .env file not found{Colors.RESET}")
        print(f"   Copy from .env.example: cp .env.example .env")
        warnings.append('no_env_file')
    
    # Check .env.example exists
    if os.path.exists('.env.example'):
        print(f"{Colors.GREEN}✅ .env.example exists{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️  .env.example not found{Colors.RESET}")
        warnings.append('no_env_example')
    
    # Check for git hooks
    if os.path.exists('.git/hooks/pre-commit'):
        print(f"{Colors.GREEN}✅ Pre-commit hook installed{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️  Pre-commit hook not installed{Colors.RESET}")
        print(f"   Install with: ./scripts/install-hooks.sh")
        warnings.append('no_git_hooks')
    
    return issues, warnings

def generate_secret_key():
    """Generate a new secret key"""
    import secrets
    return secrets.token_hex(32)

def main():
    """Main validation function"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}SkyScope Environment Validation{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    
    all_issues = []
    all_warnings = []
    
    # Run all checks
    issues, warnings = check_required_env_vars()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_security_configuration()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    issues, warnings = check_file_security()
    all_issues.extend(issues)
    all_warnings.extend(warnings)
    
    # Print summary
    print(f"\n{Colors.BOLD}📊 Validation Summary{Colors.RESET}")
    print("=" * 60)
    
    if all_issues:
        print(f"{Colors.RED}❌ {len(all_issues)} Critical Issue(s) Found{Colors.RESET}")
        print(f"\n{Colors.RED}Critical issues must be fixed before deployment!{Colors.RESET}")
        return 1
    elif all_warnings:
        print(f"{Colors.YELLOW}⚠️  {len(all_warnings)} Warning(s) Found{Colors.RESET}")
        print(f"{Colors.GREEN}✅ No critical issues{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Warnings should be addressed before production deployment.{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.GREEN}✅ All Checks Passed!{Colors.RESET}")
        print(f"\n{Colors.GREEN}Environment is properly configured.{Colors.RESET}")
        return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validation cancelled by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Error during validation: {e}{Colors.RESET}")
        sys.exit(1)
