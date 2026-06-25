#!/usr/bin/env python
"""Quick authentication test script."""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from apps.authentication.serializers import LoginSerializer

User = get_user_model()

def test_django_auth():
    """Test Django authentication."""
    print("=" * 50)
    print("TESTING DJANGO AUTHENTICATION")
    print("=" * 50)
    
    # Test user exists
    try:
        user = User.objects.get(email='admin@example.com')
        print(f"✅ User found: {user.email} (Active: {user.is_active})")
    except User.DoesNotExist:
        print("❌ User not found")
        return False
    
    # Test password
    if user.check_password('admin123'):
        print("✅ Password correct")
    else:
        print("❌ Password incorrect")
        return False
    
    # Test authentication backend
    auth_user = authenticate(username='admin@example.com', password='admin123')
    if auth_user:
        print("✅ Authentication backend works")
    else:
        print("❌ Authentication backend failed")
        return False
    
    # Test serializer
    data = {'email': 'admin@example.com', 'password': 'admin123'}
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        print("✅ Login serializer valid")
    else:
        print(f"❌ Login serializer invalid: {serializer.errors}")
        return False
    
    return True

def test_api_auth():
    """Test API authentication."""
    print("\n" + "=" * 50)
    print("TESTING API AUTHENTICATION")
    print("=" * 50)
    
    # Test login API
    url = 'http://localhost:8000/api/auth/login/'
    data = {
        'email': 'admin@example.com',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login API successful")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Login API failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        print("Note: Make sure Django server is running on localhost:8000")
        return False

if __name__ == "__main__":
    print("🔐 Authentication Test Suite")
    print("Make sure Django server is running: python manage.py runserver\n")
    
    django_ok = test_django_auth()
    api_ok = test_api_auth()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    print(f"Django Auth: {'✅ PASS' if django_ok else '❌ FAIL'}")
    print(f"API Auth: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if django_ok and api_ok:
        print("\n🎉 All tests passed! Authentication is working.")
        print("\nCredentials for frontend:")
        print("Email: admin@example.com")
        print("Password: admin123")
    else:
        print("\n❌ Some tests failed. Check the output above.")