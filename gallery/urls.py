from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.gallery, name='gallery-home'),
    path('upload/', views.upload_photo, name='upload-photo'),
]