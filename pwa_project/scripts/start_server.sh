#!/bin/bash

echo "🚀 Starting Django Task Manager Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "fresh_venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: python3 -m venv fresh_venv"
    exit 1
fi

# Start the server
echo "✅ Using virtual environment: fresh_venv"
echo "🌐 Starting server at http://127.0.0.1:8000/"
echo ""
echo "📱 Access URLs:"
echo "   Main App: http://127.0.0.1:8000/"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo "   Tasks: http://127.0.0.1:8000/tasks/"
echo ""
echo "🔑 Login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Django server
fresh_venv/bin/python manage.py runserver 