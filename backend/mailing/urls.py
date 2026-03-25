from django.urls import path
from .views import select_template

urlpatterns = [
    path("select-template/", select_template, name="select_template"),
]
