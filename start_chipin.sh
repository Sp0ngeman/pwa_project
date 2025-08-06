#!/bin/bash

echo "🎓 ChipIn Assignment - HSC Software Engineering"
echo "==============================================="
echo ""
echo "🚀 Starting ChipIn Platform with new virtual environment..."
echo ""

# Navigate to project directory
cd pwa_project/pwa_project

# Activate virtual environment and start server
echo "📱 Starting Django server..."
echo ""
echo "🌐 Access URLs:"
echo "   Main App: http://127.0.0.1:8000/"
echo "   Payment Dashboard: http://127.0.0.1:8000/tasks/payments/"
echo "   Admin Interface: http://127.0.0.1:8000/admin/"
echo ""
echo "🔐 Login Credentials:"
echo "   Username: sponge"
echo "   Email: wollybidk@outlook.com"
echo "   Password: [the password you just set]"
echo ""
echo "💰 ChipIn Demo Features:"
echo "   • Secure Payment Processing"
echo "   • Trusted Adult Oversight (Demo code: PARENT123)"
echo "   • Balance Management"
echo "   • Transaction History"
echo "   • Spending Limits"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Django development server
../chipin_venv/bin/python manage.py runserver