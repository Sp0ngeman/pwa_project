#!/bin/bash

echo "🚀 ChipIn Assignment Project Startup"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "fresh_venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv fresh_venv
    echo "Installing requirements..."
    fresh_venv/bin/pip install django django-allauth django-cors-headers requests
fi

# Check database
echo "🔧 Checking database..."
fresh_venv/bin/python manage.py check

# Apply migrations
echo "📦 Applying database migrations..."
fresh_venv/bin/python manage.py migrate

echo ""
echo "✅ Project ready!"
echo "🌐 Starting development server..."
echo "📱 Access at: http://127.0.0.1:8000/"
echo "🔑 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start server
fresh_venv/bin/python manage.py runserver