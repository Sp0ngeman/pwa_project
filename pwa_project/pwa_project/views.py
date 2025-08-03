from django.http import HttpResponse
from django.views.decorators.http import require_GET
import os

@require_GET
def serve_service_worker(request):
    file_path = os.path.join(os.path.dirname(__file__), 'service-worker.js')
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type='application/javascript')
        return response