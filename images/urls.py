from django.urls import path
from .views import home
from .views import upload

urlpatterns=[
    path('',home,name='home'),
    path('upload',upload,name='upload'),
]