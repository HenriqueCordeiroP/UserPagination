from django.urls import path

from .views import *

urlpatterns = [
    path("", user_pages, name="user_pages"),
    path("edit/<int:id>", edit_user, name="edit_user"),
    path("delete/<int:id>", delete_user, name="delete_user"),
]
