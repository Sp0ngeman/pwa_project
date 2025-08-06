# ChipIn - Task Management & Financial Platform

A web application combining personal task management with collaborative financial planning for students.

## Quick Start

```bash
# Start the server
cd pwa_project
../chipin_venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000/

## Login
- **Username**: `testuser`
- **Password**: `testpass123`
- **Admin**: http://127.0.0.1:8000/admin/

## Features

### Task Management
- Create, edit, complete, and delete tasks
- Organize tasks by category and priority
- Set due dates and track overdue items
- Filter and search functionality

### ChipIn Financial System
- Student account balance management
- Secure fund transfers between users
- Trusted adult oversight for all financial operations
- Transaction history and audit trails
- Spending limits and safety controls

### Security
- User authentication with GitHub OAuth support
- Trusted adult verification codes for financial operations
- Input validation and CSRF protection
- Age-appropriate financial safeguards

## Technology Stack
- **Backend**: Django 5.2.4
- **Database**: SQLite
- **Frontend**: Bootstrap 5 + vanilla JavaScript
- **Authentication**: Django Allauth

## Project Structure
```
pwa_project/
├── chipin/           # Main application
├── users/            # User management
├── manage.py         # Django management
└── db.sqlite3        # Database
```

## Financial Features

### Add Funds
Use trusted adult code `PARENT123` to add money to accounts.

### Transfer Money
Send funds between user accounts with balance validation.

### Account Management
- View transaction history
- Adjust spending limits (with adult approval)
- Account verification controls

## Development

### Models
- **Task**: User tasks with categories, priorities, due dates
- **Category**: Hierarchical task organization
- **Profile**: User financial profiles with balance management
- **Transaction**: Financial transaction logging and audit trails

### Key Views
- Dashboard with task overview and financial summary
- Task creation and management interface
- Payment dashboard with transaction history
- Balance management with trusted adult controls

## Admin Interface
Access full admin controls at http://127.0.0.1:8000/admin/
- Manage all users and profiles
- View all tasks and categories
- Monitor financial transactions
- System administration tools

---

**HSC Software Engineering Assignment - Task Management & Financial Platform**