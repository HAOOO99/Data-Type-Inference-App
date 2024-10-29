from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadFileForm
import os
from django.conf import settings
# Create your views here.

@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file, e.g., save it
            handle_uploaded_file(request.FILES['file'])
            return JsonResponse({'message': 'File uploaded successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=400)

def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

