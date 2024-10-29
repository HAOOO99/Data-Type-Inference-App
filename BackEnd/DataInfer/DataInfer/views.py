from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadFileForm
import os
from django.conf import settings
import csv
import chardet

import pandas as pd
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
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    if  not file_path.endswith('.csv'):
        print("Excl file upload "+file_path)
        try:
               
               
            df = pd.read_excel(file_path, engine='xlrd')
            print(df.head())

        except Exception as e:
            print(f"Failed to read Excel file: {e}")

     # After saving the file, read it back
    else: read_csv_file(file_path)


def read_csv_file(file_path):
    # Detect encoding of the file
    try:
        
        with open(file_path, mode='r', encoding='utf-8') as file:
            df = pd.read_csv(file)
            print(df)

    except UnicodeDecodeError:
        print("Unicode Decode Error encountered. Trying with a different encoding.")