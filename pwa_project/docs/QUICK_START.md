# 🚀 Quick Start Guide

## ✅ **Your Django Task Manager is Ready!**

### **To Start the Server:**

**Option 1: Use the simple script**
```bash
./start_server.sh
```

**Option 2: Use the helper script**
```bash
./activate_and_run.sh runserver
```

**Option 3: Direct command (if you know what you're doing)**
```bash
fresh_venv/bin/python manage.py runserver
```

### **❌ DON'T USE:**
```bash
python3 manage.py runserver  # This won't work!
python manage.py runserver   # This won't work!
```

## 🌐 **Access Your Application:**

Once the server is running, open your browser to:

- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Task List**: http://127.0.0.1:8000/tasks/
- **Add Task**: http://127.0.0.1:8000/tasks/add

## 🔑 **Login Credentials:**
- **Username**: `admin`
- **Password**: `admin123`

## 📊 **What You'll See:**

### **Sample Categories Created:**
```
- Home
  - Chores
    - Clean kitchen
    - Do laundry
  - Sport
    - Go for a run
- School
  - Assignments
    - Complete project
    - Study for exam
- Work
  - Write report
  - Team meeting
```

## 🛠️ **Other Useful Commands:**

```bash
# Create new migrations
./activate_and_run.sh makemigrations

# Apply migrations
./activate_and_run.sh migrate

# Create a superuser
./activate_and_run.sh createsuperuser

# Setup demo data
./activate_and_run.sh setup_demo
```

## 🚨 **If Something Goes Wrong:**

1. **Server won't start**: Make sure you're using the virtual environment
2. **Can't access admin**: Check that the server is running
3. **Database issues**: Run `./activate_and_run.sh migrate`

## 🎯 **Success Indicators:**

You'll know everything is working when:
- ✅ Server starts without errors
- ✅ You can access http://127.0.0.1:8000/admin/ and login
- ✅ You can see categories and tasks in the admin interface
- ✅ You can access http://127.0.0.1:8000/tasks/ and see the hierarchical display

---

**🎉 Ready to go! Just run `./start_server.sh` and enjoy your hierarchical task manager!** 