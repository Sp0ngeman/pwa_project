#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/oliver/Documents/Software Class/pwa_project/pwa_project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pwa_project.settings')
django.setup()

from django.contrib.auth.models import User
from tasks.models import Category, Task

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created with password 'admin123'")
    else:
        print("Superuser 'admin' already exists")

def create_sample_categories():
    """Create sample categories and subcategories"""
    # Create root categories
    home = Category.objects.get_or_create(name='Home')[0]
    school = Category.objects.get_or_create(name='School')[0]
    work = Category.objects.get_or_create(name='Work')[0]
    
    # Create subcategories
    chores = Category.objects.get_or_create(name='Chores', parent=home)[0]
    sport = Category.objects.get_or_create(name='Sport', parent=home)[0]
    assignments = Category.objects.get_or_create(name='Assignments', parent=school)[0]
    homework = Category.objects.get_or_create(name='Homework', parent=school)[0]
    
    print("Sample categories created:")
    print("- Home")
    print("  - Chores")
    print("  - Sport")
    print("- School")
    print("  - Assignments")
    print("  - Homework")
    print("- Work")

def create_sample_tasks():
    """Create sample tasks for demonstration"""
    # Get categories
    home = Category.objects.get(name='Home')
    chores = Category.objects.get(name='Chores')
    school = Category.objects.get(name='School')
    assignments = Category.objects.get(name='Assignments')
    work = Category.objects.get(name='Work')
    
    # Create sample tasks
    tasks_data = [
        ('Clean kitchen', chores),
        ('Do laundry', chores),
        ('Go for a run', Category.objects.get(name='Sport')),
        ('Complete project', assignments),
        ('Study for exam', assignments),
        ('Write report', work),
        ('Team meeting', work),
    ]
    
    for task_name, category in tasks_data:
        Task.objects.get_or_create(
            name=task_name,
            category=category,
            defaults={'completed': False}
        )
    
    print(f"Created {len(tasks_data)} sample tasks")

if __name__ == '__main__':
    print("Setting up demo data...")
    create_superuser()
    create_sample_categories()
    create_sample_tasks()
    print("Demo data setup complete!")
    print("\nYou can now:")
    print("1. Run the server: python manage.py runserver")
    print("2. Login to admin at http://127.0.0.1:8000/admin/ with username 'admin' and password 'admin123'")
    print("3. View the task list at http://127.0.0.1:8000/tasks/") 