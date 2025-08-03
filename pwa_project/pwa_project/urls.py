from django.contrib import admin
from django.urls import include, path
from tasks import views as task_views
from .views import serve_service_worker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(("users.urls", "users"), namespace="users")),
    path('tasks/', include(("tasks.urls", "tasks"), namespace="tasks")),
    path('accounts/', include('allauth.urls')),
    path('', task_views.index, name='home'),
    path('service-worker.js', serve_service_worker, name='service_worker'),
]