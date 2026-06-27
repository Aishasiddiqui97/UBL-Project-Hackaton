# Start Backend & Frontend Servers

## Quick Start Commands

### Backend Server
```bash
# Navigate to project root
cd "E:\Python.py\Hackaton project UBL"

# Activate virtual environment
.\venv\Scripts\activate

# Start Django backend
python manage.py runserver
```
**Backend URL:** http://localhost:8000/

### Frontend Server
```bash
# Open new terminal/command prompt
cd "E:\Python.py\Hackaton project UBL\frontend"

# Start React frontend
npm run dev
```
**Frontend URL:** http://localhost:3000/

## Login Credentials
- Email: admin@example.com
- Password: admin123

## If Port 3000 is Busy

Check what's using port 3000:
```powershell
netstat -ano | Select-String ":3000"
```

Kill the process:
```powershell
# Replace 4808 with your PID
taskkill /F /PID 4808
```

Then restart frontend.

## API Documentation
- Swagger: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin Panel: http://localhost:8000/admin/

## Troubleshooting

### Backend not starting
```bash
# Check if virtual environment is activated
.\venv\Scripts\activate

# Install missing packages
pip install -r requirements/base.txt

# Run migrations
python manage.py migrate
```

### Frontend blank page
1. Hard refresh browser: `Ctrl + F5`
2. Clear browser cache
3. Check browser console (F12) for errors
4. Verify backend is running on port 8000

### Port already in use
**For port 3000 (Frontend):**
```powershell
netstat -ano | Select-String ":3000"
taskkill /F /PID <PID_NUMBER>
```

**For port 8000 (Backend):**
```powershell
netstat -ano | Select-String ":8000"
taskkill /F /PID <PID_NUMBER>
```

## Running Both Servers

### Option 1: Two Separate Terminals
1. Terminal 1: Start backend
2. Terminal 2: Start frontend

### Option 2: Use provided scripts
```bash
# Backend
START.bat

# Frontend (navigate to frontend folder first)
npm run dev
```

## Current Status ✅

Both servers are now running:
- ✅ Backend: http://localhost:8000/
- ✅ Frontend: http://localhost:3000/
- ✅ Database: 10 fraud alerts, 57+ transactions
- ✅ Authentication: JWT with refresh tokens
- ✅ CORS: Configured for localhost:3000

## Test the Application

1. Open browser: http://localhost:3000
2. Login with: admin@example.com / admin123
3. Navigate to:
   - Dashboard
   - Transaction Monitoring
   - Fraud Detection (10 alerts should show)
4. Open F12 console to see debug logs

## Stop Servers

**Backend:** Press `Ctrl + C` in backend terminal

**Frontend:** Press `Ctrl + C` in frontend terminal

## Need Help?

If you see blank page:
1. Check both servers are running
2. Hard refresh: Ctrl + F5
3. Check browser console for errors
4. Verify CORS settings in config/settings.py
5. Clear localStorage: Run in browser console:
   ```javascript
   localStorage.clear()
   location.reload()
   ```

Everything is ready! Just refresh your browser at http://localhost:3000 🎉
