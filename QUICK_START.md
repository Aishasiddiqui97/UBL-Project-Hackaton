# 🚀 Quick Start Guide (Urdu/English)

## ⚡ Fastest Way to Start (Windows)

```bash
# Simply double-click setup_windows.bat
# Ya command prompt mein run karein:
setup_windows.bat
```

Ye script automatically:
- Virtual environment create karega
- Dependencies install karega
- Database setup karega
- Superuser create karne ka option dega
- Server start kar dega

---

## 📝 Manual Setup (Step by Step)

### 1️⃣ Virtual Environment Create karein

```bash
python -m venv venv
```

### 2️⃣ Virtual Environment Activate karein

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3️⃣ Dependencies Install karein

```bash
pip install -r requirements/dev.txt
```

### 4️⃣ Database Setup karein

```bash
# Migrations create karein
python manage.py makemigrations

# Database setup karein
python manage.py migrate
```

### 5️⃣ Admin User Create karein

```bash
python manage.py createsuperuser
```

Ye information deni hogi:
- **Email**: admin@example.com
- **Username**: admin
- **Full Name**: Admin User
- **Password**: (strong password choose karein)

### 6️⃣ Server Start karein

```bash
python manage.py runserver
```

---

## 🌐 Access URLs

Server start hone ke baad ye URLs open karein:

| Service | URL | Description |
|---------|-----|-------------|
| **Swagger Docs** | http://localhost:8000/api/docs/ | Interactive API documentation |
| **ReDoc** | http://localhost:8000/api/redoc/ | Alternative API docs |
| **Admin Panel** | http://localhost:8000/admin/ | Django admin interface |
| **API Base** | http://localhost:8000/api/ | API endpoints base URL |

---

## 🧪 API Test karna

### Option 1: Swagger UI Use karein (Easiest)

1. Open karein: http://localhost:8000/api/docs/
2. "Try it out" button click karein
3. Request data enter karein
4. "Execute" click karein

### Option 2: cURL Use karein

**Register New User:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"full_name\":\"Test User\",\"password\":\"Test123!@#\",\"password_confirm\":\"Test123!@#\"}"
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"Test123!@#\"}"
```

Response mein **access_token** milega, use karein:

```bash
curl -X GET http://localhost:8000/api/users/me/ ^
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Option 3: Postman Use karein

1. Postman download karein
2. New request create karein
3. URL enter karein: `http://localhost:8000/api/auth/login/`
4. Method: POST
5. Body → raw → JSON select karein
6. Request data enter karein

---

## 🔧 Common Issues & Solutions

### Issue 1: "python not found"
**Solution:** Python 3.12+ install karein from python.org

### Issue 2: "pip not found"
**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue 3: "Module not found"
**Solution:**
```bash
pip install -r requirements/dev.txt
```

### Issue 4: "Port already in use"
**Solution:** Different port use karein:
```bash
python manage.py runserver 8001
```

### Issue 5: Database errors
**Solution:** Database reset karein:
```bash
# SQLite file delete karein
del db.sqlite3

# Migrations re-run karein
python manage.py migrate
```

---

## 📊 Test karein

```bash
# All tests run karein
pytest

# Coverage ke saath
pytest --cov=apps

# Specific test file
pytest tests/test_authentication.py
```

---

## 🐳 Docker se Run karein (Optional)

Agar Docker installed hai:

```bash
# Build and start
docker-compose up --build

# Separate terminal mein migrations run karein
docker-compose exec backend python manage.py migrate

# Superuser create karein
docker-compose exec backend python manage.py createsuperuser
```

---

## 📱 Frontend Connect karna

Agar frontend app hai (React, Vue, etc.):

1. `.env` file mein CORS settings already set hain
2. Frontend se API call karein:

```javascript
// Example: Login API call
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
const token = data.data.access_token;

// Token use karke protected endpoint access karein
const userResponse = await fetch('http://localhost:8000/api/users/me/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

## 🎯 Available Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset
- `POST /api/auth/token/refresh/` - Refresh access token

### Users
- `GET /api/users/` - List users (Admin only)
- `GET /api/users/me/` - Current user profile
- `GET /api/users/{id}/` - User details
- `PATCH /api/users/{id}/` - Update user

### Products
- `GET /api/products/` - List products
- `POST /api/products/` - Create product (Manager/Admin)
- `GET /api/products/{slug}/` - Product details
- `PATCH /api/products/{slug}/` - Update product
- `DELETE /api/products/{slug}/` - Delete product

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Order details
- `POST /api/orders/{id}/cancel/` - Cancel order

### More endpoints available in Swagger docs!

---

## 💡 Tips

1. **Development mein** DEBUG=True rakhen
2. **Production mein** DEBUG=False aur strong SECRET_KEY use karein
3. **Emails** console mein print honge (development mode)
4. **Admin panel** se data easily manage kar sakte hain
5. **Swagger docs** se API test karna easiest hai

---

## 🆘 Help

Koi problem aa rahi hai? Check karein:

1. Python version: `python --version` (3.12+ hona chahiye)
2. Virtual environment active hai? (terminal mein `(venv)` dikhna chahiye)
3. Dependencies installed hain? `pip list`
4. Database migrations run hue? `python manage.py showmigrations`

---

## 🎉 Success!

Agar server chal raha hai aur http://localhost:8000/api/docs/ open ho raha hai, to setup successful hai! 🎊
