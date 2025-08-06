#!/bin/bash

echo "🔄 Restarting ChipIn Django Server..."

# Kill any existing Django processes
pkill -f "python.*runserver" 2>/dev/null || true
sleep 2

# Clear Python cache
echo "🧹 Clearing Python cache..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Navigate to the correct directory
cd pwa_project/pwa_project

# Apply any pending migrations
echo "📊 Applying migrations..."
fresh_venv/bin/python manage.py migrate

# Start the server
echo "🚀 Starting Django server..."
echo "📱 Access your ChipIn app at: http://127.0.0.1:8000/"
echo "💰 Payment Dashboard: http://127.0.0.1:8000/tasks/payments/"
echo "🔧 Admin Interface: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

fresh_venv/bin/python manage.py runserver