from django.db import models

# Create your models here.
# api/forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()