"""
Test script to verify Market Newsletter Generator setup
Checks all dependencies and credentials before running main script
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_python_version():
    """Check Python version"""
    print("="*60)
    print("1. Python Environment")
    print("="*60)
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✓ Python version: {version}")
    if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 8):
        print("⚠ Warning: Python 3.8+ recommended")
    print()

def test_imports():
    """Check if all required packages are installed"""
    print("="*60)
    print("2. Required Packages")
    print("="*60)
    
    packages = {
        'openai': 'OpenAI API client',
        'requests': 'HTTP requests library',
        'dotenv': 'Environment variable management'
    }
    
    all_ok = True
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✓ {package}: {description}")
        except ImportError:
            print(f"✗ {package}: NOT INSTALLED - {description}")
            all_ok = False
    
    if not all_ok:
        print("\n⚠ Install missing packages with:")
        print("  pip install -r requirements.txt")
    print()
    return all_ok

def test_env_file():
    """Check if .env file exists"""
    print("="*60)
    print("3. Configuration File")
    print("="*60)
    
    env_path = Path('.env')
    if env_path.exists():
        print(f"✓ .env file found at: {env_path.absolute()}")
    else:
        print(f"✗ .env file NOT found")
        print(f"  Create it by running: copy .env.example .env")
        print()
        return False
    print()
    return True

def test_env_variables():
    """Check if all required environment variables are set"""
    print("="*60)
    print("4. Environment Variables")
    print("="*60)
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key (starts with sk-)',
        'NEWSAPI_KEY': 'NewsAPI key',
        'GMAIL_USER': 'Gmail address',
        'GMAIL_PASSWORD': 'Gmail app-specific password',
        'RECIPIENT_EMAIL': 'Email to send newsletter to'
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Show masked value for sensitive data
            if 'KEY' in var or 'PASSWORD' in var:
                masked = value[:6] + '*' * (len(value) - 10) + value[-4:]
                print(f"✓ {var}: {masked} ({description})")
            else:
                print(f"✓ {var}: {value} ({description})")
        else:
            print(f"✗ {var}: NOT SET ({description})")
            all_set = False
    
    if not all_set:
        print("\n⚠ Missing environment variables!")
        print("  Edit .env file and add all required values")
    print()
    return all_set

def test_openai_connection():
    """Test connection to OpenAI API"""
    print("="*60)
    print("5. OpenAI API Connection")
    print("="*60)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OpenAI API key not set")
        print()
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # List models to verify connection
        models = client.models.list()
        model_count = len(list(models))
        
        print(f"✓ Connected to OpenAI")
        print(f"  Available models: {model_count}")
        print()
        return True
    except Exception as e:
        print(f"✗ Failed to connect to OpenAI: {e}")
        print("  Check your API key at: https://platform.openai.com/api-keys")
        print()
        return False

def test_newsapi_connection():
    """Test connection to NewsAPI"""
    print("="*60)
    print("6. NewsAPI Connection")
    print("="*60)
    
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("✗ NewsAPI key not set")
        print()
        return False
    
    try:
        import requests
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "apiKey": api_key,
            "pageSize": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok':
            print(f"✓ Connected to NewsAPI")
            print(f"  Total articles available: {data.get('totalResults', 'unknown')}")
            print()
            return True
        else:
            print(f"✗ NewsAPI returned error: {data.get('message')}")
            print("  Check your API key at: https://newsapi.org/account")
            print()
            return False
    except Exception as e:
        print(f"✗ Failed to connect to NewsAPI: {e}")
        print()
        return False

def test_gmail_connection():
    """Test Gmail SMTP connection"""
    print("="*60)
    print("7. Gmail SMTP Connection")
    print("="*60)
    
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    
    if not gmail_user or not gmail_password:
        print("✗ Gmail credentials not set")
        print()
        return False
    
    try:
        import smtplib
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5)
        server.login(gmail_user, gmail_password)
        server.quit()
        
        print(f"✓ Connected to Gmail SMTP")
        print(f"  Account: {gmail_user}")
        print()
        return True
    except smtplib.SMTPAuthenticationError:
        print(f"✗ Gmail authentication failed")
        print("  Check:")
        print("    - Correct Gmail address in .env")
        print("    - App password (not regular password)")
        print("    - 2-Step Verification enabled")
        print("  Get app password at: https://myaccount.google.com/apppasswords")
        print()
        return False
    except Exception as e:
        print(f"✗ Failed to connect to Gmail: {e}")
        print()
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "    MARKET NEWSLETTER - SETUP VERIFICATION".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print()
    
    results = []
    
    # Run all tests
    test_python_version()
    results.append(("Packages", test_imports()))
    results.append((".env file", test_env_file()))
    results.append(("Environment Variables", test_env_variables()))
    results.append(("OpenAI API", test_openai_connection()))
    results.append(("NewsAPI", test_newsapi_connection()))
    results.append(("Gmail SMTP", test_gmail_connection()))
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✓ ALL TESTS PASSED!")
        print()
        print("You're ready to run the newsletter:")
        print("  python main.py")
        print()
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print()
        print("Fix the issues above and try again.")
        print()
        print("For help, see QUICKSTART.md or README.md")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
