from django.urls import path
from .views import select_template, add_tags

urlpatterns = [
    path("select-template/", select_template, name="select_template"),
    path("add-tags/", add_tags, name="add tags"),
]
