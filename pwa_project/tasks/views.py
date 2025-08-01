from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json

# Index View - Home page showing task list
def index(request):
    # Fetch all tasks from the database to display them
    tasks = Task.objects.all()
    return render(request, "tasks/index.html", {
        "tasks": tasks  # Pass tasks to the template
    })