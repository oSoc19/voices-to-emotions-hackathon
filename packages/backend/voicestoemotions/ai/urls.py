from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from .views import upload_file

urlpatterns = [
    url(r'^$', upload_file),
]
