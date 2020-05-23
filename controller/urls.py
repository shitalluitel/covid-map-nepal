from django.urls import path

from controller.views import view_home

urlpatterns = [
    path('', view_home)
]
