from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.file_upload, name='file_upload'),
    path('submit/', views.submit_data, name='submit_data'),
]