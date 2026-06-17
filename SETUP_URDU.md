# 🚀 Backend API - Complete Setup Guide (اردو)

## ✅ Sabse Aasan Tareeqa

**START.bat** file par double-click karein!

Ya command prompt mein:
```
START.bat
```

Ye script automatically:
- Virtual environment activate karega
- Sab dependencies install karega
- Database setup karega  
- Admin user create karne ka option dega
- Server start karega

---

## 📝 Manual Setup (Agar automatic kaam na kare)

### Step 1: Virtual Environment Activate

```bash
venv\Scripts\activate
```

### Step 2: Dependencies Install (3-5 minutes lag sakte hain)

```bash
pip install -r requirements/dev.txt
```

### Step 3: Database Setup

```bash
# Migrations create
python manage.py makemigrations
python manage.py makemigrations users
python manage.py makemigrations authentication  
python manage.py makemigrations products
python manage.py makemigrations orders
python manage.py makemigrations payments
python manage.py makemigrations transactions
python manage.py makemigrations notifications

# Database migrate
python manage.py migrate
```

### Step 4: Admin User Create

```bash
python manage.py createsuperuser
```

Ye information deni hogi:
- **Email**: admin@example.com
- **Username**: admin
- **Full name**: Admin User
- **Password**: (koi bhi strong password)

### Step 5: Server Start

```bash
python manage.py runserver
```

---

## 🌐 URLs (Server start hone ke baad)

| Service | URL | Kya hai? |
|---------|-----|----------|
| **API Docs** | http://localhost:8000/api/docs/ | API test karne ke liye |
| **Admin Panel** | http://localhost:8000/admin/ | Data manage karne ke liye |
| **API Base** | http://localhost:8000/api/ | Main API URL |

---

## 🧪 API Test Kaise Karein

### Tareeqa 1: Swagger UI (Sabse Aasan)

1. Browser mein open karein: http://localhost:8000/api/docs/
2. Koi bhi endpoint click karein (jaise POST /api/auth/register/)
3. "Try it out" button click karein
4. Data enter karein
5. "Execute" click karein
6. Result dekho!

### Tareeqa 2: Postman

1. Postman download karein
2. New Request banao
3. Method: POST
4. URL: http://localhost:8000/api/auth/register/
5. Body → raw → JSON
6. Ye data enter karein:
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "password": "Test123!@#",
  "password_confirm": "Test123!@#"
}
```
7. Send click karein!

---

## 🎯 Available Features

✅ User Registration (Naya user bana sakte ho)
✅ Login/Logout (Secure authentication)
✅ Password Reset (Password bhool gaye to reset kar sakte ho)
✅ Products (Products dekh aur manage kar sakte ho)
✅ Orders (Orders create kar sakte ho)
✅ Payments (Payment track kar sakte ho)
✅ Notifications (Email aur system notifications)
✅ Role-Based Access (Admin, Manager, User roles)

---

## 🔧 Common Problems & Solutions

### Problem 1: "python not found"
**Solution**: Python install karo from python.org

### Problem 2: Virtual environment activate nahi ho raha
**Solution**: PowerShell mein ye command run karo:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Phir try karo: `.\venv\Scripts\Activate.ps1`

### Problem 3: "Module not found" error
**Solution**: Dependencies install karo:
```
pip install -r requirements/dev.txt
```

### Problem 4: Port already in use
**Solution**: Different port use karo:
```
python manage.py runserver 8001
```

### Problem 5: Django import nahi ho raha
**Solution**: 
1. Virtual environment activate hai? Check karo `(venv)` dikhna chahiye terminal mein
2. Dependencies install karo: `pip install django`

---

## 📚 API Endpoints

### Authentication (کھاتہ)
- `POST /api/auth/register/` - Naya user banao
- `POST /api/auth/login/` - Login karo
- `POST /api/auth/logout/` - Logout karo
- `POST /api/auth/password-reset/` - Password reset request

### Users (صارف)
- `GET /api/users/me/` - Apna profile dekho
- `GET /api/users/` - Sab users dekho (Admin only)

### Products (مصنوعات)
- `GET /api/products/` - Sab products dekho
- `POST /api/products/` - Naya product banao (Manager/Admin)
- `GET /api/products/{slug}/` - Product details

### Orders (آرڈرز)
- `GET /api/orders/` - Apne orders dekho
- `POST /api/orders/` - Naya order banao
- `GET /api/orders/{id}/` - Order details

### Payments (ادائیگی)
- `GET /api/payments/` - Apni payments dekho
- `GET /api/payments/{id}/` - Payment details

### Notifications (اطلاعات)
- `GET /api/notifications/` - Apni notifications dekho
- `POST /api/notifications/{id}/mark_read/` - Notification ko read mark karo

---

## 💡 Tips

1. **Admin Panel** se data easily manage kar sakte ho
2. **Swagger Docs** se API testing easiest hai
3. Development mein emails console mein print honge
4. **SQLite** database use ho raha hai (db.sqlite3 file)
5. **.env** file mein settings change kar sakte ho

---

## 🆘 Help Chahiye?

1. **Virtual environment active hai?** - Terminal mein `(venv)` dikhna chahiye
2. **Dependencies installed hain?** - `pip list` run karke check karo
3. **Database migrate hua?** - `python manage.py showmigrations` se check karo
4. **Server chal raha hai?** - http://localhost:8000 open hona chahiye

---

## 🎉 Success Kaise Patachale?

Agar server start ho gaya aur ye URL open ho raha hai, to setup successful hai:

✅ http://localhost:8000/api/docs/

Mubarak ho! 🎊 Ab aap API use kar sakte ho!

---

## 📞 Contact

Koi problem ho to:
- Swagger docs check karo
- Console logs dekho
- Error messages padho - wo solution bata dete hain!

**Happy Coding! 💻**
