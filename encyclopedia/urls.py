from django.urls import path

from . import views

app_name = "encyclopedia"

# All potential URLs
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_info, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random/", views.random_entry, name="random")
]
