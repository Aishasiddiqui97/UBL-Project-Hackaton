#!/usr/bin/env python
"""Test transaction creation API."""
import requests
import json

# Login first
login_data = {
    "email": "admin@example.com",
    "password": "admin123"
}

login_response = requests.post(
    'http://localhost:8000/api/auth/login/',
    json=login_data
)

if login_response.status_code == 200:
    token = login_response.json()['data']['access_token']
    print("✅ Login successful")
    
    # Create transaction
    transaction_data = {
        "transaction_type": "DEBIT",
        "amount": "25000.00",
        "account_number": "ACC-TEST-001",
        "description": "Test transaction from API",
        "location": "Karachi"
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    create_response = requests.post(
        'http://localhost:8000/api/transactions/',
        json=transaction_data,
        headers=headers
    )
    
    print(f"Create Transaction Status: {create_response.status_code}")
    if create_response.status_code in [200, 201]:
        result = create_response.json()
        print("✅ Transaction created successfully")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Failed to create transaction")
        print(create_response.text)
        
else:
    print("❌ Login failed")
    print(login_response.text)