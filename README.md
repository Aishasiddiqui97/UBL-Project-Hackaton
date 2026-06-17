# Backend API - Production Ready Django Application

A secure, scalable, and production-ready backend system built with Django 5+ and Django REST Framework.

## 🚀 Features

- **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin, Manager, User)
  - Password reset functionality
  - Refresh token management

- **User Management**
  - Custom user model with email authentication
  - User registration and profile management
  - Permission-based access control

- **Product Management**
  - Categories and products CRUD
  - Product search and filtering
  - Image upload support
  - Stock management

- **Order Management**
  - Order creation with multiple items
  - Order status tracking
  - Transaction management with rollback support

- **Payment System**
  - Multiple payment methods
  - Transaction history
  - Payment status tracking

- **Notifications**
  - Email notifications
  - System notifications
  - Read/unread status

- **Security**
  - Password hashing
  - Rate limiting on sensitive endpoints
  - SQL injection protection
  - CORS configuration
  - Input validation

- **API Documentation**
  - Swagger/OpenAPI documentation
  - Auto-generated API schemas

## 📋 Requirements

- Python 3.12+
- PostgreSQL 12+ (or SQLite for development)
- Docker & Docker Compose (optional)

## 🛠 Installation

### Local Development

1. **Clone the repository**


2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements/dev.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

### Docker Deployment

1. **Build and run containers**
```bash
docker-compose up --build
```

2. **Run migrations**
```bash
docker-compose exec backend python manage.py migrate
```

3. **Create superuser**
```bash
docker-compose exec backend python manage.py createsuperuser
```

## 📚 API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Authentication

### Register
```bash
POST /api/auth/register/
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

### Login
```bash
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Use Token
```bash
Authorization: Bearer <access_token>
```

## 🧪 Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=apps --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_authentication.py
```

## 📁 Project Structure

```
backend/
├── apps/
│   ├── authentication/    # JWT auth, login, logout
│   ├── users/            # User management
│   ├── products/         # Product & category management
│   ├── orders/           # Order processing
│   ├── payments/         # Payment handling
│   ├── transactions/     # Transaction records
│   └── notifications/    # Email & system notifications
├── config/               # Django settings & configuration
├── requirements/         # Dependency files
├── tests/               # Test files
├── media/               # User uploaded files
├── static/              # Static files
├── manage.py            # Django management script
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose setup
```

## 🔑 User Roles & Permissions

### Admin
- Full access to all endpoints
- User management
- System configuration

### Manager
- Manage products, orders, payments
- View reports
- Limited user management

### User
- View own data
- Create orders
- View own transactions

## 🚀 Deployment

### Environment Variables

Configure the following in your `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set strong `SECRET_KEY`
- [ ] Configure email settings
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Configure static files serving
- [ ] Set up logging and monitoring
- [ ] Enable rate limiting
- [ ] Regular database backups

## 📊 Database Schema

All models include common fields:
- `id`: Primary key
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update
- `is_active`: Soft delete flag

## 🔒 Security Features

- Password hashing with Django's built-in system
- JWT token authentication
- Rate limiting on login, registration, password reset
- CORS protection
- SQL injection prevention through ORM
- Input validation on all endpoints
- HTTPS enforcement in production
- CSRF protection

## 📝 API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "errors": {}
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Support

For issues and questions, please create an issue in the repository.
