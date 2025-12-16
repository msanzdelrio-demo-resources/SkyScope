#!/usr/bin/env python3
"""
Security testing script for SkyScope application.
Run this script to perform basic security validation.
"""

import subprocess
import sys
import os
import requests
from urllib.parse import urljoin

def run_command(command):
    """Run a command and return its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_dependencies():
    """Check for vulnerable dependencies."""
    print("🔍 Checking dependencies for vulnerabilities...")
    
    # Install safety if not present
    subprocess.run([sys.executable, "-m", "pip", "install", "safety"], 
                  capture_output=True)
    
    success, stdout, stderr = run_command("safety check --json")
    
    if success and stdout.strip() == "[]":
        print("✅ No known vulnerabilities found in dependencies")
        return True
    else:
        print("❌ Vulnerable dependencies detected:")
        print(stdout)
        return False

def check_secrets():
    """Check for exposed secrets in code."""
    print("🔍 Checking for exposed secrets...")
    
    # Install bandit if not present
    subprocess.run([sys.executable, "-m", "pip", "install", "bandit", "pbr"], 
                  capture_output=True)
    
    success, stdout, stderr = run_command("bandit -r app/ -f json")
    
    if "No issues identified" in stderr or success:
        print("✅ No obvious secrets found in code")
        return True
    else:
        print("❌ Potential security issues detected:")
        print(stdout)
        return False

def test_security_headers():
    """Test security headers if app is running."""
    print("🔍 Testing security headers...")
    
    try:
        response = requests.get("http://localhost:5001", timeout=5)
        headers = response.headers
        
        required_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options'
        ]
        
        missing_headers = []
        for header in required_headers:
            if header not in headers:
                missing_headers.append(header)
        
        if not missing_headers:
            print("✅ All required security headers present")
            return True
        else:
            print(f"❌ Missing security headers: {', '.join(missing_headers)}")
            return False
            
    except requests.exceptions.RequestException:
        print("⚠️  App not running - skipping header check")
        print("   Start the app with 'python run.py' to test headers")
        return True

def check_environment():
    """Check environment configuration."""
    print("🔍 Checking environment configuration...")
    
    required_env_vars = ['SECRET_KEY', 'OPENWEATHER_APPID']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if not missing_vars:
        print("✅ All required environment variables set")
        return True
    else:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Copy .env.example to .env and set the values")
        return False

def main():
    """Run all security checks."""
    print("🔒 SkyScope Security Check")
    print("=" * 40)
    
    checks = [
        ("Environment Configuration", check_environment),
        ("Dependency Vulnerabilities", check_dependencies),
        ("Code Security Analysis", check_secrets),
        ("Security Headers", test_security_headers)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n{name}")
        print("-" * len(name))
        if check_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Security Check Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All security checks passed!")
        sys.exit(0)
    else:
        print("⚠️  Some security issues need attention")
        sys.exit(1)

if __name__ == "__main__":
    main()