from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.getEntry, name="entry"),
    path("search/", views.search, name="search"),
    path("newPage/", views.newEntry, name="newPage"),
    path("editPage/<str:title>", views.editEntry, name="editPage"),
]

