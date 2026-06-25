# 🚨 QUICK FIX: "Given token not valid" Error

## **IMMEDIATE SOLUTION (30 seconds):**

### **Step 1: Clear Browser Storage**
1. Open browser (Chrome/Edge/Firefox)
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Copy and paste this command:

```javascript
// Clear all auth data
localStorage.clear();
sessionStorage.clear();
console.log('✅ All storage cleared!');

// Refresh page
window.location.reload();
```

5. Press **Enter**
6. Page will refresh automatically

### **Step 2: Try Login Again**
```
Email: admin@example.com
Password: admin123
```

---

## **Alternative Method - Manual Clear:**

1. **F12** → **Application** tab (Chrome) or **Storage** tab (Firefox)
2. **Local Storage** → **http://localhost:3000**
3. Delete these keys:
   - `access_token`
   - `refresh_token` 
   - `isAuthenticated`
   - `user`
4. **Refresh page** (F5)

---

## **If Still Not Working:**

### **Backend Check:**
```bash
# Stop and restart Django server
# Press Ctrl+C in backend terminal
.\RUN_SERVER.bat
```

### **Frontend Check:**
```bash
# Stop and restart frontend
# Press Ctrl+C in frontend terminal
npm run dev
```

### **Verify Credentials:**
```bash
# Reset admin password
python reset_admin_password.py
```

---

## **Root Cause:**
Your browser had an old/invalid JWT token stored. After clearing storage, the login will work with fresh tokens.

## **Why This Happened:**
- Previous authentication attempts left invalid tokens
- JWT tokens can expire or become malformed
- Browser cached old authentication state

---

## **Expected Result:**
✅ Login page loads without error
✅ Can enter email/password
✅ Successful login redirects to dashboard
✅ No more "token not valid" error

**This should fix your issue immediately!** 🚀