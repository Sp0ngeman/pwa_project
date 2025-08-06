#!/bin/bash

# Script to activate the virtual environment and run Django commands

echo "=== Django Task Manager Setup ==="
echo ""

# Check if fresh_venv exists
if [ ! -d "fresh_venv" ]; then
    echo "Error: Virtual environment 'fresh_venv' not found!"
    echo "Please run: python3 -m venv fresh_venv"
    exit 1
fi

# Function to run Django commands
run_django_command() {
    echo "Running: $1"
    fresh_venv/bin/python manage.py $1
    echo ""
}

# Function to run pip install
install_package() {
    echo "Installing: $1"
    fresh_venv/bin/pip install $1
    echo ""
}

# Show available commands
echo "Available commands:"
echo "1. runserver - Start the development server"
echo "2. makemigrations - Create database migrations"
echo "3. migrate - Apply database migrations"
echo "4. createsuperuser - Create a superuser account"
echo "5. shell - Open Django shell"
echo "6. setup_demo - Run the demo data setup script"
echo ""

# Check command line arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 [command]"
    echo ""
    echo "Examples:"
    echo "  $0 runserver"
    echo "  $0 makemigrations"
    echo "  $0 migrate"
    echo "  $0 setup_demo"
    exit 1
fi

case "$1" in
    "runserver")
        echo "Starting Django development server..."
        echo "Access the application at: http://127.0.0.1:8000/"
        echo "Admin interface: http://127.0.0.1:8000/admin/"
        echo "Task list: http://127.0.0.1:8000/tasks/"
        echo ""
        fresh_venv/bin/python manage.py runserver
        ;;
    "makemigrations")
        run_django_command "makemigrations"
        ;;
    "migrate")
        run_django_command "migrate"
        ;;
    "createsuperuser")
        run_django_command "createsuperuser"
        ;;
    "shell")
        run_django_command "shell"
        ;;
    "setup_demo")
        echo "Setting up demo data..."
        fresh_venv/bin/python setup_demo_data.py
        ;;
    "install")
        if [ -z "$2" ]; then
            echo "Error: Please specify a package to install"
            echo "Usage: $0 install [package_name]"
            exit 1
        fi
        install_package "$2"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Available commands: runserver, makemigrations, migrate, createsuperuser, shell, setup_demo, install"
        exit 1
        ;;
esac 