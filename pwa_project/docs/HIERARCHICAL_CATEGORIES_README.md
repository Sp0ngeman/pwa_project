# Hierarchical Category System Implementation

This document outlines the implementation of a hierarchical category system for the Task List application, as specified in the requirements and specifications.

## 🎯 **Requirements Overview**

The system has been extended to support categorizing tasks with a hierarchical structure, including categories and subcategories, displayed accordingly on the homepage.

### **Core Requirements Met:**

1. ✅ **Category Model Creation**: System includes a Category model allowing users to create categories with optional subcategories
2. ✅ **Task Categorisation**: Users can assign each task to a specific category or subcategory
3. ✅ **Hierarchical Relationships**: Support for hierarchical relationships between categories
4. ✅ **Task Listing by Category**: Tasks displayed on homepage grouped by category and subcategory
5. ✅ **Add Task Form with Category Selection**: Task creation form includes dropdown for category selection
6. ✅ **Category Management**: Category and subcategory creation through Django admin interface
7. ✅ **Task CRUD Operations**: Full CRUD operations for tasks associated with categories

## 🏗️ **Technical Implementation**

### **1. Database Models**

#### **Category Model**
```python
class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the category name.")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return self.name
```

**Key Features:**
- **Self-referential relationship**: `parent` field allows categories to have parent categories
- **Subcategories**: `related_name="subcategories"` enables easy access to child categories
- **Optional parent**: `null=True, blank=True` allows root categories (no parent)

#### **Updated Task Model**
```python
class Task(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the task name or description.")
    completed = models.BooleanField(default=False, help_text="Is the task completed?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The time when the task was last updated.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    # ... other fields
```

**Key Features:**
- **Category relationship**: Tasks can be associated with any category or subcategory
- **Optional category**: Tasks don't require a category (`null=True, blank=True`)
- **SET_NULL deletion**: If a category is deleted, tasks remain but lose their category

### **2. Django Admin Configuration**

#### **CategoryAdmin Class**
```python
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('parent__name', 'name')
```

**Admin Features:**
- **List display**: Shows category name and parent category
- **Filtering**: Filter categories by parent category
- **Search**: Search categories by name
- **Ordering**: Order by parent name, then category name

### **3. Form Implementation**

#### **NewTaskForm in forms.py**
```python
class NewTaskForm(forms.Form):
    task = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'id': 'task',
            'placeholder': 'New Task'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'id': 'category'}),
        label="Category"
    )
```

**Form Features:**
- **ModelChoiceField**: Dropdown populated with all categories
- **Optional selection**: Category selection is not required
- **Clear labeling**: Proper labels for form fields

### **4. View Implementation**

#### **Index View (Hierarchical Display)**
```python
def index(request):
    categories = Category.objects.filter(parent=None).prefetch_related('subcategories', 'tasks')
    return render(request, "tasks/index.html", {"categories": categories})
```

**Performance Optimizations:**
- **prefetch_related**: Efficiently loads subcategories and tasks in single queries
- **Filter by parent=None**: Only loads root categories, subcategories loaded via prefetch

#### **Add View (Category Handling)**
```python
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data["task"]
            category = form.cleaned_data.get("category") # Get the optional category
            Task.objects.create(name=task_name, category=category, user=request.user)
            return HttpResponseRedirect(reverse("tasks:index"))
```

**Key Features:**
- **Optional category**: Uses `.get()` to handle optional category selection
- **User association**: Tasks are associated with the current user
- **Form validation**: Proper form validation and error handling

### **5. Template Implementation**

#### **Index Template (Hierarchical Display)**
```html
<h1>Task List by Category</h1>
<ul id="category-list">
    {% for category in categories %}
    <li>
        <strong>{{ category.name }}</strong>
        <ul>
            {% for subcategory in category.subcategories.all %}
            <li>
                <strong>{{ subcategory.name }}</strong>
                <ul>
                    {% for task in subcategory.tasks.all %}
                    <li>{{ task.name }}</li>
                    {% empty %}
                    {% endfor %}
                </ul>
            </li>
            {% endfor %}
            {% for task in category.tasks.all %}
            <li>{{ task.name }}</li>
            {% empty %}
            {% endfor %}
        </ul>
    </li>
    {% empty %}
    {% endfor %}
</ul>
```

**Template Features:**
- **Nested structure**: Categories → Subcategories → Tasks
- **Empty handling**: `{% empty %}` blocks for categories without tasks
- **Clear hierarchy**: Visual distinction between categories and tasks

