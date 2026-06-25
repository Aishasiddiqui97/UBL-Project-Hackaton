#!/usr/bin/env python
"""Reset admin password."""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Reset admin password
try:
    user = User.objects.get(email='admin@example.com')
    user.set_password('admin123')
    user.save()
    print("✅ Admin password reset to 'admin123'")
    print(f"Email: {user.email}")
    print(f"Active: {user.is_active}")
    print(f"Password check: {user.check_password('admin123')}")
except User.DoesNotExist:
    # Create new admin user
    user = User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        username='admin',
        full_name='Admin User'
    )
    print("✅ New admin user created")
    print(f"Email: {user.email}")
    print(f"Password: admin123")