from django.urls import path

from . import views

app_name = "recipes"


urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/search/", views.search, name="search"),
    path("recipes/", views.recipe_list, name="list"),
    path("recipe/<int:id>/", views.recipe_details, name="details"),
    path("recipes/category/<int:id>/", views.category, name="category"),
]
