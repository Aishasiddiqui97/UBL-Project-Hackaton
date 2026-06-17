# API Usage Guide

Complete guide for using the Backend API endpoints.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Most endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Authentication

#### Register User
```bash
POST /auth/register/

Request:
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}

Response: 201 Created
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "John Doe",
    "role": "USER"
  }
}
```

#### Login
```bash
POST /auth/login/

Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "role": "USER"
    }
  }
}
```

#### Logout
```bash
POST /auth/logout/
Authorization: Bearer <access_token>

Request:
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "success": true,
  "message": "Logout successful"
}
```

#### Password Reset Request
```bash
POST /auth/password-reset/

Request:
{
  "email": "user@example.com"
}

Response: 200 OK
{
  "success": true,
  "message": "Password reset link sent to your email"
}
```

#### Password Reset Confirm
```bash
POST /auth/password-reset/confirm/

Request:
{
  "token": "reset_token_here",
  "password": "NewSecurePass123!",
  "password_confirm": "NewSecurePass123!"
}

Response: 200 OK
{
  "success": true,
  "message": "Password reset successful"
}
```

### 2. Users

#### Get Current User Profile
```bash
GET /users/me/
Authorization: Bearer <access_token>

Response: 200 OK
{
  "success": true,
  "message": "User profile retrieved",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "John Doe",
    "role": "USER"
  }
}
```

#### List All Users (Admin Only)
```bash
GET /users/
Authorization: Bearer <admin_access_token>

Query Parameters:
- page: Page number (default: 1)
- page_size: Items per page (default: 20)
- role: Filter by role (ADMIN, MANAGER, USER)
- search: Search in email, username, full_name
- ordering: Sort by field (created_at, email)

Response: 200 OK
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [...]
}
```

#### Update User
```bash
PATCH /users/{id}/
Authorization: Bearer <access_token>

Request:
{
  "full_name": "Updated Name"
}

Response: 200 OK
```

### 3. Products

#### List Products
```bash
GET /products/

Query Parameters:
- page: Page number
- page_size: Items per page
- category: Filter by category ID
- search: Search in name, description
- ordering: Sort by price, created_at, name

Response: 200 OK
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      "slug": "product-name",
      "description": "Product description",
      "price": "99.99",
      "stock": 100,
      "category": 1,
      "category_name": "Electronics",
      "in_stock": true,
      "image": "/media/products/image.jpg"
    }
  ]
}
```

#### Get Product Details
```bash
GET /products/{slug}/

Response: 200 OK
```

#### Create Product (Manager/Admin Only)
```bash
POST /products/
Authorization: Bearer <manager_access_token>
Content-Type: multipart/form-data

Request:
{
  "name": "New Product",
  "description": "Product description",
  "price": "99.99",
  "stock": 100,
  "category": 1,
  "image": <file>
}

Response: 201 Created
```

#### List Categories
```bash
GET /products/categories/

Response: 200 OK
```

### 4. Orders

#### Create Order
```bash
POST /orders/
Authorization: Bearer <access_token>

Request:
{
  "shipping_address": "123 Main St, City, Country",
  "notes": "Please deliver in the morning",
  "items": [
    {
      "product": 1,
      "quantity": 2
    },
    {
      "product": 3,
      "quantity": 1
    }
  ]
}

Response: 201 Created
{
  "success": true,
  "message": "Order created successfully",
  "data": {
    "id": 1,
    "user": 1,
    "status": "PENDING",
    "total_amount": "299.97",
    "items": [...]
  }
}
```

#### List My Orders
```bash
GET /orders/
Authorization: Bearer <access_token>

Query Parameters:
- status: Filter by status (PENDING, PROCESSING, COMPLETED, CANCELLED)
- ordering: Sort by created_at, total_amount

Response: 200 OK
```

#### Get Order Details
```bash
GET /orders/{id}/
Authorization: Bearer <access_token>

Response: 200 OK
```

#### Cancel Order (Manager/Admin Only)
```bash
POST /orders/{id}/cancel/
Authorization: Bearer <manager_access_token>

Response: 200 OK
{
  "success": true,
  "message": "Order cancelled successfully"
}
```

### 5. Payments

#### List My Payments
```bash
GET /payments/
Authorization: Bearer <access_token>

Query Parameters:
- status: Filter by status
- method: Filter by payment method
- ordering: Sort by created_at, amount

Response: 200 OK
```

#### Get Payment Details
```bash
GET /payments/{id}/
Authorization: Bearer <access_token>

Response: 200 OK
```

### 6. Transactions

#### List My Transactions
```bash
GET /transactions/
Authorization: Bearer <access_token>

Query Parameters:
- transaction_type: Filter by type (DEBIT, CREDIT)
- status: Filter by status
- ordering: Sort by created_at, amount

Response: 200 OK
```

### 7. Notifications

#### List My Notifications
```bash
GET /notifications/
Authorization: Bearer <access_token>

Query Parameters:
- is_read: Filter by read status (true/false)
- notification_type: Filter by type (EMAIL, SYSTEM)

Response: 200 OK
```

#### Mark Notification as Read
```bash
POST /notifications/{id}/mark_read/
Authorization: Bearer <access_token>

Response: 200 OK
{
  "success": true,
  "message": "Notification marked as read"
}
```

#### Mark All Notifications as Read
```bash
POST /notifications/mark_all_read/
Authorization: Bearer <access_token>

Response: 200 OK
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

Common HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Too Many Requests (rate limited)
- 500: Internal Server Error

## Testing with cURL

### Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### Use Token
```bash
# Get user profile
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Rate Limiting

The following endpoints have rate limiting:

- `/auth/register/`: 5 requests per hour per IP
- `/auth/login/`: 10 requests per hour per IP
- `/auth/password-reset/`: 3 requests per hour per IP

## Pagination

List endpoints support pagination:

```
GET /api/products/?page=2&page_size=10
```

Response includes:
- `count`: Total number of items
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of items

## Filtering and Searching

Use query parameters:

```
# Search products
GET /api/products/?search=laptop

# Filter by category
GET /api/products/?category=1

# Combine filters
GET /api/products/?category=1&search=laptop&ordering=-price
```

## Best Practices

1. Always use HTTPS in production
2. Store tokens securely
3. Refresh access tokens before expiry
4. Handle rate limiting gracefully
5. Validate input on client side
6. Log out users properly
7. Use appropriate HTTP methods
8. Handle errors appropriately

## Support

For API issues, check:
- Swagger documentation: http://localhost:8000/api/docs/
- Application logs
- HTTP status codes and error messages