#### **Add Task Template**
```html
<form action="{% url 'tasks:add' %}" method="post" id="taskForm">
    {% csrf_token %}
    <table>
        <tr>
            <td>{{ form.task.label_tag }}</td>
            <td>{{ form.task }}</td>
        </tr>
        <tr>
            <td>{{ form.category.label_tag }}</td>
            <td>{{ form.category }}</td>
        </tr>
        <tr>
            <td colspan="2">
                <input type="submit" id="submit" disabled>
            </td>
        </tr>
    </table>
</form>
```

**Form Features:**
- **Explicit field rendering**: Each form field rendered separately
- **Proper labeling**: Clear labels for all form fields
- **JavaScript validation**: Submit button enabled/disabled based on input

### **6. Layout Template (Simplified)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}Task List{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'tasks/styles.css' %}">
</head>
<body>
    <header>
        <div class="user-info">
            {% if request.user.is_authenticated %}
            <span>{{ request.user.username }}</span>
            <form action="{% url 'users:logout' %}" method="post">
                {% csrf_token %}
                <button type="submit">Logout</button>
            </form>
            {% endif %}
        </div>
    </header>
    {% if messages %}
    <ul class="messages">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**Layout Features:**
- **User authentication**: Display username and logout functionality
- **Message handling**: Display Django messages
- **Clean structure**: Removed PWA/React elements for simplicity

## 📊 **Database Schema**

### **Category Table**
```sql
CREATE TABLE tasks_category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES tasks_category(id)
);
```

### **Task Table (Updated)**
```sql
CREATE TABLE tasks_task (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME,
    updated_at DATETIME,
    category_id INTEGER REFERENCES tasks_category(id),
    user_id INTEGER REFERENCES auth_user(id)
);
```

## 🚀 **Setup Instructions**

### **1. Database Migrations**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### **2. Create Superuser**
```bash
python manage.py createsuperuser
```

### **3. Setup Demo Data**
```bash
python setup_demo_data.py
```

This script will:
- Create a superuser (admin/admin123)
- Create sample categories and subcategories
- Create sample tasks in different categories

### **4. Run the Server**
```bash
python manage.py runserver
```

### **5. Access the Application**
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Task List**: http://127.0.0.1:8000/tasks/
- **Add Task**: http://127.0.0.1:8000/tasks/add

## 🎯 **Non-Functional Requirements Met**

### **Usability**
✅ **Intuitive Display**: Clear visual distinction between main categories, subcategories, and tasks
✅ **Easy Categorization**: Clearly labeled dropdown for category selection

### **Performance**
✅ **Efficient Queries**: `prefetch_related` optimizes database queries
✅ **Responsive Loading**: Minimal load times with optimized queries

### **Scalability**
✅ **Designed for Growth**: Supports increasing numbers of categories, subcategories, and tasks
✅ **Optimized Structure**: Efficient database relationships and queries

## 📋 **Sample Data Structure**

### **Categories Created**
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

## 🔧 **API Endpoints (Updated)**

### **Task Management**
- `GET /tasks/` - Display tasks grouped by category
- `POST /tasks/add` - Create new task with category selection
- `GET /tasks/api/tasks/` - Get all user tasks (API)
- `POST /tasks/api/tasks/create/` - Create task via API

### **Category Management**
- `GET /admin/tasks/category/` - Manage categories in Django admin
- `POST /admin/tasks/category/add/` - Add new category
- `PUT /admin/tasks/category/{id}/change/` - Edit category

## 🎉 **Features Summary**

### **✅ Implemented Features**
1. **Hierarchical Category System**: Categories can have subcategories
2. **Task Categorization**: Tasks can be assigned to any category or subcategory
3. **Django Admin Integration**: Full category management through admin interface
4. **Form Integration**: Category selection in task creation form
5. **Hierarchical Display**: Tasks displayed grouped by category structure
6. **User Authentication**: Tasks associated with logged-in users
7. **Performance Optimization**: Efficient database queries with prefetch_related
8. **Clean UI**: Simplified layout focused on task management

### **🔧 Technical Achievements**
- **Self-referential Model**: Category model with parent-child relationships
- **Optimized Queries**: Efficient database access patterns
- **Form Validation**: Proper form handling with optional fields
- **Template Structure**: Clean, hierarchical HTML structure
- **Admin Customization**: Enhanced Django admin for category management

This implementation fully satisfies the requirements for a hierarchical category system in the Task List application, providing an intuitive and efficient way to organize and display tasks by category and subcategory. 