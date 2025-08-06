from django.urls import path
from . import views

app_name = "chipin"

urlpatterns = [
   path("", views.index, name="index"),
   path("add/", views.add, name="add"),
   path("api/tasks/", views.get_tasks, name="get_tasks"),
   path("api/tasks/<int:task_id>/", views.get_task, name="get_task"),
   path("api/tasks/create/", views.create_task, name="create_task"),
   path("api/tasks/<int:task_id>/update/", views.update_task, name="update_task"),
   path("api/tasks/<int:task_id>/delete/", views.delete_task, name="delete_task"),
   path("api/tasks/<int:task_id>/toggle/", views.toggle_task, name="toggle_task"),
   path("api/tasks/stats/", views.task_stats, name="task_stats"),
   path("api/tasks/bulk-update/", views.bulk_update, name="bulk_update"),
   path("payments/", views.payment_dashboard, name="payment_dashboard"),
   path("payments/add-funds/", views.add_funds, name="add_funds"),
   path("payments/transfer/", views.transfer_funds, name="transfer_funds"),
   path("balance/", views.balance_management, name="balance_management"),
]
